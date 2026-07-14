from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import authenticate_teacher
from app.shared.dependencies.database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await authenticate_teacher(db, request.email, request.password)
