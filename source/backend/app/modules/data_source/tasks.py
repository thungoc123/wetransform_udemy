import asyncio
import hashlib
import uuid

import pandas as pd
from celery import chord, shared_task
from celery.utils.log import get_task_logger
from sqlalchemy import select

from app.database import async_session_maker
from app.models.activity import LearningActivity, StudentEnrollment
from app.models.course import Course, Lesson, Module
from app.models.import_data import DataImport

logger = get_task_logger(__name__)


def hash_pii(text: str) -> str:
    if not text:
        return "unknown"
    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()[:16]


async def _create_courses_and_lessons(file_path: str, teacher_id: uuid.UUID):
    df = pd.read_csv(
        file_path, usecols=lambda c: c in ["Course Name", "Item Name", "Item Type"]
    )
    df.drop_duplicates(inplace=True)

    async with async_session_maker() as session:
        for course_name in df["Course Name"].dropna().unique():
            # Check if course exists
            stmt = select(Course).where(
                Course.title == course_name, Course.teacher_id == teacher_id
            )
            result = await session.execute(stmt)
            course = result.scalar_one_or_none()
            if not course:
                course = Course(title=course_name, teacher_id=teacher_id)
                session.add(course)
                await session.flush()

            # Module logic is simplified since Udemy CSV might not have modules explicitly
            module = Module(title="Default Module", course_id=course.id, order_index=1)
            session.add(module)
            await session.flush()

            # Add lessons
            lessons_df = df[df["Course Name"] == course_name]
            for idx, row in lessons_df.iterrows():
                lesson_name = row["Item Name"]
                lesson_type = (
                    row["Item Type"].lower() if pd.notna(row["Item Type"]) else "video"
                )

                stmt = select(Lesson).where(
                    Lesson.title == lesson_name, Lesson.course_id == course.id
                )
                res = await session.execute(stmt)
                if not res.scalar_one_or_none():
                    lesson = Lesson(
                        title=lesson_name,
                        type=lesson_type,
                        course_id=course.id,
                        module_id=module.id,
                        order_index=idx,
                    )
                    session.add(lesson)
        await session.commit()


@shared_task(name="app.modules.data_source.tasks.process_import_master_task")
def process_import_master_task(
    data_import_id_str: str, file_path: str, teacher_id_str: str
):
    """
    Master task to read CSV, setup Courses/Lessons, and chunk the rest to sub-tasks.
    """
    logger.info(f"Starting master task for import {data_import_id_str}")
    teacher_id = uuid.UUID(teacher_id_str)

    # Setup Foreign Keys sequentially to avoid Race Conditions
    asyncio.run(_create_courses_and_lessons(file_path, teacher_id))

    # Chunk the CSV
    chunk_size = 5000
    tasks = []

    for _, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        chunk_data = chunk.to_dict(orient="records")
        tasks.append(process_import_chunk_task.s(chunk_data, teacher_id_str))  # type: ignore

    # Use a chord to execute all chunk tasks, then call completion task
    chord(tasks)(finalize_import_task.s(data_import_id_str))  # type: ignore


async def _upsert_chunk(chunk_data: list, teacher_id: uuid.UUID):
    async with async_session_maker() as session:
        # We need course & lesson IDs
        courses_cache = {}
        lessons_cache = {}

        # Load mappings
        stmt = select(Course).where(Course.teacher_id == teacher_id)
        res = await session.execute(stmt)
        for c in res.scalars():
            courses_cache[c.title] = c.id

            stmt_l = select(Lesson).where(Lesson.course_id == c.id)
            res_l = await session.execute(stmt_l)
            for lsn in res_l.scalars():
                lessons_cache[f"{c.id}_{lsn.title}"] = lsn.id

        enrollments_cache = {}

        for row in chunk_data:
            course_name = row.get("Course Name")
            lesson_name = row.get("Item Name")
            user_name = str(row.get("User Name", "unknown"))
            progress = float(row.get("% Completed", 0.0))

            if not course_name or not lesson_name:
                continue

            course_id = courses_cache.get(course_name)
            if not course_id:
                continue

            lesson_id = lessons_cache.get(f"{course_id}_{lesson_name}")
            if not lesson_id:
                continue

            # Hash PII
            student_hash = hash_pii(user_name)

            # Create or get Enrollment
            enroll_key = f"{course_id}_{student_hash}"
            if enroll_key not in enrollments_cache:
                stmt_e = select(StudentEnrollment).where(
                    StudentEnrollment.udemy_student_id == student_hash,
                    StudentEnrollment.course_id == course_id,
                )
                res_e = await session.execute(stmt_e)
                enrollment = res_e.scalar_one_or_none()
                if not enrollment:
                    enrollment = StudentEnrollment(
                        udemy_student_id=student_hash,
                        masked_name=user_name,
                        course_id=course_id,
                        progress_percent=progress,
                    )
                    session.add(enrollment)
                    await session.flush()
                enrollments_cache[enroll_key] = enrollment.id

            enrollment_id = enrollments_cache[enroll_key]

            from datetime import datetime, timezone

            # Create Activity
            activity = LearningActivity(
                student_enrollment_id=enrollment_id,
                lesson_id=lesson_id,
                activity_type="view",
                started_at=datetime.now(timezone.utc),
                duration_seconds=int(
                    progress * 100
                ),  # dummy mapping if duration not available
                is_completed=(progress >= 1.0),
            )
            session.add(activity)

        await session.commit()


@shared_task(name="app.modules.data_source.tasks.process_import_chunk_task")
def process_import_chunk_task(chunk_data: list, teacher_id_str: str):
    """
    Sub-task to process a chunk of the CSV.
    """
    teacher_id = uuid.UUID(teacher_id_str)
    asyncio.run(_upsert_chunk(chunk_data, teacher_id))
    return len(chunk_data)


async def _update_status(
    import_id: uuid.UUID, total_activities: int, data_import_id_str: str
):
    async with async_session_maker() as session:
        stmt = select(DataImport).where(DataImport.id == import_id)
        res = await session.execute(stmt)
        data_import = res.scalar_one_or_none()
        if data_import:
            data_import.status = "completed"  # type: ignore
            data_import.row_count = total_activities  # type: ignore
            await session.commit()

    logger.info(
        f"Data Import {data_import_id_str} completed with {total_activities} activities."
    )


@shared_task(name="app.modules.data_source.tasks.finalize_import_task")
def finalize_import_task(results: list, data_import_id_str: str):
    total_rows = sum(results)
    import_id = uuid.UUID(data_import_id_str)
    asyncio.run(_update_status(import_id, total_rows, data_import_id_str))
    logger.info(f"Import {import_id} completed with {total_rows} rows.")
