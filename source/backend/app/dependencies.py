from typing import AsyncGenerator, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# import AsyncSession will be used in FND-005
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.database import async_session

# OAuth2 scheme for JWT token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db() -> AsyncGenerator[Any, None]:
    """
    Dependency provides an async database session.
    [FND-005] Will be updated to yield a real SQLAlchemy AsyncSession.
    """
    # async with async_session() as session:
    #     yield session
    yield None  # Stub for now


async def get_current_teacher(
    token: str = Depends(oauth2_scheme),
    db: Any = Depends(get_db),
) -> dict:
    """
    Dependency validates JWT token and returns the current teacher.
    [FND-017] Will be updated to decode JWT and return actual Teacher model.
    """
    # payload = decode_jwt(token)
    # teacher = await db.execute(...)
    # return teacher
    
    # Stub response
    return {"id": "stub-uuid-1234", "email": "stub_teacher@example.com"}


# ==========================================
# DI FACTORY TEMPLATE (For reference)
# ==========================================
# def get_analytics_service(
#     db: AsyncSession = Depends(get_db),
# ) -> AnalyticsService:
#     course_repo = CourseRepository(db)
#     return AnalyticsService(course_repo)
#
# @router.get("/dashboard")
# async def get_dashboard(
#     teacher: dict = Depends(get_current_teacher),
#     service: AnalyticsService = Depends(get_analytics_service)
# ):
#     return await service.get_dashboard(teacher["id"])
