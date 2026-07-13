import structlog

from app.worker import celery_app

logger = structlog.get_logger(__name__)


@celery_app.task(name="app.shared.email.send_email_task")
def send_email_task(to_email: str, subject: str, content: str):
    """
    Background job to send an email via Celery.
    (Stub implementation for MVP)
    """
    logger.info("sending_email", to_email=to_email, subject=subject)

    # In reality, you'd use a service like SendGrid, AWS SES, or SMTP here.
    # Example:
    # sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    # response = sg.send(message)

    return {"status": "sent", "to": to_email}
