from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/intervention", tags=["Intervention"])


@router.get("/health")
async def intervention_health():
    return {"status": "ok", "module": "intervention"}
