# Domain Model — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: Các đối tượng nghiệp vụ liên quan với nhau như thế nào?
> Nguồn gốc: [businessdomain.md](../../../phase_1_discovery/BC/businessdomain.md), [UserStories.md](../../../phase_2_story_definition/UserStories.md), [APISpec.md](../../../phase_2_story_definition/APISpec.md)

---

## 1. Business Entities

### 1.1 Teacher (Giáo viên)

> Nguồn: businessdomain.md mục 2 — "Teacher / Course Creator: Người dùng chính"
> API: POST /api/v1/auth/login → trả về teacherId, name, token

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | Chuẩn DB — tránh lộ tổng số user |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | API Login input: `email (string, required)` |
| `password_hash` | VARCHAR(255) | NOT NULL | Business Rule US-001: "Mật khẩu phải được mã hóa khi lưu trữ" |
| `name` | VARCHAR(255) | NOT NULL | API Login output: `name (string)` |
| `failed_login_count` | INTEGER | DEFAULT 0 | Business Rule US-001: "Sau 5 lần đăng nhập sai → khóa 15 phút" |
| `locked_until` | TIMESTAMP | NULLABLE | Business Rule US-001: Thời điểm hết khóa tài khoản |
| `created_at` | TIMESTAMP | NOT NULL | Audit column |
| `updated_at` | TIMESTAMP | NOT NULL | Audit column |
| `deleted_at` | TIMESTAMP | NULLABLE | Soft delete |

---

### 1.2 UdemyConnection (Kết nối API Udemy)

> Nguồn: businessdomain.md mục 2 — "Data Import / Udemy Connection"
> API: POST /api/v1/data/udemy-connection → trả về connectionId, status, connectedAt

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `connectionId` |
| `teacher_id` | UUID | FK → teachers.id, NOT NULL | Chỉ giáo viên đăng nhập mới được kết nối |
| `client_id_encrypted` | TEXT | NOT NULL | API input: `clientId` + Business Rule: "mã hóa dữ liệu nhạy cảm" |
| `client_secret_encrypted` | TEXT | NOT NULL | API input: `clientSecret` + Business Rule: "mã hóa dữ liệu nhạy cảm" |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | API output: `status ("connected")` |
| `connected_at` | TIMESTAMP | NULLABLE | API output: `connectedAt` |
| `last_sync_at` | TIMESTAMP | NULLABLE | US-002 AC-01: "dữ liệu tự động đồng bộ theo chu kỳ" |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |
| `deleted_at` | TIMESTAMP | NULLABLE | Soft delete |

---

### 1.3 DataImport (File upload từ Udemy)

> Nguồn: US-002 luồng Upload File
> API: POST /api/v1/data/upload → trả về importId, status, fileName

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `importId` |
| `teacher_id` | UUID | FK → teachers.id, NOT NULL | Người upload phải đã đăng nhập |
| `file_name` | VARCHAR(255) | NOT NULL | API output: `fileName` |
| `file_path` | TEXT | NOT NULL | Lưu vị trí file trên server |
| `file_size_bytes` | BIGINT | NOT NULL | Kiểm tra giới hạn `413 Payload Too Large` |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | API output: `status ("processing")` |
| `error_message` | TEXT | NULLABLE | API error: "file sai định dạng/thiếu cột" |
| `row_count` | INTEGER | NULLABLE | Số dòng dữ liệu đã parse |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |

---

### 1.4 Course (Khóa học)

> Nguồn: businessdomain.md mục 2 — "Course: Khóa học được phân tích"
> API: GET /api/v1/courses → trả về courseId, title, studentCount, status

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `courseId` |
| `teacher_id` | UUID | FK → teachers.id, NOT NULL | Business Rule: "Chỉ trả về khóa học thuộc quyền sở hữu của giáo viên" |
| `udemy_course_id` | VARCHAR(100) | UNIQUE, NULLABLE | ID gốc từ Udemy, dùng để đồng bộ |
| `title` | VARCHAR(500) | NOT NULL | API output: `title` |
| `student_count` | INTEGER | NOT NULL, DEFAULT 0 | API output: `studentCount` |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'imported' | Trạng thái: imported → analyzing → analyzed → improving |
| `data_import_id` | UUID | FK → data_imports.id, NULLABLE | Liên kết với file import nào |
| `udemy_connection_id` | UUID | FK → udemy_connections.id, NULLABLE | Liên kết với connection nào |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |
| `deleted_at` | TIMESTAMP | NULLABLE | Soft delete |

---

### 1.5 Module (Học phần)

> Nguồn: API Drop-off Analysis trả về modules array chứa moduleId, moduleTitle

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `moduleId` |
| `course_id` | UUID | FK → courses.id, NOT NULL | Module thuộc về 1 Course |
| `title` | VARCHAR(500) | NOT NULL | API output: `moduleTitle` |
| `order_index` | INTEGER | NOT NULL | Thứ tự hiển thị trong biểu đồ phễu |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |

---

### 1.6 Lesson (Bài giảng)

> Nguồn: businessdomain.md mục 2 — "Lesson / Module: Bài học nơi có thể xảy ra drop-off"
> API: GET /drop-off-analysis → trả về lessonId, lessonTitle, type, dropOffRate, hasWarning

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `lessonId` |
| `course_id` | UUID | FK → courses.id, NOT NULL | Lesson thuộc về 1 Course |
| `module_id` | UUID | FK → modules.id, NULLABLE | Lesson nằm trong module nào |
| `title` | VARCHAR(500) | NOT NULL | API output: `lessonTitle` |
| `type` | VARCHAR(20) | NOT NULL | API output: `type` — video, article, quiz, assignment |
| `order_index` | INTEGER | NOT NULL | Thứ tự bài học, phục vụ biểu đồ phễu (US-004) |
| `duration_seconds` | INTEGER | NULLABLE | Thời lượng video, phục vụ timeline analysis (US-004 AC-02) |
| `drop_off_rate` | FLOAT | NULLABLE | API output: `dropOffRate` |
| `has_warning` | BOOLEAN | DEFAULT false | API output: `hasWarning` — true nếu drop_off_rate > 0.20 |
| `student_count` | INTEGER | NOT NULL, DEFAULT 0 | Business Rule US-004: "tối thiểu 30 học viên mới phân tích" |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |

---

### 1.7 StudentEnrollment (Học viên đăng ký)

> Nguồn: businessdomain.md mục 2 — "Student: Học viên Udemy"
> API: GET /at-risk-students → trả về studentId, maskedName, daysInactive, canSendReminder

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `studentId` |
| `course_id` | UUID | FK → courses.id, NOT NULL | Học viên đăng ký trong khóa nào |
| `udemy_student_id` | VARCHAR(100) | NOT NULL | ID gốc từ Udemy |
| `masked_name` | VARCHAR(255) | NOT NULL | API output: `maskedName` — "Nguy*** A***" |
| `email_encrypted` | TEXT | NULLABLE | Business Rule US-002: "email phải được ẩn danh hóa hoặc mã hóa" |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'active' | Active → At-risk → Inactive → Re-engaged |
| `last_activity_at` | TIMESTAMP | NULLABLE | Dùng để tính `daysInactive` |
| `progress_percent` | FLOAT | DEFAULT 0.0 | Phần trăm hoàn thành khóa |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |

**Quy tắc tính status (từ Business Rule US-003):**
- `active`: last_activity_at trong 7 ngày gần nhất
- `at_risk`: last_activity_at từ 14-29 ngày trước
- `inactive`: last_activity_at > 30 ngày trước
- `reengaged`: Từng inactive/at-risk nhưng quay lại học

---

### 1.8 LearningActivity (Lịch sử hoạt động học tập)

> Nguồn: businessdomain.md mục 2 — "Learning Activity: Dữ liệu hành vi học tập"
> Đây là bảng dữ liệu lõi, parse từ file CSV/Udemy API (US-002)

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | |
| `student_enrollment_id` | UUID | FK → student_enrollments.id, NOT NULL | Hoạt động của ai |
| `lesson_id` | UUID | FK → lessons.id, NOT NULL | Hoạt động ở bài nào |
| `activity_type` | VARCHAR(20) | NOT NULL | video_watch, quiz_attempt, assignment_submit, article_read |
| `started_at` | TIMESTAMP | NOT NULL | Khi nào bắt đầu xem/làm |
| `ended_at` | TIMESTAMP | NULLABLE | Khi nào dừng — NULL = chưa hoàn thành = DROP-OFF |
| `duration_seconds` | INTEGER | NULLABLE | Xem được bao lâu — phục vụ timeline analysis (US-004 AC-02) |
| `video_stop_at_second` | INTEGER | NULLABLE | Dừng video ở giây thứ mấy — "mốc giây học viên bấm dừng nhiều nhất" |
| `is_completed` | BOOLEAN | DEFAULT false | Đã hoàn thành bài chưa — phục vụ tính Completion Rate (US-003) |
| `created_at` | TIMESTAMP | NOT NULL | Audit |

**Tại sao cần `video_stop_at_second`:**
> US-004 AC-02: "hệ thống hiển thị biểu đồ dòng thời gian thể hiện mốc giây/phút mà học viên bấm dừng video nhiều nhất"

**Tại sao cần `is_completed`:**
> US-003 Dashboard: completionRate = COUNT(is_completed=true) / COUNT(total enrollments)

---

### 1.9 AiInsight (Giả thuyết từ AI)

> Nguồn: businessdomain.md mục 2 — "AI Insight: Giả thuyết AI về nguyên nhân vấn đề"
> API: GET /api/v1/courses/{courseId}/lessons/{lessonId}/ai-insights

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `insightId` |
| `lesson_id` | UUID | FK → lessons.id, NOT NULL | Insight cho bài nào |
| `hypothesis` | TEXT | NOT NULL | API output: `hypothesis` — "video quá dài", "bài kiểm tra quá khó" |
| `confidence_score` | FLOAT | NOT NULL, CHECK(0..1) | API output: `confidenceScore` |
| `raw_prompt` | TEXT | NULLABLE | Prompt gửi cho LLM — lưu để debug/audit |
| `raw_response` | TEXT | NULLABLE | Response gốc từ LLM — lưu để debug/audit |
| `model_version` | VARCHAR(50) | NOT NULL | Phiên bản model AI đã dùng |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |

---

### 1.10 Recommendation (Đề xuất cải thiện)

> Nguồn: businessdomain.md mục 2 — "Recommendation: Đề xuất hành động cải thiện khóa học"
> API: POST /api/v1/.../recommendations/{recommendationId}/action

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | API output: `recommendationId` |
| `ai_insight_id` | UUID | FK → ai_insights.id, NOT NULL | Đề xuất sinh từ insight nào |
| `suggestion_text` | TEXT | NOT NULL | API output: `suggestionText` — "chia nhỏ video thành 3 phần" |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, applied, ignored |
| `actioned_at` | TIMESTAMP | NULLABLE | Khi nào giáo viên bấm Applied/Ignored |
| `created_at` | TIMESTAMP | NOT NULL | Audit |
| `updated_at` | TIMESTAMP | NOT NULL | Audit |

---

### 1.11 ReminderLog (Nhật ký gửi nhắc nhở)

> Nguồn: businessdomain.md mục 2 — "Reminder / Message: Tin nhắn/email nhắc học viên quay lại"
> API: POST /send-reminder, GET /at-risk-students

| Trường | Kiểu | Ràng buộc | Nguồn gốc |
|---|---|---|---|
| `id` | UUID v4 | PK | |
| `student_enrollment_id` | UUID | FK → student_enrollments.id, NOT NULL | Gửi cho ai |
| `lesson_id` | UUID | FK → lessons.id, NOT NULL | Về bài học nào |
| `teacher_id` | UUID | FK → teachers.id, NOT NULL | Ai gửi |
| `message_body` | TEXT | NOT NULL | API input: `messageBody` |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending, sent, delivered, failed |
| `sent_at` | TIMESTAMP | NULLABLE | Thời điểm gửi thực tế |
| `failure_reason` | TEXT | NULLABLE | API output: `failures[].reason` |
| `tracking_expires_at` | TIMESTAMP | NULLABLE | Business Rule: "theo dõi phản hồi trong 7 ngày" |
| `created_at` | TIMESTAMP | NOT NULL | Audit |

---

## 2. Relationships

```
Teacher (1) ──────── (N) Course
Teacher (1) ──────── (N) UdemyConnection
Teacher (1) ──────── (N) DataImport
Teacher (1) ──────── (N) ReminderLog

Course  (1) ──────── (N) Module
Course  (1) ──────── (N) StudentEnrollment

Module  (1) ──────── (N) Lesson

Lesson  (1) ──────── (N) LearningActivity
Lesson  (1) ──────── (N) AiInsight
Lesson  (1) ──────── (N) ReminderLog

StudentEnrollment (1) ── (N) LearningActivity
StudentEnrollment (1) ── (N) ReminderLog

AiInsight (1) ────── (N) Recommendation
```

---

## 3. Aggregates

| Aggregate Root | Entities thuộc Aggregate | Lý do |
|---|---|---|
| **Teacher** | Teacher, UdemyConnection, DataImport | Mọi thao tác import/connect đều gắn với 1 teacher |
| **Course** | Course, Module, Lesson, StudentEnrollment, LearningActivity | Tất cả dữ liệu phân tích xoay quanh 1 khóa học |
| **AiInsight** | AiInsight, Recommendation | Recommendation luôn sinh từ 1 Insight cụ thể |

---

## 4. Value Objects

| Value Object | Thuộc Entity | Ý nghĩa |
|---|---|---|
| `EmailAddress` | Teacher | Email hợp lệ, validate format trước khi lưu |
| `MaskedName` | StudentEnrollment | Tên ẩn danh hóa, không bao giờ hiển thị tên đầy đủ |
| `ConfidenceScore` | AiInsight | Float trong khoảng [0.0, 1.0], biểu thị độ tin cậy |
| `DateRange` | AnalyticsService (query) | Khoảng thời gian lọc dữ liệu dashboard |
| `FileExtension` | DataImport | Chỉ chấp nhận .csv hoặc .xlsx |

---

## 5. Domain Events

> Nguồn: businessdomain.md mục 9

| Event | Trigger khi nào | Kết quả |
|---|---|---|
| `TeacherLoggedIn` | Đăng nhập thành công | Tạo JWT token, reset failed_login_count |
| `UdemyDataConnected` | Kết nối API Udemy thành công | Set status = 'connected', bắt đầu đồng bộ |
| `DataImported` | Parse file CSV/XLSX xong | Tạo records Course, Lesson, StudentEnrollment |
| `DropOffDetected` | Tính toán xong, phát hiện lesson có drop_off > 20% | Set has_warning = true |
| `AIInsightGenerated` | LLM trả kết quả phân tích | Lưu hypothesis + recommendations vào DB |
| `RecommendationCreated` | AI sinh đề xuất hành động | Hiển thị trên giao diện cho giáo viên |
| `RecommendationActioned` | Giáo viên bấm Applied hoặc Ignored | Cập nhật status, feedback cho AI |
| `ReminderSent` | Email/message được gửi thành công | Set tracking_expires_at = sent_at + 7 days |
| `StudentReEngaged` | Học viên At-risk/Inactive quay lại học | Update status = 'reengaged' |

---

## 6. Invariants (Quy tắc bất biến)

| Entity | Quy tắc | Nguồn |
|---|---|---|
| Teacher | `failed_login_count` không được > 5 mà không set `locked_until` | Business Rule US-001 |
| Teacher | `password_hash` không bao giờ lưu plaintext | Business Rule US-001 |
| DataImport | File phải có extension `.csv` hoặc `.xlsx` | API Spec: "format: CSV/XLSX" |
| DataImport | Tổng quy mô ≤ 3 khóa học, ≤ 2.600 học viên (MVP) | Business Rule US-002 |
| Lesson | `has_warning = true` khi và chỉ khi `drop_off_rate > 0.20` | Business Rule US-004: "ngưỡng 20%" |
| Lesson | Không phân tích drop-off khi `student_count < 30` | Business Rule US-004 |
| AiInsight | Không sinh insight khi lesson có `student_count < 30` | Business Rule US-005 |
| AiInsight | Luôn kèm disclaimer "chỉ mang tính tham khảo" | Business Rule US-005 |
| Recommendation | `status` chỉ nhận: pending, applied, ignored | API Spec endpoint #8 |
| ReminderLog | KHÔNG gửi cùng 1 student nếu đã gửi trong 7 ngày | Business Rule US-006 |
| StudentEnrollment | `masked_name` không bao giờ hiển thị tên đầy đủ | Business Rule US-006 |

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*