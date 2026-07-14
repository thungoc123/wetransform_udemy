import uuid
from typing import List, Tuple, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.analyst.agent import create_analyst_agent


class AIInsightParsed(BaseModel):
    """Structured response schema for AI analysis of a lesson."""
    hypothesis: str = Field(
        description="Giả thuyết nguyên nhân học viên bỏ dở bài học (ví dụ: video quá dài, bài tập quá phức tạp, ...)"
    )
    confidence_score: float = Field(
        description="Độ tin cậy của giả thuyết, giá trị float trong khoảng từ 0.0 đến 1.0"
    )
    suggestions: List[str] = Field(
        description="Danh sách đề xuất hành động cải thiện bài học cụ thể, tối đa 3 đề xuất"
    )


async def generate_insight_via_llm(
    lesson_title: str,
    lesson_type: str,
    student_count: int,
    completion_rate: float,
    drop_off_rate: float,
    timeline: List[Tuple[int, int]],
    course_id: uuid.UUID = None,
    lesson_id: uuid.UUID = None,
    db: AsyncSession = None
) -> Dict[str, Any]:
    """
    Orchestrates the multi-step State Graph agent to analyze learning data,
    formulate a hypothesis, and suggest improvements.
    """
    # 1. Instantiate the LangGraph agent
    agent = create_analyst_agent()

    # 2. Compile inputs into Graph State
    state_timeline = []
    if timeline:
        state_timeline = [{"second": sec, "count": cnt} for sec, cnt in timeline]

    state = {
        "db": db,
        "course_id": course_id,
        "lesson_id": lesson_id,
        "lesson_title": lesson_title,
        "lesson_type": lesson_type,
        "student_count": student_count,
        "completion_rate": completion_rate,
        "drop_off_rate": drop_off_rate,
        "timeline": state_timeline,
        "hypothesis": None,
        "confidence_score": None,
        "suggestions": None
    }

    # 3. Invoke State Graph execution (analyze -> reason -> recommend -> END)
    result = await agent.ainvoke(state)

    # 4. Format return dict structure compatible with analytics service expectations
    return {
        "hypothesis": result.get("hypothesis", ""),
        "confidence_score": result.get("confidence_score", 0.0),
        "suggestions": result.get("suggestions", []),
        "raw_prompt": "LangGraph multi-step graph: analyze -> reason -> recommend",
        "raw_response": "LangGraph StateGraph run successful",
        "model_version": "LangGraph (gpt-4o)"
    }
