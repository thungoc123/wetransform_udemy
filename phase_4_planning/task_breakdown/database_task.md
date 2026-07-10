# Database Tasks — AI Learning Analytics MVP

Dựa trên Domain Model, Database Standards và API Specification để thiết kế và triển khai dữ liệu cho MVP.

| Task ID | Task Name | Mục tiêu | Phụ thuộc | Resource |
| --- | --- | --- | --- | --- |
| **DB-001** | Thiết kế schema cho các bảng cốt lõi | Xác định bảng teachers, courses, modules, lessons, student_enrollments, learning_activities | Domain Model | Domain Model, Database Standards |
| **DB-002** | Thiết kế schema cho dữ liệu import và kết nối nguồn | Tạo bảng data_imports, udemy_connections để lưu trạng thái nhập dữ liệu | Domain Model | Domain Model, API Specification |
| **DB-003** | Thiết kế schema cho analytics và AI insights | Tạo bảng ai_insights, recommendations, reminder_logs cho phân tích và nhắc nhở | Domain Model | Domain Model, User Stories |
| **DB-004** | Implement foreign keys và constraints | Đảm bảo toàn vẹn dữ liệu, cascade rule và khóa ngoại rõ ràng | DB Standards | Database Standards |
| **DB-005** | Tạo indexes cho truy vấn thường dùng | Tối ưu dashboard, drop-off analysis, reminder cooldown, timeline analysis | DB Standards | Database Standards, API Specification |
| **DB-006** | Implement soft delete và audit columns | Bổ sung created_at, updated_at, deleted_at cho các bảng có thể xóa mềm | DB Standards | Database Standards |
| **DB-007** | Tạo migration scripts cho tất cả bảng | Sinh Alembic migration và đảm bảo chạy được trên môi trường dev/staging | Foundation Tasks | Database Standards, Tech Stack |
| **DB-008** | Tạo seed data cho môi trường phát triển | Chuẩn bị dữ liệu mẫu cho 3 khóa học, học viên và bài học demo | Domain Model | Domain Model, User Stories |
