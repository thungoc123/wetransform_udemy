import uuid
from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class DashboardResponse(CamelModel):
    course_id: uuid.UUID
    completion_rate: float
    drop_off_rate: float
    active_students: int
    inactive_students: int
    at_risk_students: int


class TimelinePoint(CamelModel):
    second: int
    count: int


class LessonDropOff(CamelModel):
    lesson_id: uuid.UUID
    lesson_title: str
    type: str
    drop_off_rate: Optional[float] = None
    has_warning: bool
    timeline_analysis: Optional[List[TimelinePoint]] = None


class ModuleDropOff(CamelModel):
    module_id: uuid.UUID
    module_title: str
    lessons: List[LessonDropOff]


class DropOffResponse(CamelModel):
    modules: List[ModuleDropOff]


class EngagementMetrics(CamelModel):
    student_count: int
    completion_rate: float
    average_duration_seconds: float


class LessonAnalyticsResponse(CamelModel):
    lesson_id: uuid.UUID
    lesson_title: str
    type: str
    engagement_metrics: EngagementMetrics
    timeline_analysis: Optional[List[TimelinePoint]] = None
    reliability_message: Optional[str] = None


class InsightDetail(CamelModel):
    insight_id: uuid.UUID
    hypothesis: str
    confidence_score: float


class RecommendationDetail(CamelModel):
    recommendation_id: uuid.UUID
    suggestion_text: str
    status: str


class AIInsightResponse(CamelModel):
    lesson_id: uuid.UUID
    insights: List[InsightDetail]
    recommendations: List[RecommendationDetail]
    disclaimer_text: str = "AI chỉ mang tính chất tham khảo. Quyết định cuối cùng thuộc về giáo viên."


class RecommendationActionRequest(CamelModel):
    action: str

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        if v not in ("applied", "ignored"):
            raise ValueError("action must be 'applied' or 'ignored'")
        return v


class RecommendationActionResponse(CamelModel):
    recommendation_id: uuid.UUID
    status: str
    updated_at: datetime
