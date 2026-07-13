import asyncio
import logging
from sqlalchemy import select
from app.database import async_session_maker
from app.modules.auth.models import Teacher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_data():
    logger.info("Starting database seeder...")
    async with async_session_maker() as session:
        # Check if admin already exists
        result = await session.execute(select(Teacher).filter(Teacher.email == "admin@learning-analytics.com"))
        admin = result.scalars().first()

        if not admin:
            logger.info("Admin user not found. Creating admin user...")
            # Tạm thời lưu plain text, sẽ hash sau khi thực hiện task FND-019 (Password Hashing)
            new_admin = Teacher(
                email="admin@learning-analytics.com",
                hashed_password="admin",
                name="Admin Teacher"
            )
            session.add(new_admin)
            await session.commit()
            logger.info("Admin user created successfully.")
        else:
            logger.info("Admin user already exists. Skipping.")

if __name__ == "__main__":
    asyncio.run(seed_data())
