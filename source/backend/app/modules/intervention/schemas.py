import uuid

from pydantic import BaseModel, Field


class StudentAtRisk(BaseModel):
    student_id: str = Field(..., description="ID hash của học viên")
    masked_name: str = Field(..., description="Tên học viên đã được ẩn danh một phần")
    days_inactive: int = Field(..., description="Số ngày không hoạt động")
    can_send_reminder: bool = Field(
        ..., description="True nếu chưa nhận reminder trong 7 ngày qua"
    )


class AtRiskStudentsResponse(BaseModel):
    lesson_id: uuid.UUID
    default_message_template: str
    students: list[StudentAtRisk]


class SendReminderRequest(BaseModel):
    student_ids: list[str] = Field(
        ..., min_length=1, description="Danh sách ID học viên nhận reminder"
    )
    message_body: str = Field(..., min_length=5, description="Nội dung email nhắc nhở")


class ReminderFailure(BaseModel):
    student_id: str
    reason: str


class SendReminderResponse(BaseModel):
    sent_count: int
    failed_count: int
    failures: list[ReminderFailure] = []
