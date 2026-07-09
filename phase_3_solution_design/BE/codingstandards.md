# Coding Standards — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: Developer và AI phải viết code như thế nào?
> Nguồn gốc: [Spec.md](../../../Spec.md) mục 4, [techstack.md](../TechLead/techstack.md), [project_struture.md](../TechLead/project_struture.md)

---

## 1. Naming Convention

| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| **Class** | PascalCase | `CourseService`, `LessonRepository`, `DataImportTask` |
| **Function / Method** | snake_case | `get_drop_off_analysis()`, `send_reminder()`, `parse_uploaded_file()` |
| **Variable** | snake_case | `student_count`, `drop_off_rate`, `has_warning` |
| **Constant** | UPPER_SNAKE_CASE | `MAX_LOGIN_ATTEMPTS = 5`, `COOLDOWN_DAYS = 7`, `DROP_OFF_THRESHOLD = 0.20` |
| **File** | snake_case | `course_service.py`, `ai_insight_repository.py`, `prompt_builder.py` |
| **Folder / Module** | snake_case | `ai_insights/`, `data_import/`, `intervention/` |
| **DB Table** | snake_case, số nhiều | `courses`, `learning_activities`, `reminder_logs` |
| **DB Column** | snake_case | `created_at`, `video_stop_at_second`, `confidence_score` |
| **API URL** | kebab-case | `/api/v1/drop-off-analysis`, `/api/v1/at-risk-students` |
| **Pydantic Schema** | PascalCase + suffix | `LoginRequest`, `DashboardResponse`, `ReminderCreateSchema` |
| **SQLAlchemy Model** | PascalCase, danh từ số ít | `Teacher`, `Course`, `LearningActivity` |

---

## 2. Code Style

### Formatting
- **Tool:** Black (line-length = 88)
- **Config:** Thêm vào `pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py311']
```

### Lint
- **Tool:** Ruff (thay ESLint/Flake8, nhanh hơn 10-100x)
- **Config:**
```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]
```

### Type Hinting (Bắt buộc)
- Mọi function signature phải có type hint cho parameters và return type
- Ví dụ:
```python
# ✅ Đúng
async def get_dashboard(self, course_id: UUID, teacher_id: UUID) -> DashboardResponse:
    ...

# ❌ Sai — thiếu type hint
async def get_dashboard(self, course_id, teacher_id):
    ...
```

### Comment & Documentation
- **Docstring:** Google style, bắt buộc cho mọi public class và public method
- Ví dụ:
```python
class AnalyticsService:
    """Service xử lý logic phân tích dashboard và drop-off.

    Chịu trách nhiệm tính toán các chỉ số: completion rate, drop-off rate,
    active/inactive/at-risk student count cho từng khóa học.
    """

    async def get_drop_off_analysis(self, course_id: UUID) -> DropOffResponse:
        """Lấy phân tích điểm dừng cho khóa học.

        Args:
            course_id: UUID của khóa học cần phân tích.

        Returns:
            DropOffResponse chứa danh sách modules và lessons với drop_off_rate.

        Raises:
            ForbiddenException: Giáo viên không sở hữu khóa học này.
            NotFoundException: Không tìm thấy dữ liệu phân tích.
        """
```

---

## 3. Design Principles

### Áp dụng:
- **[x] Repository Pattern** — Tách biệt logic truy vấn DB khỏi business logic
- **[x] Service Layer** — Mọi business logic nằm trong Service, không nằm trong Router
- **[x] Dependency Injection** — Dùng FastAPI `Depends()`, không `new` trực tiếp
- **[x] Single Responsibility** — Mỗi file/class chỉ làm 1 việc

### KHÔNG áp dụng trong MVP:
- [ ] CQRS — Quá phức tạp cho 4 người, 6 tính năng
- [ ] DDD phức tạp (Bounded Context) — Modular Monolith đủ dùng
- [ ] Event Sourcing — Không cần replay event history

### Ví dụ Dependency Injection:
```python
# dependencies.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_teacher(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Teacher:
    # Decode JWT, verify teacher exists
    ...

# router.py
@router.get("/courses/{course_id}/dashboard")
async def get_dashboard(
    course_id: UUID,
    teacher: Teacher = Depends(get_current_teacher),
    service: AnalyticsService = Depends(get_analytics_service),
) -> StandardResponse[DashboardResponse]:
    data = await service.get_dashboard(course_id, teacher.id)
    return StandardResponse(success=True, data=data)
```

### Ví dụ Repository Pattern:
```python
# repository.py — Chỉ chứa query DB
class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, course_id: UUID) -> Course | None:
        result = await self.db.execute(
            select(Course).where(Course.id == course_id, Course.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

# service.py — Chỉ chứa business logic
class AnalyticsService:
    def __init__(self, course_repo: CourseRepository, enrollment_repo: EnrollmentRepository):
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo

    async def get_dashboard(self, course_id: UUID, teacher_id: UUID) -> DashboardResponse:
        course = await self.course_repo.get_by_id(course_id)
        if not course or course.teacher_id != teacher_id:
            raise ForbiddenException("Không có quyền truy cập khóa học này")
        # ... business logic tính toán
```

---

## 4. Best Practices

### Exception Handling
- **Global Exception Handler:** Xử lý tập trung trong `shared/exceptions.py`
- **Không lộ stack trace** ra response — chỉ trả message thân thiện
- **Custom Exceptions:**
```python
class AppException(Exception):
    def __init__(self, status_code: int, message: str, error_code: str):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code

class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(401, "Email hoặc Mật khẩu không chính xác", "INVALID_CREDENTIALS")

class AccountLockedException(AppException):
    def __init__(self):
        super().__init__(423, "Tài khoản đang bị khóa tạm thời", "ACCOUNT_LOCKED")

class ForbiddenException(AppException):
    def __init__(self, message: str = "Không có quyền truy cập"):
        super().__init__(403, message, "FORBIDDEN")

class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(404, f"{resource} không tồn tại", "NOT_FOUND")
```

### Validation
- Validate ở **Router layer** bằng Pydantic schema
- **Không** validate lại ở Service — Service tin tưởng dữ liệu đã qua Router
- Ví dụ:
```python
class LoginRequest(BaseModel):
    email: EmailStr          # Tự động validate format email
    password: str = Field(min_length=1)  # Không để trống

class UploadFileRequest(BaseModel):
    # Validate trong router bằng UploadFile type
    pass
```

### Logging
- **Tool:** structlog (structured JSON log)
- **Bắt buộc có `correlation_id`** cho mỗi request — gán trong middleware
- **Không dùng `print()`** — chỉ dùng logger
- Ví dụ:
```python
import structlog
logger = structlog.get_logger()

# Trong service
logger.info("login_attempt", email=email)
logger.warning("login_failed", email=email, attempt=failed_count)
logger.error("ai_api_error", lesson_id=str(lesson_id), error=str(e))
```

### Dependency Injection
- **Bắt buộc** dùng FastAPI `Depends()` — không khởi tạo service/repository trực tiếp
- Mỗi module có factory function:
```python
def get_analytics_service(
    db: AsyncSession = Depends(get_db),
) -> AnalyticsService:
    course_repo = CourseRepository(db)
    enrollment_repo = EnrollmentRepository(db)
    return AnalyticsService(course_repo, enrollment_repo)
```

---

## 5. Forbidden (KHÔNG được làm)

| ❌ Hành vi bị cấm | Lý do |
|---|---|
| Hardcode secret/credential trong source code | Bảo mật — dùng `.env` + Pydantic Settings |
| Dùng `print()` thay cho `logger` | Không có structured log, không trace được |
| Commit trực tiếp vào `main`/`master` | Phải qua PR + review |
| Alter table thủ công bằng SQL | Phải dùng Alembic migration |
| Magic Number (số cứng không giải thích) | Dùng constant: `DROP_OFF_THRESHOLD = 0.20` |
| God Object (class làm quá nhiều việc) | Tách theo Single Responsibility |
| Copy-paste logic giữa modules | Extract thành shared utility |
| Catch exception rồi bỏ qua (`except: pass`) | Phải log hoặc re-raise |
| Query DB trong Router | Phải đi qua Service → Repository |
| Trả stack trace trong API response | Dùng Global Exception Handler |

---

## 6. Anti-patterns cần tránh

| Anti-pattern | Giải pháp |
|---|---|
| **N+1 Query** | Dùng `joinedload()` / `selectinload()` trong SQLAlchemy |
| **Fat Controller** | Router chỉ validate + gọi service, không chứa business logic |
| **Anemic Domain Model** | Service chứa logic, nhưng Invariants nằm trong Model |
| **Circular Import** | Dùng Dependency Injection, tránh import trực tiếp giữa modules |
| **Hardcoded Config** | Mọi config đọc từ `.env` qua Pydantic `BaseSettings` |

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*