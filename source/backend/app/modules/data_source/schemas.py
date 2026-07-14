import uuid

from pydantic import BaseModel, Field


class DataSourceOption(BaseModel):
    id: str
    name: str
    type: str


class UdemyConnectionRequest(BaseModel):
    client_id: str = Field(alias="clientId", description="Udemy API Client ID")
    client_secret: str = Field(
        alias="clientSecret", description="Udemy API Client Secret"
    )


class UdemyConnectionResponse(BaseModel):
    id: uuid.UUID
    teacher_id: uuid.UUID = Field(alias="teacherId")
    status: str

    model_config = {"populate_by_name": True}


class DataImportResponse(BaseModel):
    import_id: uuid.UUID = Field(alias="importId")
    file_name: str = Field(alias="fileName")
    status: str
    error_message: str | None = Field(None, alias="errorMessage")
    row_count: int | None = Field(None, alias="rowCount")

    model_config = {"populate_by_name": True}
