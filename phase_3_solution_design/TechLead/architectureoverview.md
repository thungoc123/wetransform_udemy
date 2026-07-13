# Architecture Overview — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: Hệ thống được thiết kế như thế nào?
> Nguồn gốc: [UserStories.md](../../../phase_2_story_definition/UserStories.md), [APISpec.md](../../../phase_2_story_definition/APISpec.md), [businessdomain.md](../../../phase_1_discovery/BC/businessdomain.md)

---

## 1. System Architecture

### Kiến trúc: Modular Monolith

**Tại sao chọn Modular Monolith:**
- Team chỉ có 4 người → Microservices quá tốn overhead (mỗi service cần deploy, monitor riêng)
- MVP chỉ có 6 tính năng, 10 API endpoints → 1 codebase đủ quản lý
- Dữ liệu MVP nhỏ (3 khóa, 2.600 học viên) → không cần scale từng service riêng
- **Nhưng** chia module rõ ràng → sau có thể tách ra Microservices khi cần

**KHÔNG chọn:**
- ~~Monolith thuần~~ — code sẽ lộn xộn khi thêm tính năng mới
- ~~Microservices~~ — overhead quá lớn cho team 4 người

---

## 2. Components (Service/Module)

> 5 Module được suy ra trực tiếp từ 6 User Stories

| Module | Chịu trách nhiệm | User Story liên quan | API Endpoints |
|---|---|---|---|
| **auth** | Đăng nhập, JWT, khóa tài khoản | US-001 | POST /auth/login |
| **data_import** | Kết nối Udemy API, upload CSV/XLSX, parse dữ liệu | US-002 | POST /data/udemy-connection, POST /data/upload |
| **analytics** | Dashboard tổng quan, drop-off analysis, timeline | US-003, US-004 | GET /courses, GET /dashboard, GET /drop-off-analysis |
| **ai_insights** | Gọi LLM, sinh hypothesis, quản lý recommendation | US-005 | GET /ai-insights, POST /recommendations/action |
| **intervention** | Danh sách at-risk students, gửi reminder, theo dõi re-engagement | US-006 | GET /at-risk-students, POST /send-reminder |

### Giao tiếp giữa các module:
- **Trong cùng process** — gọi trực tiếp qua Python import (Modular Monolith)
- **Qua Celery Queue** — cho background jobs: parse file, gọi AI API, gửi email
- **KHÔNG** dùng REST giữa các module nội bộ (chỉ dùng REST cho FE ↔ BE)

---

## 3. Data Flow

### 3.1 Request Flow (Synchronous)
```
Client (React)
    │
    ▼
FastAPI Router (validate input bằng Pydantic)
    │
    ▼
Service Layer (business logic, invariants check)
    │
    ▼
Repository Layer (SQLAlchemy query)
    │
    ▼
PostgreSQL Database
```

### 3.2 Background Job Flow (Asynchronous)
```
FastAPI Router
    │
    ▼
Service Layer
    │  enqueue task
    ▼
Redis (Message Broker)
    │
    ▼
Celery Worker
    ├── Parse CSV/XLSX → Write to PostgreSQL      (US-002)
    ├── Call OpenAI API → Write AI Insights to DB  (US-005)
    └── Send Email via SMTP/SendGrid               (US-006)
```

### 3.3 Có Event / Message Queue không?
- **Có** — dùng **Celery + Redis** cho 3 loại background job:
  1. `parse_uploaded_file()` — US-002: File CSV có thể lớn, parse mất > 30s → chạy nền
  2. `generate_ai_insights()` — US-005: Gọi OpenAI API mất 5-10s → chạy nền
  3. `send_email_task()` — US-006: Gửi email hàng loạt cho nhiều học viên → chạy nền
- **Không** dùng Event Sourcing hay Kafka (quá phức tạp cho MVP)

---

## 4. Sequence Diagrams

### 4.1 Luồng Login (US-001)
```
Teacher → Router /auth/login
    → AuthService.authenticate(email, password)
        → TeacherRepository.get_by_email(email)
        → [Nếu sai] Tăng failed_login_count
            → [Nếu >= 5] Set locked_until = NOW() + 15min → Return 423
            → [Nếu < 5] Return 401
        → [Nếu đúng] Reset failed_login_count = 0
        → Generate JWT token
    → Return 200 {token, teacherId, name}
```

### 4.2 Luồng Upload CSV (US-002)
```
Teacher → Router /data/upload (file: CSV)
    → Validate file extension (.csv/.xlsx)
    → DataImportService.create_import(file, teacher_id)
        → Save file to disk
        → INSERT data_imports (status='pending')
        → Celery.enqueue(parse_uploaded_file, import_id)
    → Return 200 {importId, status: "processing"}

[Background - Celery Worker]
    → Load file from disk
    → pandas.read_csv() / read_excel()
    → Validate columns (check required fields)
    → [Nếu sai format] UPDATE data_imports SET status='failed'
    → [Nếu đúng]
        → Ẩn danh hóa email → masked_name
        → INSERT courses, modules, lessons, student_enrollments, learning_activities
        → UPDATE data_imports SET status='success'
```

### 4.3 Luồng Dashboard (US-003)
```
Teacher → Router /courses/{courseId}/dashboard
    → AnalyticsService.get_dashboard(courseId, teacherId)
        → Verify teacher owns course (403 if not)
        → COUNT students GROUP BY status → activeStudents, inactiveStudents, atRiskStudents
        → AVG(is_completed) → completionRate
        → Calculate dropOffRate
    → Return 200 {completionRate, dropOffRate, activeStudents, ...}
```

### 4.4 Luồng Drop-off Analysis (US-004)
```
Teacher → Router /courses/{courseId}/drop-off-analysis
    → AnalyticsService.get_drop_off(courseId)
        → SELECT lessons ORDER BY order_index
        → For each lesson:
            → Calculate drop_off_rate
            → Set has_warning = true if > 0.20
            → [Nếu type=video AND student_count >= 30]
                → SELECT video_stop_at_second, COUNT(*) GROUP BY second
                → Build timelineAnalysis
    → Return 200 {modules[{lessons[{dropOffRate, hasWarning, timelineAnalysis}]}]}
```

### 4.5 Luồng AI Insights (US-005)
```
Teacher → Router /courses/{courseId}/lessons/{lessonId}/ai-insights
    → AIInsightService.get_insights(lessonId)
        → Check if insights already cached in DB
        → [Nếu có] Return cached insights
        → [Nếu chưa]
            → Check lesson.student_count >= 30 (404 if not)
            → Aggregate learning_activities stats
            → Build prompt: "Bài học X có drop-off 35%, 60% dừng ở phút 4:30..."
            → Call OpenAI GPT-4o API
            → Parse response → hypotheses + recommendations
            → INSERT ai_insights + recommendations
        → Return 200 {insights, recommendations, disclaimer: "Chỉ mang tính tham khảo"}
```

### 4.6 Luồng Send Reminder (US-006)
```
Teacher → Router /send-reminder {studentIds, messageBody}
    → InterventionService.send_reminders(studentIds, messageBody, teacherId)
        → For each studentId:
            → Check cooldown: SELECT FROM reminder_logs WHERE sent_at > NOW() - 7 days
            → [Nếu đã gửi trong 7 ngày] Add to failures: "Cooldown active"
            → [Nếu chưa]
                → INSERT reminder_logs (status='pending')
                → Celery.enqueue(send_email_task, reminderId)
    → Return 200 {sentCount, failedCount, failures}

[Background - Celery Worker]
    → Decrypt student email
    → Replace placeholders: {student_name}, {lesson_name}, {best_practice_tip}
    → Send email via SMTP/SendGrid
    → [Success] UPDATE status='sent', tracking_expires_at = NOW() + 7 days
    → [Failed] UPDATE status='failed', failure_reason='...'
```

---

## 5. External Integration

| Hệ thống bên ngoài | Mục đích | API/Protocol | Bắt buộc? |
|---|---|---|---|
| **Udemy Instructor API** | Lấy dữ liệu khóa học, học viên, tiến trình | REST API + OAuth | Tùy chọn (có thể dùng file upload thay thế) |
| **OpenAI API** | Sinh AI Insights (hypothesis + recommendation) | REST API (GPT-4o) | Bắt buộc cho US-005 |
| **SMTP / SendGrid** | Gửi email reminder cho học viên | SMTP / REST API | Bắt buộc cho US-006 |

---

## 6. Constraints (Nguyên tắc kiến trúc)

### Luôn phải tuân thủ:
1. **Layered Architecture:** Router → Service → Repository → DB. Không bỏ qua layer
2. **Module Isolation:** Module A không truy cập trực tiếp Repository của Module B. Phải đi qua Service
3. **Background cho I/O nặng:** Mọi thao tác > 5s (parse file, gọi AI, gửi email) phải chạy qua Celery
4. **Stateless API:** Không lưu session trên server. Dùng JWT token cho mọi request
5. **Soft Delete:** Không xóa dữ liệu vật lý. Set `deleted_at = NOW()`

### Pattern luôn áp dụng:
- **Repository Pattern** — cho mọi database access
- **Dependency Injection** — FastAPI `Depends()`
- **Standard Response Format** — mọi API trả `{"success", "data", "message", "error_code"}`
- **Correlation ID** — gán cho mỗi request trong middleware, truyền qua log

---

## 7. System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        CLIENT (React)                        │
│  Login │ Dashboard │ Drop-off Chart │ AI Panel │ Reminder    │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTP/REST (JWT Bearer)
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                   FASTAPI APPLICATION                        │
│                                                              │
│  ┌──────────┐ ┌──────────────┐ ┌───────────┐ ┌────────────┐│
│  │   auth   │ │ data_import  │ │ analytics │ │ai_insights ││
│  │          │ │              │ │           │ │            ││
│  │ router   │ │ router       │ │ router    │ │ router     ││
│  │ service  │ │ service      │ │ service   │ │ service    ││
│  │ repo     │ │ repo         │ │ repo      │ │ repo       ││
│  │ models   │ │ models       │ │ models    │ │ models     ││
│  │ schemas  │ │ tasks.py ◄───┼─┼───────────┼─┤ tasks.py   ││
│  └──────────┘ └──────────────┘ └───────────┘ └────────────┘│
│                                               ┌────────────┐│
│                   shared/                     │intervention││
│                   exceptions.py               │ router     ││
│                   response.py                 │ service    ││
│                   middleware.py                │ repo       ││
│                   security.py                 │ tasks.py   ││
│                   encryption.py               └────────────┘│
└───────────┬────────────────────────────┬─────────────────────┘
            │                            │
            ▼                            ▼
┌───────────────────┐        ┌──────────────────────┐
│   PostgreSQL 16   │        │   Redis 7 + Celery   │
│                   │        │                      │
│ 11 tables         │        │ Task Queue:          │
│ UUID primary keys │        │ - parse CSV          │
│ Soft delete       │        │ - call OpenAI        │
│                   │        │ - send email         │
│                   │        │                      │
│                   │        │ Cache:               │
│                   │        │ - Dashboard results  │
└───────────────────┘        └──────────────────────┘
                                      │
                          ┌───────────┼───────────┐
                          ▼           ▼           ▼
                    ┌──────────┐ ┌────────┐ ┌──────────┐
                    │ Udemy API│ │ OpenAI │ │ SendGrid │
                    │          │ │ GPT-4o │ │ / SMTP   │
                    └──────────┘ └────────┘ └──────────┘
```

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*
