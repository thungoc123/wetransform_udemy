import asyncio
import uuid
from datetime import datetime, timezone

import structlog
from celery import shared_task
from sqlalchemy import select

from app.database import async_session_maker
from app.models.activity import StudentEnrollment
from app.models.ai_intervention import ReminderLog

logger = structlog.get_logger(__name__)


async def _mock_send_email_and_log(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    teacher_id: uuid.UUID,
    student_ids: list[str],
    message_body: str,
):
    async with async_session_maker() as session:
        # Get enrollments to map student_id to enrollment_id and name
        stmt = select(StudentEnrollment).where(
            StudentEnrollment.student_id.in_(student_ids),
            StudentEnrollment.course_id == course_id,
        )
        result = await session.execute(stmt)
        enrollments = result.scalars().all()

        for enrollment in enrollments:
            # Mock sending email
            personalized_msg = message_body.replace(
                "{student_name}", str(enrollment.masked_name)
            )
            personalized_msg = personalized_msg.replace(
                "{best_practice_tip}",
                "Hãy dành ra 15 phút mỗi ngày để xem lại kiến thức nhé!",
            )

            logger.info(
                "Mock sending email",
                student_id=enrollment.student_id,
                masked_name=enrollment.masked_name,
                message=personalized_msg,
            )

            # Log to database
            reminder_log = ReminderLog(
                student_enrollment_id=enrollment.id,
                lesson_id=lesson_id,
                teacher_id=teacher_id,
                message_body=personalized_msg,
                status="sent",
                sent_at=datetime.now(timezone.utc),
            )
            session.add(reminder_log)

        await session.commit()


@shared_task(name="app.modules.intervention.tasks.send_reminder_email_task")
def send_reminder_email_task(
    course_id_str: str,
    lesson_id_str: str,
    teacher_id_str: str,
    student_ids: list[str],
    message_body: str,
):
    """
    Asynchronously sends reminder emails to students and logs them.
    In the MVP, this mocks the sending by logging to console.
    """
    logger.info(f"Starting to send reminders to {len(student_ids)} students")

    course_id = uuid.UUID(course_id_str)
    lesson_id = uuid.UUID(lesson_id_str)
    teacher_id = uuid.UUID(teacher_id_str)

    asyncio.run(
        _mock_send_email_and_log(
            course_id, lesson_id, teacher_id, student_ids, message_body
        )
    )

    return len(student_ids)
