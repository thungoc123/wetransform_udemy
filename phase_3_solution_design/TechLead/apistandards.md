# API Standards — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: API phải được thiết kế theo tiêu chuẩn nào?
> Nguồn gốc: [APISpec.md](../../../phase_2_story_definition/APISpec.md) (10 endpoints đã chốt)

---

## 1. API Style

### RESTful (Đã chốt)
- Mọi API tuân theo REST conventions
- **KHÔNG** dùng GraphQL (quá phức tạp cho MVP, team chưa có kinh nghiệm)
- **KHÔNG** dùng gRPC (không cần giao tiếp giữa services — Modular Monolith)

---

## 2. Endpoint Convention

### URL Format
```
/api/v{version}/{resource}/{id}/{sub-resource}
```

### Ví dụ (từ 10 API đã chốt trong Phase 2):
| Method | URL | Mô tả |
|---|---|---|
| POST | `/api/v1/auth/login` | Đăng nhập |
| POST | `/api/v1/data/udemy-connection` | Kết nối Udemy API |
| POST | `/api/v1/data/upload` | Upload file CSV/XLSX |
| GET | `/api/v1/courses` | Danh sách khóa học |
| GET | `/api/v1/courses/{courseId}/dashboard` | Dashboard tổng quan |
| GET | `/api/v1/courses/{courseId}/drop-off-analysis` | Phân tích điểm dừng |
| GET | `/api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights` | AI Insights |
| POST | `/api/v1/courses/{courseId}/lessons/{lessonId}/recommendations/{recommendationId}/action` | Cập nhật recommendation |
| GET | `/api/v1/courses/{courseId}/lessons/{lessonId}/at-risk-students` | Danh sách at-risk |
| POST | `/api/v1/courses/{courseId}/lessons/{lessonId}/send-reminder` | Gửi nhắc nhở |

### Versioning
- **Cách thức:** URL prefix (`/api/v1/`)
- **Khi nào tăng version:** Breaking changes (thay đổi response format, xóa field)
- **MVP:** Chỉ có `v1`

---

## 3. Request

### Validation
- Validate ở **Router layer** bằng Pydantic schema
- Trả `400 Bad Request` nếu thiếu field hoặc sai format
- Ví dụ:
```python
class LoginRequest(BaseModel):
    email: EmailStr          # Validate email format tự động
    password: str = Field(min_length=1, description="Mật khẩu không được để trống")

class ReminderRequest(BaseModel):
    student_ids: list[UUID] = Field(min_length=1, description="Ít nhất 1 học viên")
    message_body: str = Field(min_length=1, max_length=2000)
```

### Pagination
- **Format:** `?page=1&page_size=20`
- **Áp dụng cho:** GET /courses, GET /at-risk-students
- **Mặc định:** page=1, page_size=20
- **Giới hạn:** page_size tối đa 100
- **Response bổ sung:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 150,
    "page": 1,
    "page_size": 20,
    "total_pages": 8
  }
}
```

### Sorting
- **Format:** `?sort_by=created_at&sort_order=desc`
- **Mặc định:** `sort_by=created_at`, `sort_order=desc` (mới nhất trước)
- **Áp dụng cho:** GET /courses

### Filtering
- **Format:** Query parameters
- **Ví dụ:** GET /at-risk-students?status=at_risk

---

## 4. Response

### Response Format chuẩn (Áp dụng cho MỌI API)

**Success Response:**
```json
{
  "success": true,
  "data": {
    "courseId": "uuid-here",
    "title": "Python for Beginners",
    "studentCount": 250
  },
  "message": "",
  "error_code": null
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "message": "Email hoặc Mật khẩu không chính xác",
  "error_code": "INVALID_CREDENTIALS"
}
```

### Error Codes (suy ra từ API Spec)
| HTTP Status | Error Code | Khi nào dùng | API liên quan |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Thiếu field bắt buộc, sai format | Tất cả |
| 401 | `INVALID_CREDENTIALS` | Sai email/password | POST /login |
| 401 | `TOKEN_EXPIRED` | JWT hết hạn | Tất cả (trừ /login) |
| 403 | `FORBIDDEN` | Không có quyền truy cập khóa học | GET /dashboard, /drop-off |
| 404 | `NOT_FOUND` | Không tìm thấy resource | GET /ai-insights, /dashboard |
| 413 | `PAYLOAD_TOO_LARGE` | File upload quá lớn | POST /upload |
| 423 | `ACCOUNT_LOCKED` | Tài khoản bị khóa 15 phút | POST /login |
| 429 | `COOLDOWN_ACTIVE` | Đã gửi reminder trong 7 ngày | POST /send-reminder |
| 500 | `INTERNAL_ERROR` | Lỗi server (không lộ stack trace) | Tất cả |

### Response Field Naming
- **Quy tắc:** `camelCase` (cho JSON response gửi về Frontend)
- **Lý do:** JavaScript convention, dễ đọc ở Frontend
- **Mapping:** SQLAlchemy `snake_case` → Pydantic `camelCase` (dùng `alias_generator`)
- **Ví dụ:** `student_count` (DB) → `studentCount` (API response)

---

## 5. Authentication

### JWT Bearer Token (Đã chốt)
- **Header:** `Authorization: Bearer <token>`
- **Payload JWT:**
```json
{
  "sub": "teacher-uuid-here",
  "name": "Nguyễn Thị Ngọc Thư",
  "exp": 1720483200,
  "iat": 1720396800
}
```
- **Token lifetime:** 24 giờ (MVP)
- **Refresh token:** Chưa áp dụng trong MVP
- **Endpoints không cần auth:** Chỉ `POST /api/v1/auth/login`
- **Tất cả endpoint khác:** Bắt buộc có JWT token hợp lệ

### KHÔNG dùng:
- ~~OAuth2 (Social Login)~~ — MVP chưa cần
- ~~API Key~~ — Không phù hợp cho ứng dụng web

---

## 6. Documentation

### Swagger / OpenAPI (Tự động)
- **Tool:** FastAPI tự động sinh Swagger UI từ Pydantic schemas
- **URL:** `http://localhost:8000/docs` (Swagger UI) hoặc `/redoc` (ReDoc)
- **Không cần** viết tay file OpenAPI spec — FastAPI auto-generate
- **Yêu cầu:** Mỗi Router phải có:
  - `summary` — mô tả ngắn
  - `description` — mô tả chi tiết
  - `response_model` — Pydantic schema cho response
  - `responses` — error cases

### Ví dụ:
```python
@router.get(
    "/courses/{course_id}/dashboard",
    summary="Get Course Dashboard Overview",
    description="Lấy dữ liệu tổng quan khóa học: completion rate, drop-off rate, student counts",
    response_model=StandardResponse[DashboardResponse],
    responses={
        403: {"description": "Giáo viên không sở hữu khóa học này"},
        404: {"description": "Khóa học không tồn tại hoặc chưa có dữ liệu"},
    },
)
```

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*