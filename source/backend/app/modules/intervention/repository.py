import uuid
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import LearningActivity, StudentEnrollment
from app.models.ai_intervention import ReminderLog
from app.models.course import Course, Lesson


class InterventionRepository:
    """Repository handling all database queries for the Intervention module."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_course_by_id(self, course_id: uuid.UUID) -> Course | None:
        stmt = select(Course).where(Course.id == course_id, Course.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_lesson_by_id(
        self, course_id: uuid.UUID, lesson_id: uuid.UUID
    ) -> Lesson | None:
        stmt = select(Lesson).where(
            Lesson.id == lesson_id, Lesson.course_id == course_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_students_stopped_at_lesson(
        self, course_id: uuid.UUID, lesson_id: uuid.UUID
    ) -> Sequence[StudentEnrollment]:
        """Fetch students who interacted with this lesson but did not complete the course."""
        stmt = (
            select(StudentEnrollment)
            .join(
                LearningActivity,
                LearningActivity.student_enrollment_id == StudentEnrollment.id,
            )
            .where(
                StudentEnrollment.course_id == course_id,
                StudentEnrollment.progress_percent < 100,
                LearningActivity.lesson_id == lesson_id,
            )
            .distinct()
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_recent_reminders(
        self,
        lesson_id: uuid.UUID,
        student_enrollment_ids: list[uuid.UUID],
        since: datetime,
    ) -> Sequence[ReminderLog]:
        if not student_enrollment_ids:
            return []
        stmt = select(ReminderLog).where(
            ReminderLog.lesson_id == lesson_id,
            ReminderLog.student_enrollment_id.in_(student_enrollment_ids),
            ReminderLog.sent_at >= since,
            ReminderLog.status == "sent",
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def save_reminder_log(self, reminder_log: ReminderLog) -> None:
        self.db.add(reminder_log)
        await self.db.commit()
        await self.db.refresh(reminder_log)
