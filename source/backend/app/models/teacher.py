"""
Teacher Model Module.

This module defines the SQLAlchemy model for the Teacher entity,
who is the main user/creator in the platform.
"""

import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base, TimestampMixin


class Teacher(Base, TimestampMixin):
    """
    Teacher model representing the platform users (course creators).
    """

    __tablename__ = "teachers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="UUID v4, PK",
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Teacher's login email",
    )
    password_hash = Column(
        String(255),
        nullable=False,
        comment="Encrypted password hash",
    )
    name = Column(
        String(255),
        nullable=False,
        comment="Teacher's full name",
    )
    failed_login_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Count of consecutive failed logins",
    )
    locked_until = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Account locked until timestamp",
    )
