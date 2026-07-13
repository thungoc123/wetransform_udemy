from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.config import settings

# Create Async Engine for PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.APP_ENV == "development"),  # In SQL queries in development
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before usage
)

# Session factory for Dependency Injection
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Declarative Base for all ORM models
Base = declarative_base()
