import asyncio

import structlog
from sqlalchemy import select

from app.database import async_session_maker
from app.models.teacher import Teacher
from app.shared.security import hash_password

logger = structlog.get_logger(__name__)


async def seed_data():
    logger.info("starting_database_seeder")
    async with async_session_maker() as session:
        # Check if admin already exists
        result = await session.execute(
            select(Teacher).filter(Teacher.email == "admin@learning-analytics.com")
        )
        admin = result.scalars().first()

        if not admin:
            logger.info("admin_user_not_found_creating")
            new_admin = Teacher(
                email="admin@learning-analytics.com",
                password_hash=hash_password("admin"),
                name="Admin Teacher",
            )
            session.add(new_admin)
            await session.commit()
            logger.info("Admin user created successfully.")
        else:
            logger.info("Admin user already exists. Skipping.")


if __name__ == "__main__":
    asyncio.run(seed_data())
