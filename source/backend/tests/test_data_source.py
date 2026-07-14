import uuid

import pytest
from httpx import AsyncClient

from app.main import app
from app.models.teacher import Teacher
from app.shared.dependencies.auth import get_current_teacher


def override_get_current_teacher():
    return Teacher(id=uuid.uuid4(), email="test@example.com")


app.dependency_overrides[get_current_teacher] = override_get_current_teacher


@pytest.mark.asyncio
async def test_get_data_source_options(client: AsyncClient):
    response = await client.get("/api/v1/data/sources")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "csv_upload"


@pytest.mark.asyncio
async def test_connect_udemy_api(client: AsyncClient):
    payload = {"clientId": "test_client_id", "clientSecret": "test_client_secret"}
    response = await client.post("/api/v1/data/udemy-connection", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "connected"
    assert "id" in data
