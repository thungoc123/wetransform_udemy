"""
Course Models.

This module defines the SQLAlchemy models for Course, Module, and Lesson.
"""

import uuid

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base, TimestampMixin


class Course(Base, TimestampMixin):
    """
    Model representing a course.
    """

    __tablename__ = "courses"

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
    udemy_course_id = Column(String(100), unique=True, nullable=True)
    title = Column(String(500), nullable=False)
    student_count = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="imported")

    data_import_id = Column(
        UUID(as_uuid=True),
        ForeignKey("data_imports.id", ondelete="SET NULL"),
        nullable=True,
    )
    udemy_connection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("udemy_connections.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    teacher = relationship("Teacher", backref="courses")
    data_import = relationship("DataImport", backref="courses")
    udemy_connection = relationship("UdemyConnection", backref="courses")
    modules = relationship(
        "Module", back_populates="course", cascade="all, delete-orphan"
    )
    lessons = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan"
    )


class Module(Base, TimestampMixin):
    """
    Model representing a module inside a course.
    """

    __tablename__ = "modules"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(500), nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship(
        "Lesson", back_populates="module", cascade="all, delete-orphan"
    )


class Lesson(Base, TimestampMixin):
    """
    Model representing a lesson inside a module.
    """

    __tablename__ = "lessons"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    module_id = Column(
        UUID(as_uuid=True),
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title = Column(String(500), nullable=False)
    type = Column(String(20), nullable=False)  # video, article, quiz, assignment
    order_index = Column(Integer, nullable=False)
    duration_seconds = Column(Integer, nullable=True)
    drop_off_rate = Column(Float, nullable=True)
    has_warning = Column(Boolean, default=False)
    student_count = Column(Integer, nullable=False, default=0)

    # Relationships
    course = relationship("Course", back_populates="lessons")
    module = relationship("Module", back_populates="lessons")
