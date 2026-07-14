"""
Models package initialization.

Import all SQLAlchemy models here so that they are registered with the Base metadata.
This is required for Alembic to auto-generate migrations.
"""

from app.models.activity import LearningActivity, StudentEnrollment
from app.models.ai_intervention import AiInsight, Recommendation, ReminderLog
from app.models.course import Course, Lesson, Module
from app.models.import_data import DataImport, UdemyConnection
from app.models.teacher import Teacher

__all__ = [
    "LearningActivity",
    "StudentEnrollment",
    "AiInsight",
    "Recommendation",
    "ReminderLog",
    "Course",
    "Lesson",
    "Module",
    "DataImport",
    "UdemyConnection",
    "Teacher",
]
