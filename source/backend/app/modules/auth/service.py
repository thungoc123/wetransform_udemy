from datetime import datetime, timedelta, timezone

import jwt
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.teacher import Teacher
from app.modules.auth.repository import (
    get_teacher_by_email,
    reset_login_success,
    update_login_fail,
)
from app.modules.auth.schemas import TokenResponse
from app.shared.error_codes import ErrorCode
from app.shared.exceptions import AppException
from app.shared.security import verify_password


def create_access_token(teacher: Teacher) -> TokenResponse:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode = {"sub": str(teacher.id), "exp": expire}

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return TokenResponse(
        token=encoded_jwt,
        teacherId=str(teacher.id),
        name=str(teacher.name),
        expiresAt=int(expire.timestamp()),
    )


async def authenticate_teacher(
    db: AsyncSession, email: str, password: str
) -> TokenResponse:
    teacher = await get_teacher_by_email(db, email)
    if not teacher:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Email hoặc Mật khẩu không chính xác",
        )

    if teacher.locked_until and teacher.locked_until > datetime.now(timezone.utc):
        raise AppException(
            status_code=status.HTTP_423_LOCKED,
            error_code=ErrorCode.AUTH_FORBIDDEN,
            message="Tài khoản bị khóa tạm thời (15 phút)",
        )

    if not verify_password(password, str(teacher.password_hash)):
        await update_login_fail(db, teacher)
        if teacher.failed_login_count >= 5:
            raise AppException(
                status_code=status.HTTP_423_LOCKED,
                error_code=ErrorCode.AUTH_FORBIDDEN,
                message="Tài khoản bị khóa tạm thời (15 phút)",
            )
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Email hoặc Mật khẩu không chính xác",
        )

    await reset_login_success(db, teacher)
    return create_access_token(teacher)
