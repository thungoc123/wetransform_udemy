"""
Activity Models.

This module defines the SQLAlchemy models for StudentEnrollment and LearningActivity.
"""

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base, TimestampMixin


class StudentEnrollment(Base, TimestampMixin):
    """
    Model representing a student enrolled in a course.
    """

    __tablename__ = "student_enrollments"

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
    udemy_student_id = Column(String(100), nullable=False)
    masked_name = Column(String(255), nullable=False)
    email_encrypted = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    last_activity_at = Column(DateTime(timezone=True), nullable=True)
    progress_percent = Column(Float, default=0.0)

    # Relationships
    course = relationship("Course", backref="enrollments")


class LearningActivity(Base, TimestampMixin):
    """
    Model representing a student's activity on a lesson.
    """

    __tablename__ = "learning_activities"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    student_enrollment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("student_enrollments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    activity_type = Column(String(20), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    video_stop_at_second = Column(Integer, nullable=True)
    is_completed = Column(Boolean, default=False)

    # Relationships
    student_enrollment = relationship("StudentEnrollment", backref="activities")
    lesson = relationship("Lesson", backref="activities")
