from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/data-import", tags=["Data Import"])


@router.get("/health")
async def data_import_health():
    return {"status": "ok", "module": "data_import"}
