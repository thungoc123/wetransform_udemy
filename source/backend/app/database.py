"""
Database Configuration Module.

This module provides the global asynchronous SQLAlchemy engine,
session maker, and declarative base used across the application.
"""

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
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
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


# Declarative Base for all ORM models
Base = declarative_base()


class TimestampMixin:
    """Mixin to add audit timestamp columns to models."""

    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
        nullable=False,
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
        nullable=False,
    )
    deleted_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
