from typing import Dict, Any, TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from app.agents.analyst.nodes import analyze_node, reason_node, recommend_node


class AnalystState(TypedDict):
    """LangGraph agent state declaration for Analyst workflow."""
    db: Any
    course_id: Any
    lesson_id: Any
    lesson_title: Optional[str]
    lesson_type: Optional[str]
    student_count: Optional[int]
    completion_rate: Optional[float]
    drop_off_rate: Optional[float]
    timeline: Optional[List[Dict[str, Any]]]
    hypothesis: Optional[str]
    confidence_score: Optional[float]
    suggestions: Optional[List[str]]


def create_analyst_agent():
    """Compiles the analyst agent state graph workflow."""
    workflow = StateGraph(AnalystState)

    # 1. Register nodes
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("reason", reason_node)
    workflow.add_node("recommend", recommend_node)

    # 2. Set entry point
    workflow.set_entry_point("analyze")

    # 3. Add edges (analyze -> reason -> recommend -> END)
    workflow.add_edge("analyze", "reason")
    workflow.add_edge("reason", "recommend")
    workflow.add_edge("recommend", END)

    return workflow.compile()
