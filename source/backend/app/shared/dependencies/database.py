from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency provides an async database session.
    Yields a real SQLAlchemy AsyncSession.
    """
    async with async_session_maker() as session:
        yield session
