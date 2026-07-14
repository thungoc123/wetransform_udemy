from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teacher import Teacher


async def get_teacher_by_email(db: AsyncSession, email: str) -> Teacher | None:
    result = await db.execute(select(Teacher).where(Teacher.email == email))
    return result.scalar_one_or_none()


async def update_login_fail(db: AsyncSession, teacher: Teacher) -> None:
    current_count = int(teacher.failed_login_count or 0)  # type: ignore
    teacher.failed_login_count = current_count + 1  # type: ignore
    if (current_count + 1) >= 5:
        teacher.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)  # type: ignore
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)


async def reset_login_success(db: AsyncSession, teacher: Teacher) -> None:
    teacher.failed_login_count = 0  # type: ignore
    teacher.locked_until = None  # type: ignore
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)
