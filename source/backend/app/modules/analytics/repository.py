import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activity import LearningActivity, StudentEnrollment
from app.models.ai_intervention import AiInsight, Recommendation
from app.models.course import Course, Lesson, Module


class AnalyticsRepository:
    """Repository handling all database queries for the Analytics & AI Insights module."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_course_by_id(self, course_id: uuid.UUID) -> Course | None:
        """Fetch a course by ID, ensuring it is not deleted."""
        stmt = select(Course).where(Course.id == course_id, Course.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_course_with_structure(self, course_id: uuid.UUID) -> Course | None:
        """Fetch a course with modules and lessons loaded."""
        stmt = (
            select(Course)
            .where(Course.id == course_id, Course.deleted_at.is_(None))
            .options(
                selectinload(Course.modules).selectinload(Module.lessons),
                selectinload(Course.lessons),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_lesson_by_id(
        self, course_id: uuid.UUID, lesson_id: uuid.UUID
    ) -> Lesson | None:
        """Fetch a lesson by ID belonging to a specific course."""
        stmt = select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
            Lesson.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_enrollments_for_course(
        self, course_id: uuid.UUID
    ) -> list[StudentEnrollment]:
        """Fetch all active enrollments for a course."""
        stmt = select(StudentEnrollment).where(
            StudentEnrollment.course_id == course_id,
            StudentEnrollment.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_activities_for_course(
        self, course_id: uuid.UUID
    ) -> list[tuple[uuid.UUID, uuid.UUID, int]]:
        """
        Fetch learning activities for a course, joining lessons to get the order_index.
        Returns tuples of (student_enrollment_id, lesson_id, order_index).
        """
        stmt = (
            select(
                LearningActivity.student_enrollment_id,
                LearningActivity.lesson_id,
                Lesson.order_index,
            )
            .join(Lesson, LearningActivity.lesson_id == Lesson.id)
            .where(Lesson.course_id == course_id)
        )
        result = await self.db.execute(stmt)
        return [(row[0], row[1], row[2]) for row in result.all()]

    async def get_activities_for_lesson(
        self, lesson_id: uuid.UUID
    ) -> list[LearningActivity]:
        """Fetch all learning activities recorded for a specific lesson."""
        stmt = select(LearningActivity).where(LearningActivity.lesson_id == lesson_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_video_timeline_analysis(
        self, lesson_id: uuid.UUID
    ) -> list[tuple[int, int]]:
        """Fetch video pause locations grouped by second, ordered by second."""
        stmt = (
            select(
                LearningActivity.video_stop_at_second, func.count(LearningActivity.id)
            )
            .where(
                LearningActivity.lesson_id == lesson_id,
                LearningActivity.video_stop_at_second.isnot(None),
            )
            .group_by(LearningActivity.video_stop_at_second)
            .order_by(LearningActivity.video_stop_at_second)
        )
        result = await self.db.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]

    async def get_cached_ai_insight(self, lesson_id: uuid.UUID) -> AiInsight | None:
        """Fetch cached AI Insight for a lesson, loading recommendations."""
        stmt = (
            select(AiInsight)
            .where(AiInsight.lesson_id == lesson_id)
            .options(selectinload(AiInsight.recommendations))
            .order_by(AiInsight.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def save_ai_insight(self, insight: AiInsight) -> AiInsight:
        """Save a new AI Insight along with its recommendations."""
        self.db.add(insight)
        await self.db.commit()
        await self.db.refresh(insight)
        return insight

    async def get_recommendation_by_id(
        self, course_id: uuid.UUID, lesson_id: uuid.UUID, recommendation_id: uuid.UUID
    ) -> Recommendation | None:
        """Fetch a recommendation and verify it belongs to the lesson and course."""
        stmt = (
            select(Recommendation)
            .join(AiInsight, Recommendation.ai_insight_id == AiInsight.id)
            .join(Lesson, AiInsight.lesson_id == Lesson.id)
            .where(
                Recommendation.id == recommendation_id,
                Lesson.id == lesson_id,
                Lesson.course_id == course_id,
                Recommendation.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def commit(self) -> None:
        """Commit changes to the database."""
        await self.db.commit()
