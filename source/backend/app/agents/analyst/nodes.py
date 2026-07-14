from typing import Dict, Any
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.config import settings
from app.agents.analyst.prompts import SYSTEM_ANALYST_PROMPT, REASON_PROMPT, RECOMMEND_PROMPT
from app.agents.tools.analytics_tools import fetch_lesson_stats_tool, fetch_video_timeline_tool


class ReasonOutput(BaseModel):
    """Pydantic model mapping the LLM's reason analysis output."""
    hypothesis: str = Field(description="Giả thuyết nguyên nhân học viên bỏ dở bài học")
    confidence_score: float = Field(description="Độ tin cậy của giả thuyết, float từ 0.0 đến 1.0")


class RecommendOutput(BaseModel):
    """Pydantic model mapping the LLM's recommendation suggestions output."""
    suggestions: list[str] = Field(description="Danh sách đề xuất hành động cải tiến nội dung, tối đa 3 đề xuất")


async def analyze_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node responsible for executing DB tools and loading statistical attributes into State."""
    db = state.get("db")
    course_id = state.get("course_id")
    lesson_id = state.get("lesson_id")

    if not db or not course_id or not lesson_id:
        # Fall back to state values passed directly (e.g. in test stubs)
        return {}

    stats = await fetch_lesson_stats_tool(db, course_id, lesson_id)
    if not stats:
        return {}

    timeline = []
    if stats["lesson_type"] == "video":
        db_timeline = await fetch_video_timeline_tool(db, lesson_id)
        timeline = [{"second": sec, "count": cnt} for sec, cnt in db_timeline]

    return {
        "lesson_title": stats["lesson_title"],
        "lesson_type": stats["lesson_type"],
        "student_count": stats["student_count"],
        "completion_rate": stats["completion_rate"],
        "drop_off_rate": stats["drop_off_rate"],
        "timeline": timeline
    }


async def reason_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node using ChatOpenAI to formulate a hypothesis based on stats state."""
    # Fallback/Mock mode for testing
    if settings.OPENAI_API_KEY == "sk-test-key" or settings.APP_ENV == "testing":
        return {
            "hypothesis": f"Giả thuyết tự động cho bài học '{state.get('lesson_title')}': Video có thời lượng quá dài khiến học viên giảm chú ý.",
            "confidence_score": 0.85
        }

    timeline_str = ""
    if state.get("timeline"):
        points = [f"+ Giây thứ {pt['second']}: có {pt['count']} học viên dừng video" for pt in state["timeline"]]
        timeline_str = "- Biểu đồ dòng thời gian mốc giây mà học viên bấm dừng video nhiều nhất:\n" + "\n".join(points)

    user_msg = REASON_PROMPT.format(
        lesson_title=state.get("lesson_title", "Unknown"),
        lesson_type=state.get("lesson_type", "Unknown"),
        student_count=state.get("student_count", 0),
        completion_rate_pct=state.get("completion_rate", 0.0) * 100,
        drop_off_rate_pct=state.get("drop_off_rate", 0.0) * 100,
        timeline_section=timeline_str
    )

    llm = ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0.2)
    structured_llm = llm.with_structured_output(ReasonOutput)

    messages = [
        {"role": "system", "content": SYSTEM_ANALYST_PROMPT},
        {"role": "user", "content": user_msg}
    ]
    result = await structured_llm.ainvoke(messages)
    return {
        "hypothesis": result.hypothesis,
        "confidence_score": result.confidence_score
    }


async def recommend_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node using ChatOpenAI to output 개선 recommendations based on hypothesis state."""
    # Fallback/Mock mode for testing
    if settings.OPENAI_API_KEY == "sk-test-key" or settings.APP_ENV == "testing":
        return {
            "suggestions": [
                "Chia nhỏ video bài giảng thành các phần dưới 5 phút.",
                "Bổ sung bài trắc nghiệm ngắn (Quiz) xen kẽ để tăng tương tác.",
                "Tối ưu lại phần giải thích ở phút thứ 4."
            ]
        }

    user_msg = RECOMMEND_PROMPT.format(hypothesis=state.get("hypothesis", ""))

    llm = ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0.2)
    structured_llm = llm.with_structured_output(RecommendOutput)

    messages = [
        {"role": "system", "content": SYSTEM_ANALYST_PROMPT},
        {"role": "user", "content": user_msg}
    ]
    result = await structured_llm.ainvoke(messages)
    return {
        "suggestions": result.suggestions
    }
