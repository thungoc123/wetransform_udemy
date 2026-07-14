import pytest
from app.agents.analyst.agent import create_analyst_agent


@pytest.mark.asyncio
async def test_analyst_agent_graph():
    """
    Test compiling and invoking the analyst agent State Graph
    to verify node traversal and state updates.
    """
    # 1. Instantiate the graph
    agent = create_analyst_agent()
    assert agent is not None

    # 2. Invoke graph with mock input state
    state = {
        "db": None,
        "course_id": None,
        "lesson_id": None,
        "lesson_title": "Lesson 1: Introduction",
        "lesson_type": "video",
        "student_count": 50,
        "completion_rate": 0.6,
        "drop_off_rate": 0.4,
        "timeline": [{"second": 120, "count": 15}]
    }

    result = await agent.ainvoke(state)

    # 3. Assert correct output states
    assert "hypothesis" in result
    assert "confidence_score" in result
    assert "suggestions" in result

    assert result["hypothesis"] == "Giả thuyết tự động cho bài học 'Lesson 1: Introduction': Video có thời lượng quá dài khiến học viên giảm chú ý."
    assert result["confidence_score"] == 0.85
    assert len(result["suggestions"]) == 3
    assert result["suggestions"][0] == "Chia nhỏ video bài giảng thành các phần dưới 5 phút."
