from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.get("/health")
async def auth_health():
    return {"status": "ok", "module": "auth"}
