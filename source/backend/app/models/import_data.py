"""
Data Import Models.

This module defines the SQLAlchemy models for UdemyConnection and DataImport.
"""

import uuid

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base, TimestampMixin


class UdemyConnection(Base, TimestampMixin):
    """
    Model representing a teacher's connection to the Udemy API.
    """

    __tablename__ = "udemy_connections"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    teacher_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_id_encrypted = Column(Text, nullable=False)
    client_secret_encrypted = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    connected_at = Column(DateTime(timezone=True), nullable=True)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    teacher = relationship("Teacher", backref="udemy_connections")


class DataImport(Base, TimestampMixin):
    """
    Model representing a file upload from Udemy (CSV/XLSX).
    """

    __tablename__ = "data_imports"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    teacher_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    error_message = Column(Text, nullable=True)
    row_count = Column(Integer, nullable=True)

    # Relationships
    teacher = relationship("Teacher", backref="data_imports")
