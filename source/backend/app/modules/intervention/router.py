import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teacher import Teacher
from app.modules.intervention.repository import InterventionRepository
from app.modules.intervention.schemas import (
    AtRiskStudentsResponse,
    SendReminderRequest,
    SendReminderResponse,
)
from app.modules.intervention.service import InterventionService
from app.shared.dependencies.auth import get_current_teacher
from app.shared.dependencies.database import get_db

router = APIRouter(prefix="/api/v1/courses", tags=["Intervention"])


def get_intervention_service(db: AsyncSession = Depends(get_db)) -> InterventionService:
    repository = InterventionRepository(db)
    return InterventionService(repository)


@router.get(
    "/{course_id}/lessons/{lesson_id}/at-risk-students",
    response_model=AtRiskStudentsResponse,
)
async def get_at_risk_students(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    service: InterventionService = Depends(get_intervention_service),
    teacher: Teacher = Depends(get_current_teacher),
):
    """
    Retrieve a list of at-risk students for a specific lesson,
    along with a default message template to send them.
    """
    return await service.get_at_risk_students(course_id, lesson_id, teacher.id)  # type: ignore


@router.post(
    "/{course_id}/lessons/{lesson_id}/send-reminder",
    response_model=SendReminderResponse,
)
async def send_reminder(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    request: SendReminderRequest,
    service: InterventionService = Depends(get_intervention_service),
    teacher: Teacher = Depends(get_current_teacher),
):
    """
    Send a reminder email to a selected list of at-risk students.
    """
    return await service.trigger_send_reminders(
        course_id, lesson_id, teacher.id, request.student_ids, request.message_body  # type: ignore
    )
