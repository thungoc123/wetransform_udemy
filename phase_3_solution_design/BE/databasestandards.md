# Database Standards — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: Database phải được thiết kế như thế nào?
> Nguồn gốc: [domainmodel.md](./domainmodel.md), [APISpec.md](../../../phase_2_story_definition/APISpec.md), [businessdomain.md](../../../phase_1_discovery/BC/businessdomain.md)

---

## 1. Database Convention

### Table Naming
- **Quy tắc:** `snake_case`, danh từ số nhiều
- **Ví dụ:** `teachers`, `courses`, `lessons`, `student_enrollments`, `learning_activities`, `ai_insights`, `recommendations`, `reminder_logs`, `udemy_connections`, `data_imports`, `modules`

### Column Naming
- **Quy tắc:** `snake_case`
- **Ví dụ:** `teacher_id`, `drop_off_rate`, `student_count`, `last_activity_at`, `video_stop_at_second`
- **Boolean columns:** prefix `is_` hoặc `has_` — `is_completed`, `has_warning`
- **Timestamp columns:** suffix `_at` — `created_at`, `sent_at`, `connected_at`
- **Foreign Key columns:** `{referenced_table_singular}_id` — `teacher_id`, `course_id`, `lesson_id`

---

## 2. Primary Key

### UUID v4 (Bắt buộc)
- **Quy tắc:** Mọi bảng dùng UUID v4 làm Primary Key
- **Lý do:**
  - Tránh lộ tổng số records qua ID tự tăng (bảo mật)
  - Hỗ trợ merge dữ liệu từ nhiều nguồn (Udemy API + File upload) không lo trùng ID
  - PostgreSQL hỗ trợ native: `gen_random_uuid()`
- **Cú pháp:**
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```
- **KHÔNG dùng:** Auto Increment (không phù hợp cho hệ thống có dữ liệu từ bên ngoài)

---

## 3. Relationships

### Foreign Key
- **Quy tắc:** Mọi quan hệ phải có FK constraint tường minh
- **Đặt tên:** `fk_{bảng_con}_{cột}` — ví dụ: `fk_courses_teacher_id`
- **Danh sách FK:**

| Bảng con | Cột FK | Bảng cha | Nguồn gốc |
|---|---|---|---|
| `courses` | `teacher_id` | `teachers` | Teacher owns Course |
| `courses` | `data_import_id` | `data_imports` | Course được tạo từ import nào |
| `courses` | `udemy_connection_id` | `udemy_connections` | Course được tạo từ connection nào |
| `modules` | `course_id` | `courses` | Module thuộc Course |
| `lessons` | `course_id` | `courses` | Lesson thuộc Course |
| `lessons` | `module_id` | `modules` | Lesson thuộc Module |
| `student_enrollments` | `course_id` | `courses` | Student đăng ký Course |
| `learning_activities` | `student_enrollment_id` | `student_enrollments` | Activity của Student |
| `learning_activities` | `lesson_id` | `lessons` | Activity tại Lesson |
| `ai_insights` | `lesson_id` | `lessons` | Insight cho Lesson |
| `recommendations` | `ai_insight_id` | `ai_insights` | Recommendation từ Insight |
| `reminder_logs` | `student_enrollment_id` | `student_enrollments` | Reminder gửi cho Student |
| `reminder_logs` | `lesson_id` | `lessons` | Reminder về Lesson |
| `reminder_logs` | `teacher_id` | `teachers` | Teacher gửi Reminder |
| `udemy_connections` | `teacher_id` | `teachers` | Teacher tạo Connection |
| `data_imports` | `teacher_id` | `teachers` | Teacher upload file |

### Cascade
- **`ON DELETE CASCADE`:** Áp dụng cho child tables có dependency chặt:
  - Xóa Course → xóa Module, Lesson, StudentEnrollment
  - Xóa Lesson → xóa LearningActivity, AiInsight
  - Xóa AiInsight → xóa Recommendation
- **`ON DELETE RESTRICT`:** Áp dụng cho bảng Teacher (không được xóa teacher nếu còn course)

---

## 4. Audit

### Audit Columns (Bắt buộc cho mọi bảng)

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `created_at` | TIMESTAMP NOT NULL DEFAULT NOW() | Thời điểm tạo record |
| `updated_at` | TIMESTAMP NOT NULL DEFAULT NOW() | Thời điểm cập nhật lần cuối — tự động update bằng trigger |
| `deleted_at` | TIMESTAMP NULLABLE | Soft delete — NULL = chưa xóa |

### Soft Delete
- **Quy tắc:** KHÔNG bao giờ xóa dữ liệu vật lý (DELETE). Chỉ set `deleted_at = NOW()`
- **Query mặc định:** Mọi SELECT phải thêm `WHERE deleted_at IS NULL`
- **Lý do:** Giữ lại dữ liệu để audit, phân tích AI (dữ liệu quá khứ có giá trị)
- **Bảng KHÔNG cần `deleted_at`:** `learning_activities` (dữ liệu log, không xóa), `reminder_logs` (dữ liệu audit)

### Trigger tự động update `updated_at`:
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Áp dụng cho mỗi bảng
CREATE TRIGGER update_teachers_updated_at
    BEFORE UPDATE ON teachers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## 5. Migration

### Tool: Alembic
- **Lý do:** Chuẩn migration cho SQLAlchemy, hỗ trợ auto-generate từ model changes
- **Cú pháp tạo migration:**
```bash
# Tạo migration tự động từ thay đổi model
alembic revision --autogenerate -m "add_courses_table"

# Chạy migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Quy trình Migration
1. Developer thay đổi SQLAlchemy model trong `models.py`
2. Chạy `alembic revision --autogenerate` để sinh file migration
3. Review file migration — kiểm tra SQL đúng ý định
4. Commit file migration cùng với code changes
5. CI/CD chạy `alembic upgrade head` khi deploy

### Quy tắc:
- **KHÔNG** alter table thủ công bằng SQL trực tiếp
- Mỗi migration phải có cả `upgrade()` và `downgrade()`
- File migration đặt tên: `{revision_id}_{mô_tả_ngắn}.py`

---

## 6. Performance

### Index Strategy
> Mỗi index được thiết kế dựa trên query thực tế từ 10 API Endpoints

| Index | Bảng | Cột | API nào cần |
|---|---|---|---|
| `idx_courses_teacher_id` | courses | teacher_id | GET /courses — lọc theo giáo viên |
| `idx_modules_course_id` | modules | course_id | GET /drop-off-analysis — lấy modules theo course |
| `idx_lessons_course_id` | lessons | course_id | GET /drop-off-analysis — lấy lessons theo course |
| `idx_lessons_order` | lessons | (course_id, order_index) | Sắp xếp biểu đồ phễu |
| `idx_enrollments_course_id` | student_enrollments | course_id | GET /dashboard — đếm students |
| `idx_enrollments_status` | student_enrollments | (course_id, status) | GET /at-risk-students — filter by status |
| `idx_activities_student` | learning_activities | student_enrollment_id | Tính completion per student |
| `idx_activities_lesson` | learning_activities | lesson_id | Tính drop-off rate per lesson |
| `idx_activities_video_stop` | learning_activities | (lesson_id, video_stop_at_second) | Timeline analysis (US-004 AC-02) |
| `idx_insights_lesson` | ai_insights | lesson_id | GET /ai-insights per lesson |
| `idx_recommendations_insight` | recommendations | ai_insight_id | GET recommendations per insight |
| `idx_reminders_student_sent` | reminder_logs | (student_enrollment_id, sent_at) | Check 7-day cooldown (US-006) |
| `idx_reminders_tracking` | reminder_logs | tracking_expires_at | Cron job theo dõi re-engagement |

### Partition
- **Chưa áp dụng trong MVP** — dữ liệu chỉ 3 khóa học, ~2.600 học viên
- **Chuẩn bị cho tương lai:** Bảng `learning_activities` sẽ là ứng cử viên partition theo `created_at` (range partition theo tháng) khi dữ liệu vượt 1 triệu rows

### Query Optimization
- **Tránh N+1:** Dùng `joinedload()` hoặc `selectinload()` trong SQLAlchemy khi load relationships
- **Eager loading có kiểm soát:** Chỉ load relationship khi API cần — không load tất cả
- **Tối ưu aggregation:** Dashboard queries dùng `GROUP BY` + `COUNT()` thay vì load toàn bộ records vào Python
- **Caching:** Cache kết quả Dashboard và Drop-off analysis trong Redis (TTL 5 phút) — tránh query nặng lặp lại

---

## 7. Entity-Relationship Diagram

```
teachers ──┬── courses ──┬── modules ── lessons ──┬── learning_activities
            │              │                        ├── ai_insights ── recommendations
            │              └── student_enrollments ──┬── learning_activities
            │                                        └── reminder_logs
            ├── udemy_connections
            ├── data_imports
            └── reminder_logs
```

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*