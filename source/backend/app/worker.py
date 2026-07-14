from celery import Celery

from app.config import settings

celery_app = Celery(
    "learning_analytics_worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Load task modules automatically from app.shared and other modules
celery_app.autodiscover_tasks(["app.shared", "app.modules.data_source"])
