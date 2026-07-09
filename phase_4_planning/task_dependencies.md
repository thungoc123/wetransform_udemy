# Task Breakdown & Dependencies — Nền tảng AI Learning Analytics

> Nguồn gốc: [UserStories.md](../phase_2_story_definition/UserStories.md), [APISpec.md](../phase_2_story_definition/APISpec.md), [architectureoverview.md](../phase_3_solution_design/TechLead/architectureoverview.md)

---

## Tại sao phải có Dependencies Graph

- Chỉ tạo các task có thể bắt đầu ngay.
- Tự xác định task nào đang bị Blocked.
- Phân công song song các task không phụ thuộc nhau.
- Ước lượng critical path (đường găng) để tối ưu tiến độ.
- Hiển thị biểu đồ phụ thuộc giữa các task trong dashboard.

---

## Đầu vào để tạo ra Dependencies Graph

- Task Breakdown (bên dưới)
- Artifact Dependency: API cần DB model → DB task trước API task
- Domain Dependency: Login trước mọi thứ → US-001 là gốc
- Technical Dependency: Celery worker cần Redis → Infrastructure task trước
- UI Dependency: Frontend cần API response format → Backend task trước Frontend task

---

## Dependency Graph

```
INFRA-001 (Project Setup)
    │
    ├── AUTH-001 (Teacher DB Model)
    │       │
    │       ├── AUTH-002 (Login API + JWT)
    │       │       │
    │       │       └── DATA-001 (Course/Lesson/Student Models)
    │       │               │
    │       │               ├── DATA-002 (Upload CSV API)
    │       │               │       │
    │       │               │       └── DATA-003 (Celery Parse Worker)
    │       │               │               │
    │       │               │               ├── DASH-001 (Dashboard API)
    │       │               │               │       │
    │       │               │               │       ├── DROP-001 (Drop-off Analysis API)
    │       │               │               │       │       │
    │       │               │               │       │       ├── DROP-002 (Timeline Analysis)
    │       │               │               │       │       │
    │       │               │               │       │       └── AI-001 (AI Insight API + LLM)
    │       │               │               │       │               │
    │       │               │               │       │               └── AI-002 (Recommendation Action API)
    │       │               │               │       │
    │       │               │               │       └── REM-001 (At-risk Students API)
    │       │               │               │               │
    │       │               │               │               └── REM-002 (Send Reminder API)
    │       │               │               │                       │
    │       │               │               │                       └── REM-003 (7-day Tracking)
    │       │               │               │
    │       │               │               └── DATA-004 (Udemy Connect API)  [Song song với DASH]
    │       │               │
    │       │               └── [Song song] DATA-004 (Udemy Connect API)
    │       │
    │       └── AUTH-003 (Account Lock Logic)  [Song song với DATA]
    │
    └── FE-001 (React Project Setup)  [Song song với toàn bộ Backend]
            │
            ├── FE-002 (Login Page)
            │       │
            │       └── FE-003 (Dashboard Page)
            │               │
            │               ├── FE-004 (Drop-off Chart Page)
            │               │       │
            │               │       └── FE-005 (AI Insights Panel)
            │               │
            │               └── FE-006 (Reminder Page)
```

---

## Critical Path (Đường găng)

```
INFRA-001 → AUTH-001 → AUTH-002 → DATA-001 → DATA-002 → DATA-003 → DASH-001 → DROP-001 → AI-001
```

**Tổng critical path: 51 Story Points**

---

## Parallel Tracks (Làm song song)

| Track | Tasks | Ai làm |
|---|---|---|
| **Track A: Backend Core** | INFRA → AUTH → DATA → DASH → DROP → AI → REM | Backend Developer |
| **Track B: Frontend** | FE-001 → FE-002 → FE-003 → FE-004 → FE-005 → FE-006 | Frontend Developer (dùng mock API) |
| **Track C: Song song** | AUTH-003, DATA-004 (không block nhau) | Ai rảnh |

---

## Task Breakdown chi tiết

---

# Feature: Authentication (US-001)

## Description
Giáo viên đăng nhập hệ thống bằng email + mật khẩu, nhận JWT token. Tài khoản bị khóa 15 phút sau 5 lần sai.

---

### TASK INFRA-001

**Title:** Project Setup — Docker + PostgreSQL + Redis + Celery

**Role:** DevOps / Backend

**Category:** DevOps

**Priority:** High

**Estimate:** 5 SP

**Depends On:** None

**Deliverables:**
- Docker Compose file (4 services: api, db, redis, celery)
- FastAPI skeleton (main.py, config.py, database.py)
- Alembic init
- .env.example
- requirements.txt
- Dockerfile
- pyproject.toml (Black + Ruff config)

**Definition of Done:**
- [ ] `docker-compose up` chạy được 4 services
- [ ] FastAPI trả về `{"status": "ok"}` tại GET /health
- [ ] Alembic kết nối được PostgreSQL
- [ ] Celery worker connect được Redis
- [ ] Code format pass Black + Ruff

**Description:**
Khởi tạo toàn bộ infrastructure cho dự án. Tạo skeleton FastAPI, cấu hình Docker Compose với PostgreSQL 16, Redis 7, Celery worker. Cài đặt Alembic cho migration. Setup linter và formatter.

---

### TASK AUTH-001

**Title:** Teacher Database Model + Migration

**Role:** Backend

**Category:** Database

**Priority:** High

**Estimate:** 2 SP

**Depends On:** INFRA-001

**Deliverables:**
- SQLAlchemy model: Teacher (trong app/modules/auth/models.py)
- Alembic migration: create_teachers table
- Shared utilities: security.py (password hash), encryption.py

**Definition of Done:**
- [ ] Migration chạy thành công, tạo bảng `teachers`
- [ ] Có UUID PK, audit columns (created_at, updated_at, deleted_at)
- [ ] Password hash function hoạt động (bcrypt)
- [ ] Unit test cho hash/verify password

**Description:**
Tạo SQLAlchemy model Teacher với đầy đủ fields từ Domain Model. Tạo migration Alembic. Implement bcrypt password hashing trong shared/security.py.

---

### TASK AUTH-002

**Title:** Login API + JWT Token Generation

**Role:** Backend

**Category:** API

**Priority:** High

**Estimate:** 5 SP

**Depends On:** AUTH-001

**Deliverables:**
- Router: POST /api/v1/auth/login
- Service: AuthService.authenticate()
- Repository: TeacherRepository.get_by_email()
- Schemas: LoginRequest, LoginResponse
- JWT token generation (shared/security.py)
- Global exception handler (shared/exceptions.py)
- Standard response wrapper (shared/response.py)
- Middleware: CorrelationIdMiddleware

**Definition of Done:**
- [ ] Login thành công trả 200 + JWT token
- [ ] Sai password trả 401
- [ ] Thiếu field trả 400
- [ ] Swagger docs hiển thị đúng
- [ ] Unit test cover happy path + error cases
- [ ] Structured log ghi nhận login attempt

**Description:**
Implement endpoint login theo API Spec đã chốt. Setup global exception handler, standard response format, correlation ID middleware.

---

### TASK AUTH-003

**Title:** Account Lock Logic (5 lần sai → khóa 15 phút)

**Role:** Backend

**Category:** Backend

**Priority:** Medium

**Estimate:** 3 SP

**Depends On:** AUTH-002

**Deliverables:**
- Logic tăng failed_login_count trong AuthService
- Logic set locked_until = NOW() + 15 min
- Logic kiểm tra locked_until trước khi authenticate
- AccountLockedException (423)

**Definition of Done:**
- [ ] Sau 5 lần sai → trả 423 Locked
- [ ] Sau 15 phút → cho phép đăng nhập lại
- [ ] Đăng nhập thành công → reset failed_login_count = 0
- [ ] Unit test cover lock/unlock flow

**Description:**
Bổ sung business rule khóa tài khoản vào AuthService. Kiểm tra locked_until trước mỗi lần authenticate.

---

# Feature: Data Import (US-002)

## Description
Giáo viên kết nối API Udemy hoặc upload file CSV/XLSX. Hệ thống parse dữ liệu, ẩn danh hóa email, tạo records Course/Lesson/Student.

---

### TASK DATA-001

**Title:** Course, Module, Lesson, StudentEnrollment, LearningActivity Models + Migration

**Role:** Backend

**Category:** Database

**Priority:** High

**Estimate:** 5 SP

**Depends On:** AUTH-002

**Deliverables:**
- SQLAlchemy models: Course, Module, Lesson, StudentEnrollment, LearningActivity, DataImport, UdemyConnection
- Alembic migration cho tất cả bảng
- FK constraints + indexes theo database standards

**Definition of Done:**
- [ ] Migration tạo thành công 7 bảng mới
- [ ] FK constraints hoạt động (CASCADE)
- [ ] Indexes được tạo (13 indexes theo DB standards)
- [ ] Soft delete columns có mặt

**Description:**
Tạo toàn bộ data models còn lại từ Domain Model. Đây là task lớn nhất về database, tạo nền tảng cho mọi feature sau.

---

### TASK DATA-002

**Title:** Upload CSV/XLSX API

**Role:** Backend

**Category:** API

**Priority:** High

**Estimate:** 8 SP

**Depends On:** DATA-001

**Deliverables:**
- Router: POST /api/v1/data/upload
- Service: DataImportService.create_import()
- Repository: DataImportRepository
- Schemas: UploadResponse
- Parser: parser.py (CSV/XLSX parsing với pandas)
- Anonymization: mask_name() utility
- Email encryption: encrypt_aes()

**Definition of Done:**
- [ ] Upload CSV → trả 200 {importId, status: "processing"}
- [ ] File sai format → trả 400
- [ ] File quá lớn → trả 413
- [ ] parser.py parse đúng dữ liệu Udemy mẫu
- [ ] Email được mã hóa, tên được ẩn danh
- [ ] Unit test cho parser + anonymization

**Description:**
Implement upload file API + CSV/XLSX parser. Parser cần xử lý ẩn danh hóa email và mask tên học viên trước khi lưu DB.

---

### TASK DATA-003

**Title:** Celery Worker — Parse Uploaded File (Background)

**Role:** Backend

**Category:** Backend

**Priority:** High

**Estimate:** 5 SP

**Depends On:** DATA-002

**Deliverables:**
- Celery task: parse_uploaded_file()
- Logic: validate columns → parse → anonymize → INSERT batch records
- Update data_imports status (processing → success/failed)

**Definition of Done:**
- [ ] Celery task được trigger khi upload file
- [ ] Parse thành công → tạo Course, Lesson, StudentEnrollment, LearningActivity
- [ ] Parse thất bại → update status='failed' + error_message
- [ ] Integration test chạy end-to-end

**Description:**
Tách logic parse file sang Celery worker để tránh timeout. Worker đọc file, validate, parse bằng pandas, INSERT batch vào DB.

---

### TASK DATA-004

**Title:** Udemy API Connection

**Role:** Backend

**Category:** API

**Priority:** Medium

**Estimate:** 5 SP

**Depends On:** DATA-001

**Deliverables:**
- Router: POST /api/v1/data/udemy-connection
- Service: UdemyConnectionService
- Repository: UdemyConnectionRepository
- Logic mã hóa client_id, client_secret trước khi lưu

**Definition of Done:**
- [ ] Kết nối thành công → trả 200 {connectionId, status: "connected"}
- [ ] Thông tin sai → trả 401
- [ ] Credentials được mã hóa AES trước khi lưu DB
- [ ] Unit test cover

**Description:**
Implement Udemy API connection endpoint. Mã hóa credentials trước khi lưu DB.

---

# Feature: Analytics (US-003, US-004)

## Description
Dashboard tổng quan khóa học + phân tích điểm dừng (drop-off funnel chart + video timeline).

---

### TASK DASH-001

**Title:** Dashboard Overview API

**Role:** Backend

**Category:** API

**Priority:** High

**Estimate:** 5 SP

**Depends On:** DATA-003

**Deliverables:**
- Router: GET /api/v1/courses, GET /api/v1/courses/{courseId}/dashboard
- Service: AnalyticsService.get_dashboard()
- Repository: aggregate queries (COUNT, AVG, GROUP BY status)
- Schemas: CourseListResponse, DashboardResponse
- Authorization check: verify teacher owns course

**Definition of Done:**
- [ ] GET /courses trả danh sách khóa học của teacher đang đăng nhập
- [ ] GET /dashboard trả completionRate, dropOffRate, activeStudents, inactiveStudents, atRiskStudents
- [ ] Teacher không sở hữu course → 403
- [ ] Course không có data → empty state response
- [ ] Unit test cho aggregate calculations

**Description:**
Implement dashboard API với các aggregate queries tính toán KPIs. Kiểm tra quyền sở hữu course qua teacher_id.

---

### TASK DROP-001

**Title:** Drop-off Analysis API

**Role:** Backend

**Category:** API

**Priority:** High

**Estimate:** 8 SP

**Depends On:** DASH-001

**Deliverables:**
- Router: GET /api/v1/courses/{courseId}/drop-off-analysis
- Service: AnalyticsService.get_drop_off_analysis()
- Repository: query lessons + calculate drop_off_rate per lesson
- Logic: set has_warning = true if drop_off_rate > 0.20
- Logic: filter student_count >= 30

**Definition of Done:**
- [ ] Trả danh sách modules → lessons với dropOffRate
- [ ] Lessons có drop-off > 20% → hasWarning = true
- [ ] Lessons có student_count < 30 → không phân tích chi tiết
- [ ] Kết quả sắp xếp theo order_index
- [ ] Unit test cho threshold logic

**Description:**
Implement drop-off funnel analysis. Tính drop-off rate cho từng lesson, đánh dấu warning nếu vượt ngưỡng 20%.

---

### TASK DROP-002

**Title:** Video Timeline Analysis

**Role:** Backend

**Category:** Backend

**Priority:** Medium

**Estimate:** 5 SP

**Depends On:** DROP-001

**Deliverables:**
- Logic: aggregate video_stop_at_second → heatmap data
- Thêm timelineAnalysis vào DropOffResponse (chỉ cho video lessons)

**Definition of Done:**
- [ ] Video lessons hiển thị mốc giây dừng nhiều nhất
- [ ] Non-video lessons chỉ hiển thị tỷ lệ chung
- [ ] Unit test cho timeline aggregation

**Description:**
Bổ sung timeline analysis cho video lessons. Tổng hợp video_stop_at_second từ learning_activities để xác định mốc thời gian học viên dừng nhiều nhất.

---

# Feature: AI Insights (US-005)

## Description
AI phân tích nguyên nhân drop-off cao và đề xuất hành động cải thiện cho giáo viên.

---

### TASK AI-001

**Title:** AI Insight API + LLM Integration

**Role:** AI Engineering

**Category:** Backend

**Priority:** High

**Estimate:** 8 SP

**Depends On:** DROP-001

**Deliverables:**
- Router: GET /api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights
- Service: AIInsightService.get_insights()
- Repository: AiInsightRepository
- prompt_builder.py: build LLM prompt từ lesson stats
- Celery task: generate_insights() — gọi OpenAI API
- Models: AiInsight, Recommendation
- Disclaimer text trong response

**Definition of Done:**
- [ ] Trả insights + recommendations khi lesson có đủ data
- [ ] Trả 404 khi lesson có student_count < 30
- [ ] Response kèm disclaimer
- [ ] Prompt builder tạo prompt có dữ liệu thống kê thực
- [ ] Celery task gọi OpenAI API thành công
- [ ] Raw prompt + response được lưu để audit
- [ ] Unit test cho prompt builder + service logic

**Description:**
Implement AI insight generation. Build prompt từ dữ liệu thống kê thực (drop-off rate, video stop points), gọi OpenAI GPT-4o, parse response thành hypotheses + recommendations.

---

### TASK AI-002

**Title:** Recommendation Action API (Applied/Ignored)

**Role:** Backend

**Category:** API

**Priority:** Medium

**Estimate:** 3 SP

**Depends On:** AI-001

**Deliverables:**
- Router: POST /recommendations/{recommendationId}/action
- Service: update_recommendation()
- Logic: ignored → ẩn khỏi UI + ghi feedback

**Definition of Done:**
- [ ] Applied → update status
- [ ] Ignored → update status + ẩn khỏi danh sách
- [ ] Action không hợp lệ → 400
- [ ] Recommendation không tồn tại → 404
- [ ] Unit test cover

**Description:**
Implement endpoint để giáo viên phản hồi đề xuất AI. Ghi nhận feedback để cải thiện AI trong tương lai.

---

# Feature: Intervention (US-006)

## Description
Gửi nhắc nhở cá nhân hóa cho học viên at-risk/inactive, sử dụng message template từ best practice.

---

### TASK REM-001

**Title:** At-risk Students API + Message Template

**Role:** Backend

**Category:** API

**Priority:** High

**Estimate:** 5 SP

**Depends On:** DASH-001

**Deliverables:**
- Router: GET /api/v1/courses/{courseId}/lessons/{lessonId}/at-risk-students
- Service: InterventionService.get_at_risk_students()
- Repository: filter students by status
- template_builder.py: build message template với placeholders
- Logic: canSendReminder = false nếu đã gửi trong 7 ngày

**Definition of Done:**
- [ ] Trả danh sách students at-risk/inactive
- [ ] Tên được ẩn danh hóa (maskedName)
- [ ] canSendReminder chính xác (check 7-day cooldown)
- [ ] defaultMessageTemplate có placeholders
- [ ] Unit test cover cooldown logic

**Description:**
Implement at-risk students listing + message template builder. Template được sinh từ best practice analysis.

---

### TASK REM-002

**Title:** Send Reminder API + Email Service

**Role:** Backend

**Category:** API

**Priority:** High

**Estimate:** 8 SP

**Depends On:** REM-001

**Deliverables:**
- Router: POST /api/v1/courses/{courseId}/lessons/{lessonId}/send-reminder
- Service: InterventionService.send_reminders()
- Repository: save_reminder_log(), check_cooldown()
- Celery task: send_email_task()
- Email integration (SMTP/SendGrid)

**Definition of Done:**
- [ ] Gửi thành công → trả sentCount
- [ ] Học viên đã nhận reminder 7 ngày qua → trả trong failures
- [ ] Danh sách rỗng → 400
- [ ] Email được gửi qua Celery (không block request)
- [ ] ReminderLog được tạo trong DB
- [ ] Integration test cho email flow

**Description:**
Implement send reminder API + Celery email worker. Kiểm tra 7-day cooldown trước khi gửi. Ghi nhận reminder log để tracking.

---

### TASK REM-003

**Title:** 7-day Re-engagement Tracking

**Role:** Backend

**Category:** Backend

**Priority:** Medium

**Estimate:** 3 SP

**Depends On:** REM-002

**Deliverables:**
- Celery periodic task: check_reengagement()
- Logic: nếu student quay lại học trong 7 ngày sau reminder → update status = 'reengaged'
- Update dashboard stats

**Definition of Done:**
- [ ] Celery beat chạy periodic check
- [ ] Student quay lại → status updated
- [ ] Dashboard cập nhật số liệu re-engaged
- [ ] Unit test cover

**Description:**
Implement tracking logic sau khi gửi reminder. Celery periodic task kiểm tra activity trong 7 ngày.

---

# Feature: Frontend

## Description
Giao diện React cho giáo viên: Login, Dashboard, Drop-off Chart, AI Insights Panel, Reminder Page.

---

### TASK FE-001

**Title:** React Project Setup

**Role:** Frontend

**Category:** Frontend

**Priority:** High

**Estimate:** 3 SP

**Depends On:** INFRA-001

**Deliverables:**
- Vite + React 18 project
- React Router setup (routes: /login, /dashboard, /courses/:id)
- Axios instance với JWT interceptor
- Ant Design setup
- Layout component (Sidebar + Header)

**Definition of Done:**
- [ ] `npm run dev` chạy được
- [ ] Routing hoạt động
- [ ] Axios tự động gắn JWT token
- [ ] Layout skeleton hiển thị

---

### TASK FE-002

**Title:** Login Page

**Role:** Frontend

**Category:** Frontend

**Priority:** High

**Estimate:** 3 SP

**Depends On:** FE-001

**Deliverables:**
- Login form (email + password)
- Error handling (sai mật khẩu, account locked)
- Redirect to dashboard sau login thành công
- Lưu JWT token vào localStorage

**Definition of Done:**
- [ ] Form validate email + password
- [ ] Hiển thị error message từ API
- [ ] Login thành công → redirect /dashboard

---

### TASK FE-003

**Title:** Dashboard Page

**Role:** Frontend

**Category:** Frontend

**Priority:** High

**Estimate:** 8 SP

**Depends On:** FE-002

**Deliverables:**
- Course list selector
- KPI cards (Completion Rate, Drop-off Rate, Active/Inactive/At-risk counts)
- Empty state khi chưa có data
- Recharts bar/pie charts

**Definition of Done:**
- [ ] Hiển thị đúng 5 KPIs từ API
- [ ] Course selector hoạt động
- [ ] Empty state hiển thị khi chưa import data
- [ ] Charts render đúng data

---

### TASK FE-004

**Title:** Drop-off Analysis Chart Page

**Role:** Frontend

**Category:** Frontend

**Priority:** High

**Estimate:** 8 SP

**Depends On:** FE-003

**Deliverables:**
- Funnel chart (biểu đồ phễu) cho modules → lessons
- Warning highlight (đỏ/cam) cho lessons drop-off > 20%
- Video timeline chart (heatmap mốc giây dừng)
- Click vào lesson → xem chi tiết

**Definition of Done:**
- [ ] Funnel chart hiển thị đúng drop-off data
- [ ] Lessons warning được highlight
- [ ] Video timeline chart hoạt động
- [ ] Responsive trên desktop

---

### TASK FE-005

**Title:** AI Insights Panel

**Role:** Frontend

**Category:** Frontend

**Priority:** Medium

**Estimate:** 5 SP

**Depends On:** FE-004

**Deliverables:**
- Hypothesis cards (nguyên nhân + confidence score)
- Recommendation list (với nút Applied/Ignored)
- Disclaimer text
- Loading state khi AI đang xử lý

**Definition of Done:**
- [ ] Hiển thị hypotheses + recommendations
- [ ] Nút Applied/Ignored hoạt động (gọi API)
- [ ] Disclaimer hiển thị rõ ràng
- [ ] Loading spinner khi chờ AI

---

### TASK FE-006

**Title:** Reminder Page

**Role:** Frontend

**Category:** Frontend

**Priority:** Medium

**Estimate:** 5 SP

**Depends On:** FE-003

**Deliverables:**
- At-risk student list (masked names)
- Message template editor (với placeholders)
- Send button + confirmation dialog
- Success/failure feedback

**Definition of Done:**
- [ ] Hiển thị danh sách at-risk students
- [ ] canSendReminder = false → disable checkbox
- [ ] Message template editable
- [ ] Gửi thành công → hiển thị sentCount/failedCount

---

## Tổng kết

| Category | Số task | Story Points |
|---|---|---|
| Infrastructure | 1 | 5 |
| Backend Auth | 3 | 10 |
| Backend Data | 4 | 23 |
| Backend Analytics | 3 | 18 |
| Backend AI | 2 | 11 |
| Backend Intervention | 3 | 16 |
| Frontend | 6 | 32 |
| **Tổng** | **22 tasks** | **115 SP** |

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*
