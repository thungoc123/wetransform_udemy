import os
import uuid

from fastapi import UploadFile, status

from app.modules.data_source.repository import DataSourceRepository
from app.modules.data_source.schemas import (
    DataImportResponse,
    DataSourceOption,
    UdemyConnectionResponse,
)
from app.modules.data_source.tasks import process_import_master_task
from app.shared.encryption import encryptor
from app.shared.error_codes import ErrorCode
from app.shared.exceptions import AppException


class DataSourceService:
    def __init__(self, repository: DataSourceRepository):
        self.repository = repository
        self.upload_dir = "uploads/data_imports"
        os.makedirs(self.upload_dir, exist_ok=True)

    async def get_data_source_options(self) -> list[DataSourceOption]:
        return [
            DataSourceOption(id="csv_upload", name="Upload file CSV", type="file"),
            DataSourceOption(id="udemy_api", name="Kết nối Udemy API", type="api"),
        ]

    async def connect_udemy_api(
        self, teacher_id: uuid.UUID, client_id: str, client_secret: str
    ) -> UdemyConnectionResponse:
        # Encrypt the credentials
        client_id_enc = encryptor.encrypt(client_id)
        client_secret_enc = encryptor.encrypt(client_secret)

        connection = await self.repository.save_udemy_connection(
            teacher_id=teacher_id,
            client_id_enc=client_id_enc,
            client_secret_enc=client_secret_enc,
        )

        return UdemyConnectionResponse(
            id=connection.id,  # type: ignore
            teacherId=connection.teacher_id,  # type: ignore
            status=str(connection.status),
        )

    async def upload_file(
        self, teacher_id: uuid.UUID, file: UploadFile
    ) -> DataImportResponse:
        if not file.filename or not file.filename.endswith(".csv"):
            raise AppException(
                message="Chỉ hỗ trợ định dạng file .csv",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCode.VALIDATION_ERROR,
            )

        # Generate a unique path
        file_ext = os.path.splitext(file.filename)[1] if file.filename else ".csv"
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        # Calculate size while saving
        size = 0
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                size += len(chunk)
                buffer.write(chunk)

        if size > 100 * 1024 * 1024:  # 100MB limit for MVP
            os.remove(file_path)
            raise AppException(
                message="File quá lớn, vượt quá giới hạn 100MB",
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                error_code=ErrorCode.VALIDATION_ERROR,
            )

        # Create DB record
        data_import = await self.repository.create_data_import(
            teacher_id=teacher_id,
            file_name=file.filename or "unknown.csv",
            file_path=file_path,
            size=size,
        )

        # Dispatch background task
        process_import_master_task.delay(str(data_import.id), file_path, str(teacher_id))  # type: ignore

        return DataImportResponse(
            importId=data_import.id,  # type: ignore
            fileName=data_import.file_name,  # type: ignore
            status=str(data_import.status),
        )
