from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.config import settings


class AIInsightParsed(BaseModel):
    """Structured response schema for AI analysis of a lesson."""

    hypothesis: str = Field(
        description="Giả thuyết nguyên nhân học viên bỏ dở bài học (ví dụ: video quá dài, bài tập quá phức tạp, ...)"
    )
    confidence_score: float = Field(
        description="Độ tin cậy của giả thuyết, giá trị float trong khoảng từ 0.0 đến 1.0"
    )
    suggestions: list[str] = Field(
        description="Danh sách đề xuất hành động cải thiện bài học cụ thể, tối đa 3 đề xuất"
    )


async def generate_insight_via_llm(
    lesson_title: str,
    lesson_type: str,
    student_count: int,
    completion_rate: float,
    drop_off_rate: float,
    timeline: list[tuple[int, int]],
) -> dict[str, Any]:
    """
    Formulates a prompt with learning analytics and queries OpenAI GPT-4o
    to generate insights and actionable recommendations.
    """
    # 1. Fallback for testing environments
    if settings.OPENAI_API_KEY == "sk-test-key" or settings.APP_ENV == "testing":
        return {
            "hypothesis": f"Giả thuyết tự động cho bài học '{lesson_title}': Video có thời lượng quá dài khiến học viên giảm chú ý.",
            "confidence_score": 0.85,
            "suggestions": [
                "Chia nhỏ video bài giảng thành các phần dưới 5 phút.",
                "Bổ sung bài trắc nghiệm ngắn (Quiz) xen kẽ để tăng tương tác.",
                "Tối ưu lại phần giải thích ở phút thứ 4.",
            ],
            "raw_prompt": "Simulated prompt for testing",
            "raw_response": "Simulated response for testing",
            "model_version": "simulated-gpt-4o",
        }

    # 2. Build prompts
    system_message = (
        "Bạn là một chuyên gia giáo dục và phân tích dữ liệu học tập (Learning Analyst).\n"
        "Nhiệm vụ của bạn là phân tích dữ liệu thống kê của bài học để đưa ra giả thuyết logic tại sao học viên lại dừng học (drop-off) "
        "và đề xuất các giải pháp cải thiện cụ thể mà giáo viên có thể thực hiện trên Udemy."
    )

    user_message = (
        f"Thông tin bài học:\n"
        f"- Tiêu đề bài học: {lesson_title}\n"
        f"- Loại hình: {lesson_type}\n"
        f"- Số học viên đã tham gia học: {student_count}\n"
        f"- Tỷ lệ hoàn thành (Completion Rate): {completion_rate * 100:.2f}%\n"
        f"- Tỷ lệ bỏ học tại bài học này (Drop-off Rate): {drop_off_rate * 100:.2f}%\n"
    )

    if timeline:
        timeline_str = "\n".join(
            [f"+ Giây thứ {sec}: có {cnt} học viên tạm dừng" for sec, cnt in timeline]
        )
        user_message += f"- Biểu đồ dòng thời gian mốc giây mà học viên bấm dừng video nhiều nhất:\n{timeline_str}\n"

    user_message += (
        "\nHãy phân tích dữ liệu trên để đưa ra:\n"
        "1. Giả thuyết nguyên nhân cụ thể tại sao học viên dừng học.\n"
        "2. Điểm tin cậy (confidence score) cho giả thuyết đó (từ 0.0 đến 1.0).\n"
        "3. Tối đa 3 đề xuất hành động cải thiện nội dung trực tiếp trên Udemy.\n"
    )

    # 3. Invoke OpenAI via LangChain with structured output
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0.2
    )

    structured_llm = llm.with_structured_output(AIInsightParsed)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message),
    ]

    result = await structured_llm.ainvoke(messages)

    raw_prompt = f"SYSTEM:\n{system_message}\n\nUSER:\n{user_message}"
    raw_response = result.model_dump_json()

    return {
        "hypothesis": result.hypothesis,
        "confidence_score": result.confidence_score,
        "suggestions": result.suggestions,
        "raw_prompt": raw_prompt,
        "raw_response": raw_response,
        "model_version": settings.OPENAI_MODEL,
    }
