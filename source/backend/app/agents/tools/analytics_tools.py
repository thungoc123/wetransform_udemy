import uuid
from typing import List, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.analytics.repository import AnalyticsRepository


async def fetch_lesson_stats_tool(db: AsyncSession, course_id: uuid.UUID, lesson_id: uuid.UUID) -> Dict[str, Any]:
    """
    Fetch student count, completion rate, and drop-off rate for a specific lesson in a course.
    """
    repo = AnalyticsRepository(db)
    lesson = await repo.get_lesson_by_id(course_id, lesson_id)
    if not lesson:
        return {}

    activities = await repo.get_activities_for_lesson(lesson_id)
    total_students = {act.student_enrollment_id for act in activities}
    student_count = len(total_students)

    completed_students = {act.student_enrollment_id for act in activities if act.is_completed}
    completion_rate = len(completed_students) / student_count if student_count > 0 else 0.0

    course_activities = await repo.get_activities_for_course(course_id)
    student_max_order = {}
    for sid, lid, oidx in course_activities:
        if sid not in student_max_order or oidx > student_max_order[sid][1]:
            student_max_order[sid] = (lid, oidx)

    stopped_count = sum(1 for sid, val in student_max_order.items() if val[0] == lesson_id)
    drop_off_rate = stopped_count / student_count if student_count > 0 else 0.0

    return {
        "lesson_title": lesson.title,
        "lesson_type": lesson.type,
        "student_count": student_count,
        "completion_rate": completion_rate,
        "drop_off_rate": drop_off_rate
    }


async def fetch_video_timeline_tool(db: AsyncSession, lesson_id: uuid.UUID) -> List[Tuple[int, int]]:
    """
    Fetch video pauses timeline points for a specific video lesson.
    """
    repo = AnalyticsRepository(db)
    return await repo.get_video_timeline_analysis(lesson_id)
