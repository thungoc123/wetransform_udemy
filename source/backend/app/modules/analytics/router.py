import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teacher import Teacher
from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.schemas import (
    AIInsightResponse,
    DashboardResponse,
    DropOffResponse,
    LessonAnalyticsResponse,
    RecommendationActionRequest,
    RecommendationActionResponse,
)
from app.modules.analytics.service import AnalyticsService
from app.shared.dependencies.auth import get_current_teacher
from app.shared.dependencies.database import get_db
from app.shared.response import StandardResponse

router = APIRouter(prefix="/api/v1/courses", tags=["Analytics"])


def get_analytics_service(db: AsyncSession = Depends(get_db)) -> AnalyticsService:
    """Dependency provider for AnalyticsService."""
    repo = AnalyticsRepository(db)
    return AnalyticsService(repo)


@router.get(
    "/{course_id}/dashboard",
    summary="Get Course Dashboard Overview",
    description="Lấy dữ liệu tổng quan của một khóa học (completion rate, drop-off rate, active/inactive/at-risk students)",
    response_model=StandardResponse[DashboardResponse],
    responses={
        403: {"description": "Giáo viên không sở hữu khóa học này"},
        404: {"description": "Khóa học không tồn tại"},
    },
)
async def get_dashboard(
    course_id: uuid.UUID,
    teacher: Teacher = Depends(get_current_teacher),
    service: AnalyticsService = Depends(get_analytics_service),
) -> StandardResponse[DashboardResponse]:
    data = await service.get_dashboard(course_id=course_id, teacher_id=teacher.id)
    return StandardResponse(success=True, message="Success", data=data)


@router.get(
    "/{course_id}/drop-off-analysis",
    summary="Get Drop-off Point Analysis",
    description="Trả về phân tích phễu drop-off theo các bài học và mốc dừng video nếu có.",
    response_model=StandardResponse[DropOffResponse],
    responses={
        403: {"description": "Giáo viên không sở hữu khóa học này"},
        404: {"description": "Khóa học không tồn tại"},
    },
)
async def get_drop_off_analysis(
    course_id: uuid.UUID,
    threshold: float = Query(
        0.20, description="Ngưỡng cảnh báo drop-off, mặc định 20%"
    ),
    teacher: Teacher = Depends(get_current_teacher),
    service: AnalyticsService = Depends(get_analytics_service),
) -> StandardResponse[DropOffResponse]:
    data = await service.get_drop_off_analysis(
        course_id=course_id, teacher_id=teacher.id, threshold=threshold
    )
    return StandardResponse(success=True, message="Success", data=data)


@router.get(
    "/{course_id}/lessons/{lesson_id}/analytics",
    summary="Get Lesson Analytics Detail",
    description="Lấy dữ liệu thống kê chi tiết cho một bài học (engagement metrics, timeline analysis).",
    response_model=StandardResponse[LessonAnalyticsResponse],
    responses={
        403: {"description": "Giáo viên không sở hữu khóa học này"},
        404: {"description": "Bài học hoặc khóa học không tồn tại"},
    },
)
async def get_lesson_analytics(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    teacher: Teacher = Depends(get_current_teacher),
    service: AnalyticsService = Depends(get_analytics_service),
) -> StandardResponse[LessonAnalyticsResponse]:
    data = await service.get_lesson_analytics(
        course_id=course_id, lesson_id=lesson_id, teacher_id=teacher.id
    )
    return StandardResponse(success=True, message="Success", data=data)


@router.get(
    "/{course_id}/lessons/{lesson_id}/ai-insights",
    summary="Get AI Insights for Lesson",
    description="Lấy hoặc sinh gợi ý phân tích nguyên nhân và giải pháp từ AI ChatOpenAI.",
    response_model=StandardResponse[AIInsightResponse],
    responses={
        400: {"description": "Bài học chưa đủ độ tin cậy để sinh insight (LOW_DATA)"},
        403: {"description": "Giáo viên không sở hữu khóa học này"},
        404: {"description": "Bài học hoặc khóa học không tồn tại"},
    },
)
async def get_ai_insights(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    teacher: Teacher = Depends(get_current_teacher),
    service: AnalyticsService = Depends(get_analytics_service),
) -> StandardResponse[AIInsightResponse]:
    data = await service.get_ai_insights(
        course_id=course_id, lesson_id=lesson_id, teacher_id=teacher.id
    )
    return StandardResponse(success=True, message="Success", data=data)


@router.post(
    "/{course_id}/lessons/{lesson_id}/recommendations/{recommendation_id}/action",
    summary="Update Recommendation Status",
    description="Ghi nhận phản hồi hành động (applied/ignored) của giáo viên đối với đề xuất của AI.",
    response_model=StandardResponse[RecommendationActionResponse],
    responses={
        400: {"description": "Yêu cầu không hợp lệ"},
        403: {"description": "Giáo viên không sở hữu khóa học này"},
        404: {"description": "Đề xuất không tồn tại"},
    },
)
async def action_recommendation(
    course_id: uuid.UUID,
    lesson_id: uuid.UUID,
    recommendation_id: uuid.UUID,
    body: RecommendationActionRequest,
    teacher: Teacher = Depends(get_current_teacher),
    service: AnalyticsService = Depends(get_analytics_service),
) -> StandardResponse[RecommendationActionResponse]:
    data = await service.action_recommendation(
        course_id=course_id,
        lesson_id=lesson_id,
        recommendation_id=recommendation_id,
        teacher_id=teacher.id,
        action=body.action,
    )
    return StandardResponse(success=True, message="Success", data=data)
