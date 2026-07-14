import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.agents.workflows.insight_workflow import AIInsightParsed
from app.database import Base
from app.models.course import Course
from app.models.teacher import Teacher
from app.shared.security import hash_password
from app.worker import celery_app
from tests.conftest import TestingSessionLocal, engine

# Configure celery
celery_app.conf.task_always_eager = False
celery_app.conf.task_eager_propagates = False


@pytest.fixture(autouse=True)
async def setup_db():
    """Recreate all tables for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
async def db_session():
    """Provide a database session with expire_on_commit=False."""
    async with TestingSessionLocal(expire_on_commit=False) as session:
        yield session


@pytest.fixture
async def test_teacher(db_session):
    """Seed test data for a teacher."""
    teacher = Teacher(
        name="E2E Teacher",
        email="test_e2e@example.com",
        password_hash=hash_password("Password123!"),
    )
    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)
    return teacher


@pytest.mark.asyncio
async def test_e2e_user_flow(client: AsyncClient, test_teacher: Teacher, db_session):
    """
    Test End-to-End flow:
    1. Login
    2. Upload CSV Data (trigger Celery tasks synchronously)
    3. Get Course Dashboard
    4. View Drop-off Analysis
    5. Trigger AI Insights for a Drop-off Lesson
    6. Identify At-Risk Students and Send Reminders
    """

    # 1. Login
    login_payload = {"email": test_teacher.email, "password": "Password123!"}
    login_response = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    res_json = login_response.json()
    token = res_json["data"]["token"] if "data" in res_json else res_json["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload CSV Data (with 35 students to bypass AI Insight 30 student limit)
    csv_lines = ["Course Name,Item Name,Item Type,User Name,% Completed"]
    for i in range(35):
        csv_lines.append(f"E2E Course,Lesson 1,video,Student_{i},1.0")
        csv_lines.append(f"E2E Course,Lesson 2,video,Student_{i},0.5")
        csv_lines.append(f"E2E Course,Lesson 3,video,Student_{i},0.1")

    csv_content = "\n".join(csv_lines) + "\n"
    csv_path = "/tmp/e2e_test_data.csv"
    with open(csv_path, "w") as f:
        f.write(csv_content)

    with (
        patch("app.modules.data_source.service.process_import_master_task.delay"),
        open(csv_path, "rb") as f,
    ):
        upload_response = await client.post(
            "/api/v1/data/upload",
            headers=headers,
            files={"file": ("e2e_test_data.csv", f, "text/csv")},
        )
    assert upload_response.status_code == 200

    # Manually execute the import logic to bypass asyncio.run conflict
    import pandas as pd

    from app.modules.data_source.tasks import _create_courses_and_lessons, _upsert_chunk

    with patch(
        "app.modules.data_source.tasks.async_session_maker",
        return_value=TestingSessionLocal(),
    ):
        await _create_courses_and_lessons(csv_path, test_teacher.id)  # type: ignore
        chunk_data = pd.read_csv(csv_path).to_dict(orient="records")
        await _upsert_chunk(chunk_data, test_teacher.id)  # type: ignore

    # Wait, getting course id
    async with TestingSessionLocal(expire_on_commit=False) as session:
        stmt = select(Course).where(Course.title == "E2E Course")
        result = await session.execute(stmt)
        course = result.scalar_one()
        course_id = course.id

        # Manually update last_activity_at so they appear as at-risk
        from app.models.activity import StudentEnrollment

        stmt_e = select(StudentEnrollment).where(
            StudentEnrollment.course_id == course_id
        )
        res_e = await session.execute(stmt_e)
        for e in res_e.scalars().all():
            e.last_activity_at = datetime.now(timezone.utc) - timedelta(days=15)  # type: ignore
        await session.commit()

    # 3. Get Dashboard
    dashboard_response = await client.get(
        f"/api/v1/courses/{course_id}/dashboard", headers=headers
    )
    assert dashboard_response.status_code == 200
    assert "courseId" in dashboard_response.json().get(
        "data", dashboard_response.json()
    )

    # 4. View Drop-off Analysis
    drop_off_response = await client.get(
        f"/api/v1/courses/{course_id}/drop-off-analysis", headers=headers
    )
    assert drop_off_response.status_code == 200
    drop_off_data = drop_off_response.json().get("data", drop_off_response.json())

    # Find a lesson with high drop-off
    lesson_id = drop_off_data["modules"][0]["lessons"][0]["lessonId"]

    # 5. Trigger AI Insights for a Drop-off Lesson
    mock_insight = AIInsightParsed(
        hypothesis="Students stop because of the long video.",
        confidence_score=0.85,
        suggestions=["Add a quiz", "Simplify terminology"],
    )

    with patch(
        "app.modules.analytics.service.generate_insight_via_llm"
    ) as mock_generate:
        mock_generate.return_value = {
            "hypothesis": mock_insight.hypothesis,
            "confidence_score": mock_insight.confidence_score,
            "suggestions": mock_insight.suggestions,
            "raw_prompt": "mock",
            "raw_response": "mock",
            "model_version": "mock",
        }

        insights_response = await client.get(
            f"/api/v1/courses/{course_id}/lessons/{lesson_id}/ai-insights",
            headers=headers,
        )
        assert insights_response.status_code == 200, insights_response.text
        insights_data = insights_response.json().get("data", insights_response.json())
        assert len(insights_data["insights"]) > 0
        assert insights_data["insights"][0]["hypothesis"] == mock_insight.hypothesis

    # 6. Identify At-Risk Students and Send Reminders
    at_risk_response = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson_id}/at-risk-students",
        headers=headers,
    )
    assert at_risk_response.status_code == 200
    at_risk_data = at_risk_response.json().get("data", at_risk_response.json())

    # Might be empty if no one stopped exactly at this lesson, but the endpoint should return successfully
    if at_risk_data.get("students"):
        student_to_remind = at_risk_data["students"][0]["student_id"]

        # Send Reminder
        reminder_payload = {
            "student_ids": [student_to_remind],
            "message_body": at_risk_data.get("default_message_template", "Hello"),
        }
        reminder_response = await client.post(
            f"/api/v1/courses/{course_id}/lessons/{lesson_id}/send-reminder",
            headers=headers,
            json=reminder_payload,
        )
        assert reminder_response.status_code == 200

    # Clean up
    if os.path.exists(csv_path):
        os.remove(csv_path)
