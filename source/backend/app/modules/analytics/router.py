from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/health")
async def analytics_health():
    return {"status": "ok", "module": "analytics"}
