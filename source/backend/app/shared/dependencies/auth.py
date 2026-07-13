import uuid
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.dependencies.database import get_db
from app.shared.security import decode_access_token
from app.shared.exceptions import AppException
from app.shared.constants import ErrorMessage
from app.modules.auth.models import Teacher

bearer_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def extract_teacher_id(payload: dict) -> uuid.UUID:
    """Extract and validate the teacher ID from the JWT payload."""
    teacher_id_str = payload.get("sub")
    if not teacher_id_str:
        raise AppException(
            message=ErrorMessage.TOKEN_MISSING_SUBJECT, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    try:
        return uuid.UUID(teacher_id_str)
    except ValueError:
        raise AppException(
            message=ErrorMessage.INVALID_TOKEN_FORMAT, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )

async def find_teacher(db: AsyncSession, teacher_id: uuid.UUID) -> Teacher:
    """Query the database to find the teacher by ID."""
    result = await db.execute(select(Teacher).where(Teacher.id == teacher_id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise AppException(
            message=ErrorMessage.TEACHER_NOT_FOUND, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return teacher

async def get_current_teacher(
    token: str = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> Teacher:
    """
    Dependency validates JWT token and returns the current teacher.
    """
    # 1. Decode token
    try:
        payload = decode_access_token(token)
    except AppException:
        raise
    except Exception:
        raise AppException(
            message=ErrorMessage.INVALID_TOKEN, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # 2. Extract ID
    teacher_id = extract_teacher_id(payload)
    
    # 3. Find Teacher
    teacher = await find_teacher(db, teacher_id)
    
    return teacher
