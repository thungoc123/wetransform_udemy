import logging
import sys

import structlog

from app.config import settings


def setup_logging():
    """Configure structured logging for the application."""
    log_level = logging.INFO if settings.APP_ENV == "production" else logging.DEBUG

    # Clear existing log handlers to avoid duplicate logs
    logging.root.handlers = []

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # Use JSON layout for production, and colored dev layout for local
            (
                structlog.processors.JSONRenderer()
                if settings.APP_ENV == "production"
                else structlog.dev.ConsoleRenderer()
            ),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
