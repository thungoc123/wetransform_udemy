import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.import_data import DataImport, UdemyConnection


class DataSourceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_udemy_connection(
        self, teacher_id: uuid.UUID
    ) -> UdemyConnection | None:
        stmt = select(UdemyConnection).where(UdemyConnection.teacher_id == teacher_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def save_udemy_connection(
        self, teacher_id: uuid.UUID, client_id_enc: str, client_secret_enc: str
    ) -> UdemyConnection:
        existing = await self.get_udemy_connection(teacher_id)
        if existing:
            existing.client_id_encrypted = client_id_enc  # type: ignore
            existing.client_secret_encrypted = client_secret_enc  # type: ignore
            existing.status = "connected"  # type: ignore
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        new_connection = UdemyConnection(
            teacher_id=teacher_id,
            client_id_encrypted=client_id_enc,
            client_secret_encrypted=client_secret_enc,
            status="connected",
        )
        self.db.add(new_connection)
        await self.db.commit()
        await self.db.refresh(new_connection)
        return new_connection

    async def create_data_import(
        self, teacher_id: uuid.UUID, file_name: str, file_path: str, size: int
    ) -> DataImport:
        new_import = DataImport(
            teacher_id=teacher_id,
            file_name=file_name,
            file_path=file_path,
            file_size_bytes=size,
            status="pending",
        )
        self.db.add(new_import)
        await self.db.commit()
        await self.db.refresh(new_import)
        return new_import

    async def update_data_import_status(
        self,
        import_id: uuid.UUID,
        status: str,
        error_message: Optional[str] = None,
        row_count: Optional[int] = None,
    ):
        stmt = (
            update(DataImport)
            .where(DataImport.id == import_id)
            .values(
                status=status,
                error_message=error_message,
                row_count=row_count,
            )
        )
        await self.db.execute(stmt)
        await self.db.commit()
