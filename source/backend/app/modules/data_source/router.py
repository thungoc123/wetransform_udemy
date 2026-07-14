from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teacher import Teacher
from app.modules.data_source.repository import DataSourceRepository
from app.modules.data_source.schemas import (
    DataImportResponse,
    DataSourceOption,
    UdemyConnectionRequest,
    UdemyConnectionResponse,
)
from app.modules.data_source.service import DataSourceService
from app.shared.dependencies.auth import get_current_teacher
from app.shared.dependencies.database import get_db

router = APIRouter(prefix="/api/v1/data", tags=["Data Sources"])


def get_data_source_service(db: AsyncSession = Depends(get_db)) -> DataSourceService:
    repository = DataSourceRepository(db)
    return DataSourceService(repository)


@router.get("/sources", response_model=list[DataSourceOption])
async def list_data_sources(
    service: DataSourceService = Depends(get_data_source_service),
    current_teacher: Teacher = Depends(get_current_teacher),
):
    return await service.get_data_source_options()


@router.post("/udemy-connection", response_model=UdemyConnectionResponse)
async def connect_udemy(
    request: UdemyConnectionRequest,
    service: DataSourceService = Depends(get_data_source_service),
    current_teacher: Teacher = Depends(get_current_teacher),
):
    return await service.connect_udemy_api(
        teacher_id=current_teacher.id,
        client_id=request.client_id,
        client_secret=request.client_secret,
    )


@router.post("/upload", response_model=DataImportResponse)
async def upload_file(
    file: UploadFile = File(...),
    service: DataSourceService = Depends(get_data_source_service),
    current_teacher: Teacher = Depends(get_current_teacher),
):
    return await service.upload_file(teacher_id=current_teacher.id, file=file)
