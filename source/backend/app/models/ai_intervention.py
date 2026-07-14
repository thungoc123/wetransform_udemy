"""
AI & Intervention Models.

This module defines the SQLAlchemy models for AiInsight, Recommendation, and ReminderLog.
"""

import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base, TimestampMixin


class AiInsight(Base, TimestampMixin):
    """
    Model representing AI-generated insights for a lesson.
    """

    __tablename__ = "ai_insights"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    hypothesis = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)
    raw_prompt = Column(Text, nullable=True)
    raw_response = Column(Text, nullable=True)
    model_version = Column(String(50), nullable=False)

    # Relationships
    lesson = relationship("Lesson", backref="ai_insights")


class Recommendation(Base, TimestampMixin):
    """
    Model representing an AI-generated action recommendation.
    """

    __tablename__ = "recommendations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    ai_insight_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ai_insights.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    suggestion_text = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    actioned_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    ai_insight = relationship("AiInsight", backref="recommendations")


class ReminderLog(Base, TimestampMixin):
    """
    Model representing a reminder sent to a student.
    """

    __tablename__ = "reminder_logs"

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
    teacher_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    message_body = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    sent_at = Column(DateTime(timezone=True), nullable=True)
    failure_reason = Column(Text, nullable=True)
    tracking_expires_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    student_enrollment = relationship("StudentEnrollment", backref="reminder_logs")
    lesson = relationship("Lesson", backref="reminder_logs")
    teacher = relationship("Teacher", backref="reminder_logs")
