from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email giáo viên")
    password: str = Field(..., description="Mật khẩu đăng nhập")


class TokenResponse(BaseModel):
    token: str
    teacher_id: str = Field(alias="teacherId")
    name: str
    expires_at: int = Field(alias="expiresAt")

    model_config = ConfigDict(populate_by_name=True)
