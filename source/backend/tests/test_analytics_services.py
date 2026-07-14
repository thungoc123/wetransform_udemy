import pytest
import uuid
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from sqlalchemy import select

from app.database import Base
from tests.conftest import engine, TestingSessionLocal
from app.models.teacher import Teacher
from app.models.course import Course, Module, Lesson
from app.models.activity import StudentEnrollment, LearningActivity
from app.models.ai_intervention import AiInsight, Recommendation
from app.shared.security import hash_password, create_access_token


@pytest.fixture(autouse=True)
async def setup_db():
    """Recreate all tables for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    """Provide a database session with expire_on_commit=False."""
    async with TestingSessionLocal(expire_on_commit=False) as session:
        yield session


@pytest.fixture
async def test_data(db_session):
    """Seed test data for a teacher, course, modules, lessons, and students."""
    # 1. Create Teacher
    teacher = Teacher(
        email="teacher@test.com",
        password_hash=hash_password("password"),
        name="Test Teacher"
    )
    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

    # 2. Create Course
    course = Course(
        teacher_id=teacher.id,
        title="Python testing course",
        student_count=35,
        status="imported"
    )
    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    # 3. Create Module
    module = Module(
        course_id=course.id,
        title="Module 1: Introduction",
        order_index=1
    )
    db_session.add(module)
    await db_session.commit()
    await db_session.refresh(module)

    # 4. Create Lessons
    lesson1 = Lesson(
        course_id=course.id,
        module_id=module.id,
        title="Lesson 1: Installation",
        type="video",
        order_index=1,
        duration_seconds=600,
        student_count=35
    )
    lesson2 = Lesson(
        course_id=course.id,
        module_id=module.id,
        title="Lesson 2: Variables",
        type="video",
        order_index=2,
        duration_seconds=500,
        student_count=25
    )
    lesson3 = Lesson(
        course_id=course.id,
        module_id=module.id,
        title="Lesson 3: Functions",
        type="quiz",
        order_index=3,
        student_count=5
    )
    db_session.add_all([lesson1, lesson2, lesson3])
    await db_session.commit()
    await db_session.refresh(lesson1)
    await db_session.refresh(lesson2)
    await db_session.refresh(lesson3)

    # 5. Create 35 Students and their learning activities
    now = datetime.now(timezone.utc)
    enrollments = []
    
    # 15 active students (last activity <= 7 days ago)
    for i in range(15):
        student = StudentEnrollment(
            course_id=course.id,
            udemy_student_id=f"stud_{i}",
            masked_name=f"Stu*** {i}",
            status="active",
            last_activity_at=now - timedelta(days=2),
            progress_percent=100.0  # Finished course
        )
        enrollments.append(student)

    # 5 at-risk students (last activity between 14 and 29 days ago)
    for i in range(15, 20):
        student = StudentEnrollment(
            course_id=course.id,
            udemy_student_id=f"stud_{i}",
            masked_name=f"Stu*** {i}",
            status="at_risk",
            last_activity_at=now - timedelta(days=20),
            progress_percent=33.33  # Stopped after lesson 1
        )
        enrollments.append(student)

    # 15 inactive students (last activity >= 30 days ago)
    for i in range(20, 35):
        student = StudentEnrollment(
            course_id=course.id,
            udemy_student_id=f"stud_{i}",
            masked_name=f"Stu*** {i}",
            status="inactive",
            last_activity_at=now - timedelta(days=35),
            progress_percent=66.67  # Stopped after lesson 2
        )
        enrollments.append(student)

    db_session.add_all(enrollments)
    await db_session.commit()

    for enrollment in enrollments:
        await db_session.refresh(enrollment)

    # Add learning activities
    activities = []
    # All 35 students started lesson 1
    for enrollment in enrollments:
        act = LearningActivity(
            student_enrollment_id=enrollment.id,
            lesson_id=lesson1.id,
            activity_type="video",
            started_at=now - timedelta(days=40),
            ended_at=now - timedelta(days=40),
            duration_seconds=500,
            is_completed=True
        )
        activities.append(act)

    # 30 students (15 active + 15 inactive) went on to start lesson 2
    # 5 at-risk students stopped at lesson 1
    for enrollment in enrollments[0:15] + enrollments[20:35]:
        act = LearningActivity(
            student_enrollment_id=enrollment.id,
            lesson_id=lesson2.id,
            activity_type="video",
            started_at=now - timedelta(days=35),
            ended_at=now - timedelta(days=35),
            duration_seconds=400,
            video_stop_at_second=120 if enrollment.id.int % 2 == 0 else 240,
            is_completed=True
        )
        activities.append(act)

    # Only 10 active students studied lesson 3
    # 5 active students and 15 inactive students stopped at lesson 2
    for enrollment in enrollments[0:10]:
        act = LearningActivity(
            student_enrollment_id=enrollment.id,
            lesson_id=lesson3.id,
            activity_type="quiz",
            started_at=now - timedelta(days=2),
            ended_at=now - timedelta(days=2),
            is_completed=True
        )
        activities.append(act)

    db_session.add_all(activities)
    await db_session.commit()

    token = create_access_token(teacher.id)
    headers = {"Authorization": f"Bearer {token}"}

    return {
        "teacher": teacher,
        "course": course,
        "module": module,
        "lesson1": lesson1,
        "lesson2": lesson2,
        "lesson3": lesson3,
        "headers": headers
    }


@pytest.mark.asyncio
async def test_dashboard_metrics(client: AsyncClient, test_data: dict):
    """Test GET /api/v1/courses/{courseId}/dashboard."""
    course_id = test_data["course"].id
    headers = test_data["headers"]

    response = await client.get(f"/api/v1/courses/{course_id}/dashboard", headers=headers)
    assert response.status_code == 200
    
    res_data = response.json()
    assert res_data["success"] is True
    
    dashboard = res_data["data"]
    assert dashboard["activeStudents"] == 15
    assert dashboard["atRiskStudents"] == 5
    assert dashboard["inactiveStudents"] == 15
    assert dashboard["dropOffRate"] == round(20 / 35, 4)  # (15 + 5) / 35
    expected_completion = (15*1.0 + 5*0.3333 + 15*0.6667) / 35
    assert abs(dashboard["completionRate"] - expected_completion) < 0.01


@pytest.mark.asyncio
async def test_drop_off_analysis(client: AsyncClient, test_data: dict):
    """Test GET /api/v1/courses/{courseId}/drop-off-analysis."""
    course_id = test_data["course"].id
    headers = test_data["headers"]

    response = await client.get(f"/api/v1/courses/{course_id}/drop-off-analysis", headers=headers)
    assert response.status_code == 200
    
    res_data = response.json()
    assert res_data["success"] is True
    
    modules = res_data["data"]["modules"]
    assert len(modules) == 1
    assert modules[0]["moduleTitle"] == "Module 1: Introduction"
    
    lessons = modules[0]["lessons"]
    assert len(lessons) == 3
    
    # Lesson 1 (Installation): 35 started. 5 stopped here. drop-off rate = 5/35 = 14.28%
    assert lessons[0]["lessonTitle"] == "Lesson 1: Installation"
    assert abs(lessons[0]["dropOffRate"] - 5/35) < 0.01
    assert lessons[0]["hasWarning"] is False
    
    # Lesson 2 (Variables): 30 started. 20 stopped here. drop-off rate = 20/30 = 66.67%
    assert lessons[1]["lessonTitle"] == "Lesson 2: Variables"
    assert abs(lessons[1]["dropOffRate"] - 20/30) < 0.01
    assert lessons[1]["hasWarning"] is True
    assert len(lessons[1]["timelineAnalysis"]) > 0
    
    # Lesson 3 (Functions): 10 started (< 30 student count threshold).
    assert lessons[2]["lessonTitle"] == "Lesson 3: Functions"
    assert lessons[2]["dropOffRate"] is None
    assert lessons[2]["hasWarning"] is False
    assert lessons[2]["timelineAnalysis"] is None


@pytest.mark.asyncio
async def test_lesson_analytics_detail(client: AsyncClient, test_data: dict):
    """Test GET /api/v1/courses/{courseId}/lessons/{lessonId}/analytics."""
    course_id = test_data["course"].id
    lesson1_id = test_data["lesson1"].id
    lesson3_id = test_data["lesson3"].id
    headers = test_data["headers"]

    # Test lesson 1 (reliable, student count >= 30)
    response = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson1_id}/analytics", headers=headers
    )
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert res_data["engagementMetrics"]["studentCount"] == 35
    assert res_data["reliabilityMessage"] is None

    # Test lesson 3 (low-data, student count < 30)
    response2 = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson3_id}/analytics", headers=headers
    )
    assert response2.status_code == 200
    res_data2 = response2.json()["data"]
    assert res_data2["engagementMetrics"]["studentCount"] == 10
    assert res_data2["reliabilityMessage"] == "Dữ liệu quá ít để phân tích tin cậy."
    assert res_data2["timelineAnalysis"] is None


@pytest.mark.asyncio
async def test_ai_insights_generation_and_caching(client: AsyncClient, test_data: dict, db_session):
    """Test GET /api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights."""
    course_id = test_data["course"].id
    lesson1_id = test_data["lesson1"].id
    lesson3_id = test_data["lesson3"].id
    headers = test_data["headers"]

    # 1. Lesson 3 has student count = 5 (< 30). Should return 400 Bad Request (LOW_DATA)
    response_low = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson3_id}/ai-insights", headers=headers
    )
    assert response_low.status_code == 400
    assert response_low.json()["error_code"] == "LOW_DATA"

    # 2. First call to Lesson 1: Should run simulated LLM generation and save to DB
    response_gen = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson1_id}/ai-insights", headers=headers
    )
    assert response_gen.status_code == 200
    res_data = response_gen.json()["data"]
    assert len(res_data["insights"]) == 1
    assert "Video có thời lượng quá dài" in res_data["insights"][0]["hypothesis"]
    assert len(res_data["recommendations"]) == 3
    
    insight_id = res_data["insights"][0]["insightId"]
    recommendation_id = res_data["recommendations"][0]["recommendationId"]

    # Verify saved in DB
    db_result = await db_session.execute(
        select(AiInsight).where(AiInsight.id == uuid.UUID(insight_id))
    )
    saved_insight = db_result.scalar_one_or_none()
    assert saved_insight is not None
    assert saved_insight.hypothesis == res_data["insights"][0]["hypothesis"]

    # 3. Second call to Lesson 1: Should return cached records
    # Let's modify the saved hypothesis directly in the database to test caching
    saved_insight.hypothesis = "Cached modification test"
    await db_session.commit()

    response_cached = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson1_id}/ai-insights", headers=headers
    )
    assert response_cached.status_code == 200
    res_data_cached = response_cached.json()["data"]
    assert res_data_cached["insights"][0]["hypothesis"] == "Cached modification test"


@pytest.mark.asyncio
async def test_recommendation_action(client: AsyncClient, test_data: dict, db_session):
    """Test POST /api/v1/courses/{courseId}/lessons/{lessonId}/recommendations/{recommendationId}/action."""
    course_id = test_data["course"].id
    lesson1_id = test_data["lesson1"].id
    headers = test_data["headers"]

    # Generate insights to create a recommendation
    gen_response = await client.get(
        f"/api/v1/courses/{course_id}/lessons/{lesson1_id}/ai-insights", headers=headers
    )
    rec_id = gen_response.json()["data"]["recommendations"][0]["recommendationId"]

    # Test invalid action input
    response_invalid = await client.post(
        f"/api/v1/courses/{course_id}/lessons/{lesson1_id}/recommendations/{rec_id}/action",
        json={"action": "invalid_action"},
        headers=headers
    )
    assert response_invalid.status_code == 422 # FastAPI validation error

    # Test apply recommendation
    response_apply = await client.post(
        f"/api/v1/courses/{course_id}/lessons/{lesson1_id}/recommendations/{rec_id}/action",
        json={"action": "applied"},
        headers=headers
    )
    assert response_apply.status_code == 200
    assert response_apply.json()["data"]["status"] == "applied"

    # Verify status in database
    db_result = await db_session.execute(
        select(Recommendation).where(Recommendation.id == uuid.UUID(rec_id))
    )
    rec_db = db_result.scalar_one()
    assert rec_db.status == "applied"
