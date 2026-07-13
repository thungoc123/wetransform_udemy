"""
Audit Logging Module.

This module provides functionality for logging critical business events
(audit trails) with context such as user ID, resources, and client IPs.
"""

from typing import Any, Optional

import structlog
from fastapi import Request

logger = structlog.get_logger("audit")


async def log_audit_event(
    action: str,
    teacher_id: Optional[str] = None,
    resource: Optional[str] = None,
    details: Optional[dict[str, Any]] = None,
    request: Optional[Request] = None,
) -> None:
    """
    Log an audit event.

    Args:
        action: The action being performed (e.g., 'TEACHER_LOGIN', 'COURSE_CREATED').
        teacher_id: The ID of the teacher performing the action.
        resource: The resource being affected (e.g., 'Course:123').
        details: Any additional details.
        request: The FastAPI Request object to extract IP/User-Agent if needed.
    """
    audit_data: dict[str, Any] = {
        "event_type": "AUDIT_TRAIL",
        "action": action,
    }

    if teacher_id:
        audit_data["teacher_id"] = str(teacher_id)
    if resource:
        audit_data["resource"] = resource
    if details:
        audit_data["details"] = details

    if request:
        audit_data["client_ip"] = request.client.host if request.client else "unknown"
        audit_data["user_agent"] = request.headers.get("user-agent", "unknown")

    logger.info("audit_event", **audit_data)
