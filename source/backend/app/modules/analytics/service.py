import uuid
from datetime import datetime, timezone

from fastapi import status

from app.agents.workflows.insight_workflow import generate_insight_via_llm
from app.models.ai_intervention import AiInsight, Recommendation
from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.schemas import (
    AIInsightResponse,
    DashboardResponse,
    DropOffResponse,
    EngagementMetrics,
    InsightDetail,
    LessonAnalyticsResponse,
    LessonDropOff,
    ModuleDropOff,
    RecommendationActionResponse,
    RecommendationDetail,
    TimelinePoint,
)
from app.shared.error_codes import ErrorCode
from app.shared.exceptions import AppException


class AnalyticsService:
    """Service layer handling analytics calculations and orchestrating AI workflows."""

    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    async def _verify_course_ownership(
        self, course_id: uuid.UUID, teacher_id: uuid.UUID
    ) -> None:
        """Verify that the course exists and belongs to the teacher."""
        course = await self.repository.get_course_by_id(course_id)
        if not course:
            raise AppException(
                message="Khóa học không tồn tại",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )
        if course.teacher_id != teacher_id:
            raise AppException(
                message="Bạn không có quyền truy cập khóa học này",
                status_code=status.HTTP_403_FORBIDDEN,
                error_code=ErrorCode.AUTH_FORBIDDEN,
            )

    async def get_dashboard(
        self, course_id: uuid.UUID, teacher_id: uuid.UUID, now: datetime | None = None
    ) -> DashboardResponse:
        """Calculate course overview dashboard metrics."""
        if now is None:
            now = datetime.now(timezone.utc)

        await self._verify_course_ownership(course_id, teacher_id)
        enrollments = await self.repository.get_enrollments_for_course(course_id)

        if not enrollments:
            return DashboardResponse(
                course_id=course_id,
                completion_rate=0.0,
                drop_off_rate=0.0,
                active_students=0,
                inactive_students=0,
                at_risk_students=0,
            )

        active_count = 0
        at_risk_count = 0
        inactive_count = 0
        total_students = len(enrollments)
        progress_sum = 0.0

        for enrollment in enrollments:
            progress_sum += enrollment.progress_percent
            last_act = enrollment.last_activity_at

            if last_act is None:
                inactive_count += 1
            else:
                # Ensure last_act has timezone info
                if last_act.tzinfo is None:
                    last_act = last_act.replace(tzinfo=timezone.utc)

                diff = now - last_act
                days = diff.days

                if days <= 7:
                    active_count += 1
                elif 14 <= days <= 29:
                    at_risk_count += 1
                elif days >= 30:
                    inactive_count += 1

        # Check if progress is stored as percentage (0-100) or ratio (0-1)
        avg_progress = progress_sum / total_students
        completion_rate = avg_progress / 100.0 if avg_progress > 1.0 else avg_progress
        drop_off_rate = (inactive_count + at_risk_count) / total_students

        return DashboardResponse(
            course_id=course_id,
            completion_rate=round(completion_rate, 4),
            drop_off_rate=round(drop_off_rate, 4),
            active_students=active_count,
            inactive_students=inactive_count,
            at_risk_students=at_risk_count,
        )

    async def get_drop_off_analysis(
        self, course_id: uuid.UUID, teacher_id: uuid.UUID, threshold: float = 0.20
    ) -> DropOffResponse:
        """Calculate funnel drop-off rate per lesson and module."""
        await self._verify_course_ownership(course_id, teacher_id)

        course = await self.repository.get_course_with_structure(course_id)
        if not course:
            raise AppException(
                message="Khóa học không tồn tại hoặc lỗi cấu trúc",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )

        # Get activities to determine student progress
        activities = await self.repository.get_activities_for_course(course_id)

        student_started_lessons: dict[uuid.UUID, set[uuid.UUID]] = {}
        student_max_order: dict[uuid.UUID, tuple[uuid.UUID, int]] = {}

        for student_id, lesson_id, order_index in activities:
            if student_id not in student_started_lessons:
                student_started_lessons[student_id] = set()
            student_started_lessons[student_id].add(lesson_id)

            if student_id not in student_max_order:
                student_max_order[student_id] = (lesson_id, order_index)
            else:
                if order_index > student_max_order[student_id][1]:
                    student_max_order[student_id] = (lesson_id, order_index)

        # Precompute timeline for video lessons with student_count >= 30
        lesson_data = {}
        for lesson in course.lessons:
            # unique students who started this lesson
            started_students = [
                sid
                for sid, slist in student_started_lessons.items()
                if lesson.id in slist
            ]
            student_count = len(started_students)

            # unique students who stopped at this lesson
            stopped_count = sum(
                1 for sid, val in student_max_order.items() if val[0] == lesson.id
            )

            drop_off_rate: float | None = (
                stopped_count / student_count if student_count > 0 else 0.0
            )

            timeline_analysis = None
            has_warning = False

            if student_count >= 30:
                has_warning = (
                    drop_off_rate > threshold if drop_off_rate is not None else False
                )
                if lesson.type == "video":
                    db_timeline = await self.repository.get_video_timeline_analysis(
                        lesson.id
                    )
                    timeline_analysis = [
                        TimelinePoint(second=sec, count=cnt) for sec, cnt in db_timeline
                    ]
            else:
                drop_off_rate = None

            lesson_data[lesson.id] = {
                "drop_off_rate": drop_off_rate,
                "has_warning": has_warning,
                "timeline_analysis": timeline_analysis,
            }

        # Build response hierarchy
        modules_list = []
        # Sort modules by order_index
        sorted_modules = sorted(course.modules, key=lambda m: m.order_index)

        for module in sorted_modules:
            lessons_list = []
            # Sort lessons in this module by order_index
            sorted_lessons = sorted(module.lessons, key=lambda lsn: lsn.order_index)

            for lesson in sorted_lessons:
                l_stats = lesson_data.get(
                    lesson.id,
                    {
                        "drop_off_rate": None,
                        "has_warning": False,
                        "timeline_analysis": None,
                    },
                )
                lessons_list.append(
                    LessonDropOff(
                        lesson_id=lesson.id,
                        lesson_title=lesson.title,
                        type=lesson.type,
                        drop_off_rate=l_stats["drop_off_rate"],
                        has_warning=l_stats["has_warning"],
                        timeline_analysis=l_stats["timeline_analysis"],
                    )
                )

            modules_list.append(
                ModuleDropOff(
                    module_id=module.id, module_title=module.title, lessons=lessons_list
                )
            )

        return DropOffResponse(modules=modules_list)

    async def get_lesson_analytics(
        self, course_id: uuid.UUID, lesson_id: uuid.UUID, teacher_id: uuid.UUID
    ) -> LessonAnalyticsResponse:
        """Fetch detail analytics for a specific lesson."""
        await self._verify_course_ownership(course_id, teacher_id)

        lesson = await self.repository.get_lesson_by_id(course_id, lesson_id)
        if not lesson:
            raise AppException(
                message="Bài học không tồn tại",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )

        activities = await self.repository.get_activities_for_lesson(lesson_id)

        if not activities:
            return LessonAnalyticsResponse(
                lesson_id=lesson_id,
                lesson_title=lesson.title,
                type=lesson.type,
                engagement_metrics=EngagementMetrics(
                    student_count=0, completion_rate=0.0, average_duration_seconds=0.0
                ),
                timeline_analysis=[],
                reliability_message="Dữ liệu quá ít để phân tích tin cậy.",
            )

        completed_students = {
            act.student_enrollment_id for act in activities if act.is_completed
        }
        total_students = {act.student_enrollment_id for act in activities}
        student_count = len(total_students)
        completion_rate = (
            len(completed_students) / student_count if student_count > 0 else 0.0
        )

        durations = [
            act.duration_seconds
            for act in activities
            if act.duration_seconds is not None
        ]
        average_duration = sum(durations) / len(durations) if durations else 0.0

        reliability_message = None
        timeline_analysis = None

        if student_count < 30:
            reliability_message = "Dữ liệu quá ít để phân tích tin cậy."
        else:
            if lesson.type == "video":
                db_timeline = await self.repository.get_video_timeline_analysis(
                    lesson_id
                )
                timeline_analysis = [
                    TimelinePoint(second=sec, count=cnt) for sec, cnt in db_timeline
                ]

        return LessonAnalyticsResponse(
            lesson_id=lesson_id,
            lesson_title=lesson.title,
            type=lesson.type,
            engagement_metrics=EngagementMetrics(
                student_count=student_count,
                completion_rate=round(completion_rate, 4),
                average_duration_seconds=round(average_duration, 2),
            ),
            timeline_analysis=timeline_analysis,
            reliability_message=reliability_message,
        )

    async def get_ai_insights(
        self, course_id: uuid.UUID, lesson_id: uuid.UUID, teacher_id: uuid.UUID
    ) -> AIInsightResponse:
        """Retrieve cached AI insights or trigger OpenAI workflow to generate new ones."""
        await self._verify_course_ownership(course_id, teacher_id)

        lesson = await self.repository.get_lesson_by_id(course_id, lesson_id)
        if not lesson:
            raise AppException(
                message="Bài học không tồn tại",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )

        # 1. Check database cache
        cached = await self.repository.get_cached_ai_insight(lesson_id)
        if cached:
            insights_list = [
                InsightDetail(
                    insight_id=cached.id,
                    hypothesis=cached.hypothesis,
                    confidence_score=cached.confidence_score,
                )
            ]
            recs_list = [
                RecommendationDetail(
                    recommendation_id=rec.id,
                    suggestion_text=rec.suggestion_text,
                    status=rec.status,
                )
                for rec in cached.recommendations
            ]
            return AIInsightResponse(
                lesson_id=lesson_id, insights=insights_list, recommendations=recs_list
            )

        # 2. Check student count reliability
        activities = await self.repository.get_activities_for_lesson(lesson_id)
        total_students = {act.student_enrollment_id for act in activities}
        student_count = len(total_students)

        if student_count < 30:
            raise AppException(
                message="Bài học chưa đủ độ tin cậy để sinh insight (tối thiểu 30 học viên).",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCode.LOW_DATA,
            )

        # 3. Calculate metrics for the prompt context
        completed_students = {
            act.student_enrollment_id for act in activities if act.is_completed
        }
        completion_rate = (
            len(completed_students) / student_count if student_count > 0 else 0.0
        )

        # Calculate drop-off rate specifically for this lesson
        # Get overall course activities
        course_activities = await self.repository.get_activities_for_course(course_id)
        student_max_order: dict[uuid.UUID, tuple[uuid.UUID, int]] = {}
        for sid, lid, oidx in course_activities:
            if sid not in student_max_order or oidx > student_max_order[sid][1]:
                student_max_order[sid] = (lid, oidx)

        stopped_count = sum(
            1 for sid, val in student_max_order.items() if val[0] == lesson_id
        )
        drop_off_rate = stopped_count / student_count if student_count > 0 else 0.0

        db_timeline = []
        if lesson.type == "video":
            db_timeline = await self.repository.get_video_timeline_analysis(lesson_id)

        # 4. Invoke ChatOpenAI via agent layer
        # (This implements task BE-006 & INT-002)
        llm_result = await generate_insight_via_llm(
            lesson_title=lesson.title,
            lesson_type=lesson.type,
            student_count=student_count,
            completion_rate=completion_rate,
            drop_off_rate=drop_off_rate,
            timeline=db_timeline,
        )

        # 5. Save to database
        new_insight = AiInsight(
            lesson_id=lesson_id,
            hypothesis=llm_result["hypothesis"],
            confidence_score=llm_result["confidence_score"],
            raw_prompt=llm_result.get("raw_prompt"),
            raw_response=llm_result.get("raw_response"),
            model_version=llm_result.get("model_version", "gpt-4o"),
        )

        recs = [
            Recommendation(suggestion_text=suggestion, status="pending")
            for suggestion in llm_result["suggestions"]
        ]
        new_insight.recommendations = recs

        await self.repository.save_ai_insight(new_insight)

        # 6. Map to response
        insights_list = [
            InsightDetail(
                insight_id=new_insight.id,
                hypothesis=new_insight.hypothesis,
                confidence_score=new_insight.confidence_score,
            )
        ]
        recs_list = [
            RecommendationDetail(
                recommendation_id=rec.id,
                suggestion_text=rec.suggestion_text,
                status=rec.status,
            )
            for rec in recs
        ]

        return AIInsightResponse(
            lesson_id=lesson_id, insights=insights_list, recommendations=recs_list
        )

    async def action_recommendation(
        self,
        course_id: uuid.UUID,
        lesson_id: uuid.UUID,
        recommendation_id: uuid.UUID,
        teacher_id: uuid.UUID,
        action: str,
    ) -> RecommendationActionResponse:
        """Record teacher action (applied/ignored) on an AI Recommendation."""
        await self._verify_course_ownership(course_id, teacher_id)

        rec = await self.repository.get_recommendation_by_id(
            course_id, lesson_id, recommendation_id
        )
        if not rec:
            raise AppException(
                message="Đề xuất không tồn tại",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )

        rec.status = action
        rec.actioned_at = datetime.now(timezone.utc)
        await self.repository.commit()

        return RecommendationActionResponse(
            recommendation_id=rec.id, status=rec.status, updated_at=rec.actioned_at
        )
