import pytest
from app.agents.workflows.insight_workflow import generate_insight_via_llm


@pytest.mark.asyncio
async def test_generate_insight_via_workflow():
    """
    Verify the workflow wrapper correctly instantiates the LangGraph
    agent and returns the expected structured dictionary formats.
    """
    result = await generate_insight_via_llm(
        lesson_title="Test Lesson",
        lesson_type="video",
        student_count=40,
        completion_rate=0.7,
        drop_off_rate=0.3,
        timeline=[(120, 10)]
    )

    assert "hypothesis" in result
    assert "confidence_score" in result
    assert "suggestions" in result

    assert "Test Lesson" in result["hypothesis"]
    assert result["confidence_score"] == 0.85
    assert len(result["suggestions"]) == 3
