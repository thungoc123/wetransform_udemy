import asyncio
import uuid
from datetime import datetime, timezone, timedelta
import structlog
from sqlalchemy import select

from app.database import async_session_maker, Base, engine
from app.models.teacher import Teacher
from app.models.course import Course, Module, Lesson
from app.models.activity import StudentEnrollment, LearningActivity
from app.shared.security import hash_password

logger = structlog.get_logger(__name__)


async def seed_data():
    logger.info("creating_tables_if_not_exists")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("starting_database_seeder")
    async with async_session_maker() as session:
        # 1. Check if admin already exists
        result = await session.execute(
            select(Teacher).filter(Teacher.email == "admin@learning-analytics.com")
        )
        admin = result.scalars().first()

        if not admin:
            logger.info("admin_user_not_found_creating")
            admin = Teacher(
                email="admin@learning-analytics.com",
                password_hash=hash_password("admin"),
                name="Admin Teacher",
            )
            session.add(admin)
            await session.commit()
            await session.refresh(admin)
            logger.info("Admin user created successfully.")
        else:
            logger.info("Admin user already exists. Checking for existing courses.")

        # Check if courses are already seeded for this teacher
        course_check = await session.execute(
            select(Course).filter(Course.teacher_id == admin.id)
        )
        existing_courses = course_check.scalars().all()
        if existing_courses:
            logger.info("Courses already seeded for admin. Skipping seeder database load.")
            return

        now = datetime.now(timezone.utc)

        # -------------------------------------------------------------
        # COURSE 1: Lập trình Python từ cơ bản đến nâng cao
        # -------------------------------------------------------------
        logger.info("seeding_course_1")
        course1 = Course(
            id=uuid.uuid4(),
            teacher_id=admin.id,
            title="Lập trình Python từ cơ bản đến nâng cao",
            student_count=40,
            status="imported"
        )
        session.add(course1)

        # Modules for Course 1
        m1_1 = Module(id=uuid.uuid4(), course_id=course1.id, title="Giới thiệu & Cài đặt", order_index=1)
        m1_2 = Module(id=uuid.uuid4(), course_id=course1.id, title="Cấu trúc điều khiển & Vòng lặp", order_index=2)
        m1_3 = Module(id=uuid.uuid4(), course_id=course1.id, title="Hàm & Lập trình hướng đối tượng", order_index=3)
        session.add_all([m1_1, m1_2, m1_3])

        # Lessons for Course 1
        l1_1 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_1.id, title="Cài đặt Python và IDE", type="video", order_index=1, duration_seconds=600, student_count=40)
        l1_2 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_1.id, title="Chương trình Hello World", type="video", order_index=2, duration_seconds=450, student_count=40)
        l1_3 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_1.id, title="Bài kiểm tra trắc nghiệm đầu khóa", type="quiz", order_index=3, student_count=40)

        l1_4 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_2.id, title="Câu lệnh điều kiện If-Else", type="video", order_index=4, duration_seconds=800, student_count=25)
        l1_5 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_2.id, title="Vòng lặp For và While", type="video", order_index=5, duration_seconds=900, student_count=25)
        l1_6 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_2.id, title="Bài tập thực hành vòng lặp", type="quiz", order_index=6, student_count=25)

        l1_7 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_3.id, title="Định nghĩa Hàm (Functions)", type="video", order_index=7, duration_seconds=1000, student_count=15)
        l1_8 = Lesson(id=uuid.uuid4(), course_id=course1.id, module_id=m1_3.id, title="Lập trình hướng đối tượng cơ bản", type="video", order_index=8, duration_seconds=1200, student_count=15)
        session.add_all([l1_1, l1_2, l1_3, l1_4, l1_5, l1_6, l1_7, l1_8])

        # Enrollments for Course 1 (40 students)
        enrollments1 = []
        # 15 Active (progress = 100%)
        for i in range(15):
            enrollments1.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course1.id,
                udemy_student_id=f"c1_std_{i}",
                masked_name=f"Học viên {i+1}",
                progress_percent=100.0,
                last_activity_at=now - timedelta(days=i % 7)
            ))
        # 10 At-risk (progress = 37.5%, stopped at lesson 1.3)
        for i in range(15, 25):
            enrollments1.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course1.id,
                udemy_student_id=f"c1_std_{i}",
                masked_name=f"Học viên {i+1}",
                progress_percent=37.50,
                last_activity_at=now - timedelta(days=15 + (i % 10))
            ))
        # 15 Inactive (progress = 12.5%, stopped at lesson 1.1)
        for i in range(25, 40):
            enrollments1.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course1.id,
                udemy_student_id=f"c1_std_{i}",
                masked_name=f"Học viên {i+1}",
                progress_percent=12.50,
                last_activity_at=now - timedelta(days=32 + (i % 10))
            ))
        session.add_all(enrollments1)

        # -------------------------------------------------------------
        # COURSE 2: Lập trình Web với React và FastAPI
        # -------------------------------------------------------------
        logger.info("seeding_course_2")
        course2 = Course(
            id=uuid.uuid4(),
            teacher_id=admin.id,
            title="Lập trình Web với React và FastAPI",
            student_count=35,
            status="imported"
        )
        session.add(course2)

        m2_1 = Module(id=uuid.uuid4(), course_id=course2.id, title="Cơ bản về React & Component", order_index=1)
        m2_2 = Module(id=uuid.uuid4(), course_id=course2.id, title="Xây dựng Backend với FastAPI", order_index=2)
        session.add_all([m2_1, m2_2])

        l2_1 = Lesson(id=uuid.uuid4(), course_id=course2.id, module_id=m2_1.id, title="Giới thiệu JSX và Component", type="video", order_index=1, duration_seconds=700, student_count=35)
        l2_2 = Lesson(id=uuid.uuid4(), course_id=course2.id, module_id=m2_1.id, title="State và Props trong React", type="video", order_index=2, duration_seconds=850, student_count=35)
        l2_3 = Lesson(id=uuid.uuid4(), course_id=course2.id, module_id=m2_1.id, title="Quản lý State nâng cao với Redux", type="video", order_index=3, duration_seconds=1500, student_count=35)

        l2_4 = Lesson(id=uuid.uuid4(), course_id=course2.id, module_id=m2_2.id, title="Giới thiệu FastAPI & Uvicorn", type="video", order_index=4, duration_seconds=600, student_count=15)
        l2_5 = Lesson(id=uuid.uuid4(), course_id=course2.id, module_id=m2_2.id, title="Kết nối Database với SQLAlchemy", type="video", order_index=5, duration_seconds=1000, student_count=15)
        session.add_all([l2_1, l2_2, l2_3, l2_4, l2_5])

        # Enrollments for Course 2 (35 students)
        enrollments2 = []
        # 12 Active (progress = 100%)
        for i in range(12):
            enrollments2.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course2.id,
                udemy_student_id=f"c2_std_{i}",
                masked_name=f"Học sinh {i+1}",
                progress_percent=100.0,
                last_activity_at=now - timedelta(days=i % 7)
            ))
        # 8 At-risk (progress = 40%, stopped at lesson 2.2 Redux)
        for i in range(12, 20):
            enrollments2.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course2.id,
                udemy_student_id=f"c2_std_{i}",
                masked_name=f"Học sinh {i+1}",
                progress_percent=40.0,
                last_activity_at=now - timedelta(days=16 + (i % 8))
            ))
        # 15 Inactive (progress = 20%, stopped at lesson 2.1 JSX)
        for i in range(20, 35):
            enrollments2.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course2.id,
                udemy_student_id=f"c2_std_{i}",
                masked_name=f"Học sinh {i+1}",
                progress_percent=20.0,
                last_activity_at=now - timedelta(days=35 + (i % 10))
            ))
        session.add_all(enrollments2)

        # -------------------------------------------------------------
        # COURSE 3: Học máy cơ bản cho mọi người (Low student count < 30)
        # -------------------------------------------------------------
        logger.info("seeding_course_3")
        course3 = Course(
            id=uuid.uuid4(),
            teacher_id=admin.id,
            title="Học máy cơ bản cho mọi người",
            student_count=10,
            status="imported"
        )
        session.add(course3)

        m3_1 = Module(id=uuid.uuid4(), course_id=course3.id, title="Giới thiệu Trí tuệ Nhân tạo", order_index=1)
        m3_2 = Module(id=uuid.uuid4(), course_id=course3.id, title="Hồi quy tuyến tính", order_index=2)
        session.add_all([m3_1, m3_2])

        l3_1 = Lesson(id=uuid.uuid4(), course_id=course3.id, module_id=m3_1.id, title="Trí tuệ nhân tạo là gì?", type="video", order_index=1, duration_seconds=500, student_count=10)
        l3_2 = Lesson(id=uuid.uuid4(), course_id=course3.id, module_id=m3_1.id, title="Các thuật toán học máy phổ biến", type="video", order_index=2, duration_seconds=600, student_count=10)
        l3_3 = Lesson(id=uuid.uuid4(), course_id=course3.id, module_id=m3_2.id, title="Toán học trong hồi quy tuyến tính", type="video", order_index=3, duration_seconds=1200, student_count=5)
        session.add_all([l3_1, l3_2, l3_3])

        # Enrollments for Course 3 (10 students)
        enrollments3 = []
        for i in range(10):
            enrollments3.append(StudentEnrollment(
                id=uuid.uuid4(),
                course_id=course3.id,
                udemy_student_id=f"c3_std_{i}",
                masked_name=f"Sinh viên {i+1}",
                progress_percent=66.67 if i < 5 else 33.33,
                last_activity_at=now - timedelta(days=1 + i)
            ))
        session.add_all(enrollments3)

        await session.flush()

        # -------------------------------------------------------------
        # SEEDING ACTIVITIES (Course 1, Course 2, Course 3)
        # -------------------------------------------------------------
        logger.info("seeding_learning_activities")
        activities = []

        # Activities for Course 1
        for idx, se in enumerate(enrollments1):
            # All 40 students studied lesson 1.1
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l1_1.id,
                activity_type="video",
                started_at=now - timedelta(days=40),
                ended_at=now - timedelta(days=40),
                duration_seconds=580,
                video_stop_at_second=180 if idx % 3 == 0 else (350 if idx % 2 == 0 else None),
                is_completed=True
            ))

            # All 40 studied lesson 1.2
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l1_2.id,
                activity_type="video",
                started_at=now - timedelta(days=39),
                ended_at=now - timedelta(days=39),
                duration_seconds=420,
                is_completed=True
            ))

            # All 40 completed lesson 1.3 (quiz)
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l1_3.id,
                activity_type="quiz",
                started_at=now - timedelta(days=38),
                ended_at=now - timedelta(days=38),
                is_completed=True
            ))

            # 25 students (15 active + 10 at-risk) went on to Module 2
            if idx < 25:
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l1_4.id,
                    activity_type="video",
                    started_at=now - timedelta(days=20),
                    ended_at=now - timedelta(days=20),
                    duration_seconds=750,
                    is_completed=True
                ))
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l1_5.id,
                    activity_type="video",
                    started_at=now - timedelta(days=19),
                    ended_at=now - timedelta(days=19),
                    duration_seconds=850,
                    is_completed=True
                ))
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l1_6.id,
                    activity_type="quiz",
                    started_at=now - timedelta(days=18),
                    ended_at=now - timedelta(days=18),
                    is_completed=True
                ))

            # Only the 15 active students studied Module 3
            if idx < 15:
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l1_7.id,
                    activity_type="video",
                    started_at=now - timedelta(days=5),
                    ended_at=now - timedelta(days=5),
                    duration_seconds=950,
                    is_completed=True
                ))
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l1_8.id,
                    activity_type="video",
                    started_at=now - timedelta(days=2),
                    ended_at=now - timedelta(days=2),
                    duration_seconds=1150,
                    is_completed=True
                ))

        # Activities for Course 2
        for idx, se in enumerate(enrollments2):
            # All 35 students studied lesson 2.1 (JSX)
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l2_1.id,
                activity_type="video",
                started_at=now - timedelta(days=50),
                ended_at=now - timedelta(days=50),
                duration_seconds=680,
                is_completed=True
            ))

            # All 35 studied lesson 2.2 (State & Props)
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l2_2.id,
                activity_type="video",
                started_at=now - timedelta(days=45),
                ended_at=now - timedelta(days=45),
                duration_seconds=820,
                is_completed=True
            ))

            # All 35 studied lesson 2.3 (Redux - heavily pauses and drop-offs)
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l2_3.id,
                activity_type="video",
                started_at=now - timedelta(days=40),
                ended_at=now - timedelta(days=40),
                duration_seconds=1100,
                # Pauses at 420s (7 minutes) and 600s (10 minutes)
                video_stop_at_second=420 if idx % 3 == 0 else (600 if idx % 2 == 0 else None),
                is_completed=idx < 20  # Only 20 students completed Redux
            ))

            # 15 students continue to Module 2
            if idx < 15:
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l2_4.id,
                    activity_type="video",
                    started_at=now - timedelta(days=5),
                    ended_at=now - timedelta(days=5),
                    duration_seconds=580,
                    is_completed=True
                ))
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l2_5.id,
                    activity_type="video",
                    started_at=now - timedelta(days=2),
                    ended_at=now - timedelta(days=2),
                    duration_seconds=980,
                    is_completed=True
                ))

        # Activities for Course 3
        for idx, se in enumerate(enrollments3):
            # All 10 students studied lesson 3.1
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l3_1.id,
                activity_type="video",
                started_at=now - timedelta(days=5),
                ended_at=now - timedelta(days=5),
                duration_seconds=480,
                is_completed=True
            ))
            # All 10 studied lesson 3.2
            activities.append(LearningActivity(
                student_enrollment_id=se.id,
                lesson_id=l3_2.id,
                activity_type="video",
                started_at=now - timedelta(days=4),
                ended_at=now - timedelta(days=4),
                duration_seconds=550,
                is_completed=True
            ))
            # 5 students studied lesson 3.3
            if idx < 5:
                activities.append(LearningActivity(
                    student_enrollment_id=se.id,
                    lesson_id=l3_3.id,
                    activity_type="video",
                    started_at=now - timedelta(days=2),
                    ended_at=now - timedelta(days=2),
                    duration_seconds=1100,
                    is_completed=True
                ))

        session.add_all(activities)
        await session.commit()
        logger.info("database_seeder_completed_successfully")


if __name__ == "__main__":
    asyncio.run(seed_data())
