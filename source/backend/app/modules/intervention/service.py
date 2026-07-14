import uuid
from datetime import datetime, timedelta, timezone

from fastapi import status

from app.modules.intervention.repository import InterventionRepository
from app.modules.intervention.schemas import (
    AtRiskStudentsResponse,
    SendReminderResponse,
    StudentAtRisk,
)
from app.modules.intervention.tasks import send_reminder_email_task
from app.modules.intervention.template_builder import build_default_template
from app.shared.error_codes import ErrorCode
from app.shared.exceptions import AppException


class InterventionService:
    def __init__(self, repository: InterventionRepository):
        self.repository = repository

    async def _verify_course_ownership(
        self, course_id: uuid.UUID, teacher_id: uuid.UUID
    ) -> None:
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

    async def get_at_risk_students(
        self,
        course_id: uuid.UUID,
        lesson_id: uuid.UUID,
        teacher_id: uuid.UUID,
        now: datetime | None = None,
    ) -> AtRiskStudentsResponse:
        if now is None:
            now = datetime.now(timezone.utc)

        await self._verify_course_ownership(course_id, teacher_id)

        lesson = await self.repository.get_lesson_by_id(course_id, lesson_id)
        if not lesson:
            raise AppException(
                message="Bài học không tồn tại",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )

        enrollments = await self.repository.get_students_stopped_at_lesson(
            course_id, lesson_id
        )

        # Filter out those who are inactive for > 14 days
        at_risk_enrollments = []
        for e in enrollments:
            last_act = e.last_activity_at
            if last_act:
                if last_act.tzinfo is None:
                    last_act = last_act.replace(tzinfo=timezone.utc)
                diff = now - last_act
                if diff.days >= 14:
                    at_risk_enrollments.append((e, diff.days))
            else:
                # If no activity at all but enrolled, they are inactive.
                # We could set a dummy value or diff from created_at
                created = e.created_at
                if created and created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
                diff = now - created if created else timedelta(days=0)
                if diff.days >= 14:
                    at_risk_enrollments.append((e, diff.days))

        enrollment_ids = [e.id for e, _ in at_risk_enrollments]  # type: ignore

        # Check reminders in the last 7 days
        seven_days_ago = now - timedelta(days=7)
        recent_reminders = await self.repository.get_recent_reminders(lesson_id, enrollment_ids, seven_days_ago)  # type: ignore

        recently_reminded_eids = {r.student_enrollment_id for r in recent_reminders}

        students_response = []
        for e, days_inactive in at_risk_enrollments:
            can_send = e.id not in recently_reminded_eids
            students_response.append(
                StudentAtRisk(
                    student_id=e.udemy_student_id,  # type: ignore
                    masked_name=e.masked_name,  # type: ignore
                    days_inactive=days_inactive,
                    can_send_reminder=can_send,
                )
            )

        default_template = build_default_template(lesson.title)  # type: ignore

        return AtRiskStudentsResponse(
            lesson_id=lesson_id,
            default_message_template=default_template,
            students=students_response,
        )

    async def trigger_send_reminders(
        self,
        course_id: uuid.UUID,
        lesson_id: uuid.UUID,
        teacher_id: uuid.UUID,
        student_ids: list[str],
        message_body: str,
        now: datetime | None = None,
    ) -> SendReminderResponse:
        if now is None:
            now = datetime.now(timezone.utc)

        await self._verify_course_ownership(course_id, teacher_id)

        lesson = await self.repository.get_lesson_by_id(course_id, lesson_id)
        if not lesson:
            raise AppException(
                message="Bài học không tồn tại",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCode.NOT_FOUND,
            )

        enrollments = await self.repository.get_students_stopped_at_lesson(
            course_id, lesson_id
        )

        enrollment_map = {e.udemy_student_id: e for e in enrollments}
        failures = []

        seven_days_ago = now - timedelta(days=7)
        all_eids = [e.id for e in enrollments if e.udemy_student_id in student_ids]  # type: ignore
        recent_reminders = await self.repository.get_recent_reminders(lesson_id, all_eids, seven_days_ago)  # type: ignore
        recently_reminded_eids = {r.student_enrollment_id for r in recent_reminders}

        valid_student_ids = []

        for sid in student_ids:
            if sid not in enrollment_map:
                failures.append(
                    {
                        "student_id": sid,
                        "reason": "Student not found or not at risk for this lesson",
                    }
                )
                continue
            e = enrollment_map[sid]
            if e.id in recently_reminded_eids:
                failures.append(
                    {
                        "student_id": sid,
                        "reason": "Student has already received a reminder in the last 7 days",
                    }
                )
                continue

            valid_student_ids.append(sid)

        if valid_student_ids:
            send_reminder_email_task.delay(
                str(course_id),
                str(lesson_id),
                str(teacher_id),
                valid_student_ids,
                message_body,
            )  # type: ignore

        if not valid_student_ids and not failures:
            raise AppException(
                message="Danh sách học viên không hợp lệ.",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCode.VALIDATION_ERROR,
            )

        return SendReminderResponse(
            sent_count=len(valid_student_ids),
            failed_count=len(failures),
            failures=failures,  # type: ignore
        )
