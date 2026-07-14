# GitHub Issue List — AI Learning Analytics MVP

Tài liệu này là danh sách issue gợi ý để GitHub Copilot tạo issue cho dự án. Mỗi task trong task breakdown tương ứng với một issue.

## Hướng dẫn dùng

- Mỗi mục dưới đây tạo thành 1 issue GitHub.
- Tiêu đề issue nên theo format: [TASK_ID] Task Name
- Dùng metadata ở dưới để điền vào issue body, labels, assignee và project column.
- Nếu Copilot có GitHub MCP/CLI, có thể tạo trực tiếp từ danh sách này.

## Project

- Project name: AI Learning Analytics MVP
- Columns: Backlog, Ready, In Progress, Review, Done

---

## Foundation Tasks

### [FND-001] Initialize Backend Project
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, type:infra, size:3
- Depends on: None
- Suggested column: Done
- Summary: Khởi tạo project backend theo tech stack đã chọn, cấu hình base app và môi trường dev.

### [FND-002] Configure Project Structure
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, size:2
- Depends on: FND-001
- Suggested column: Done
- Summary: Tạo cấu trúc thư mục và module chuẩn theo project structure.

### [FND-003] Configure Environment Management
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, type:infra, size:2
- Depends on: FND-001
- Suggested column: Done
- Summary: Thiết lập env config, biến môi trường và config loader.

### [FND-004] Configure Dependency Injection
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, size:3
- Depends on: FND-002
- Suggested column: Done
- Summary: Cài đặt DI/IoC container và đăng ký service core.

### [FND-005] Configure Database Connection
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:database, type:backend, size:3
- Depends on: FND-003, FND-004
- Suggested column: Done
- Summary: Kết nối database và thiết lập ORM/connection pool.

### [FND-006] Configure Migration Framework
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:database, size:2
- Depends on: FND-005
- Suggested column: Done
- Summary: Thiết lập migration framework cho schema management.

### [FND-007] Configure Seeder Framework
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:database, size:2
- Depends on: FND-006
- Suggested column: Done
- Summary: Cấu hình seed data cho môi trường dev và demo.

### [FND-008] Configure Global Exception Handling
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Thiết lập global exception handling thống nhất.

### [FND-009] Configure Global Validation Framework
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Thêm validation pipeline cho DTO và request payload.

### [FND-010] Configure Unified API Response
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, type:api, size:2
- Depends on: FND-008
- Suggested column: Done
- Summary: Chuẩn hóa format response cho toàn hệ thống.

### [FND-011] Configure Logging Framework
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:observability, type:infra, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Tích hợp thư viện logging có cấu trúc.

### [FND-012] Configure Request/Response Logging
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:observability, size:2
- Depends on: FND-011
- Suggested column: Done
- Summary: Bổ sung correlation ID và access log middleware.

### [FND-013] Configure API Documentation
- Assignee: Phan Đức Duy
- Priority: Low
- Estimate: 1 SP
- Labels: priority:low, type:api, size:1
- Suggested column: Done
- Summary: Hoàn thiện cấu hình Swagger UI / ReDoc.

### [FND-014] Configure Health Check Endpoint
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 1 SP
- Labels: priority:medium, type:backend, size:1
- Depends on: FND-004
- Suggested column: Done
- Summary: Tạo endpoint /health, /ready, /live.

### [FND-015] Configure CORS Policy
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 1 SP
- Labels: priority:medium, type:security, size:1
- Depends on: FND-004
- Suggested column: Done
- Summary: Cấu hình CORS an toàn cho API.

### [FND-016] Configure Security Headers
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 1 SP
- Labels: priority:medium, type:security, size:1
- Depends on: FND-004
- Suggested column: Done
- Summary: Thêm các middleware bảo mật cơ bản (Helmet tương đương).

### [FND-017] Configure Authentication Framework
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:security, type:api, size:3
- Depends on: FND-006
- Suggested column: Done
- Summary: Thiết lập JWT auth cơ bản cho nội bộ.

### [FND-018] Configure Authorization Framework
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:security, type:api, size:2
- Depends on: FND-017
- Suggested column: Done
- Summary: Xây dựng RBAC decorator/middleware đơn giản.

### [FND-019] Configure Password Hashing
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 1 SP
- Labels: priority:high, type:security, size:1
- Suggested column: Done
- Summary: Cấu hình thư viện mã hóa mật khẩu.

### [FND-020] Configure Rate Limiting
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 1 SP
- Labels: priority:medium, type:backend, size:1
- Depends on: FND-004
- Suggested column: Done
- Summary: Thêm rate limiting cho API.

### [FND-021] Configure Cache Framework
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Cấu hình cache layer cho performance.

### [FND-022] Configure File Storage Abstraction
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Thiết lập abstraction cho file storage.

### [FND-023] Configure Email Infrastructure
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Kết nối dịch vụ email cho reminder.

### [FND-024] Configure Background Job Framework
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, type:infra, size:3
- Depends on: FND-004
- Suggested column: Done
- Summary: Thiết lập background jobs và queue system.

### [FND-025] Configure Event Bus
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-004
- Suggested column: Done
- Summary: Cài đặt event-driven cơ bản cho notification.

### [FND-026] Configure Monitoring
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:devops, size:2
- Depends on: FND-011
- Suggested column: Done
- Summary: Bật metrics và monitoring cho hệ thống.

### [FND-027] Configure Distributed Tracing
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:devops, size:2
- Depends on: FND-011
- Suggested column: Done
- Summary: Cấu hình tracing cho request flow.

### [FND-028] Configure Audit Logging
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-011
- Suggested column: Done
- Summary: Thiết lập audit trail cho action logging.

### [FND-029] Configure Error Code Registry
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 1 SP
- Labels: priority:medium, type:backend, size:1
- Depends on: FND-008
- Suggested column: Done
- Summary: Chuẩn hóa error code cho API.

### [FND-030] Configure Localization Framework
- Assignee: Phan Đức Duy
- Priority: Low
- Estimate: 1 SP
- Labels: priority:low, type:backend, size:1
- Depends on: FND-004
- Suggested column: Done
- Summary: Thiết lập framework đa ngôn ngữ nếu cần.

### [FND-031] Configure Unit Test Framework
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:testing, size:2
- Depends on: FND-001
- Suggested column: Done
- Summary: Cài đặt unit test framework cho backend.

### [FND-032] Configure Integration Test Framework
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:testing, size:2
- Depends on: FND-005
- Suggested column: Done
- Summary: Cài đặt integration test framework và test containers.

### [FND-033] Configure Code Quality Tools
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, type:devops, size:2
- Depends on: FND-001
- Suggested column: Done
- Summary: Thiết lập linting, formatting và static analysis.

### [FND-034] Configure Git Hooks
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 1 SP
- Labels: priority:medium, type:devops, size:1
- Depends on: FND-033
- Suggested column: Done
- Summary: Cài đặt pre-commit hooks và auto lint.

### [FND-035] Configure Docker Environment
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:devops, size:2
- Depends on: FND-001
- Suggested column: Done
- Summary: Tạo Dockerfile và docker-compose cho app.

### [FND-036] Configure CI Pipeline
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:devops, size:3
- Depends on: FND-031, FND-033
- Suggested column: Done
- Summary: Thiết lập pipeline build/test/lint tự động.

### [FND-037] Configure CD Pipeline
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:devops, size:2
- Depends on: FND-036
- Suggested column: Done
- Summary: Chuẩn bị deployment pipeline cho staging/production.

### [FND-038] Configure Secrets Management
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:devops, size:2
- Depends on: FND-003
- Suggested column: Done
- Summary: Quản lý secret và environment credentials.

### [FND-039] Configure Backup Strategy
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:devops, size:2
- Depends on: FND-005
- Suggested column: Done
- Summary: Thiết lập strategy backup và restore database.

### [FND-040] Configure Project Documentation
- Assignee: Huỳnh Hữu Tài
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:documentation, size:2
- Depends on: FND-001
- Suggested column: Backlog
- Summary: Viết README, contribution guide và onboarding doc.

---

## Infrastructure Tasks

### [INF-001] Xây dựng Authentication Module
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, type:infra, size:3
- Depends on: FND-017, FND-019
- Suggested column: Backlog
- Summary: Triển khai module xác thực và session/JWT.

### [INF-002] Xây dựng Authorization Module
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, size:2
- Depends on: FND-018, INF-001
- Suggested column: Backlog
- Summary: Thiết lập phân quyền cho giáo viên và course/lesson access.

### [INF-003] Xây dựng Email Service
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-023
- Suggested column: Backlog
- Summary: Xây dựng service gửi reminder email.

### [INF-004] Xây dựng File Storage Abstraction
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-022
- Suggested column: Backlog
- Summary: Hỗ trợ lưu trữ file upload CSV/XLSX.

### [INF-005] Xây dựng Cache Service
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-021
- Suggested column: Backlog
- Summary: Cache kết quả dashboard và analytics.

### [INF-006] Xây dựng Queue & Background Job Infrastructure
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, type:infra, size:3
- Depends on: FND-024
- Suggested column: Backlog
- Summary: Cài đặt queue, retry policy và monitoring task.

### [INF-007] Xây dựng Notification Service
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: INF-003, FND-025
- Suggested column: Backlog
- Summary: Cung cấp thông báo đa kênh cho giáo viên và học viên.

### [INF-008] Xây dựng Audit Logging & Config Management
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:backend, type:infra, size:2
- Depends on: FND-028, FND-038
- Suggested column: Backlog
- Summary: Ghi log hành động hệ thống và cấu hình môi trường.

---

## Database Tasks

### [DB-001] Thiết kế schema cho các bảng cốt lõi
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:database, size:3
- Depends on: FND-006
- Suggested column: Backlog
- Summary: Xác định schema cho teachers, courses, lessons, enrollments, activities.

### [DB-002] Thiết kế schema cho dữ liệu import và kết nối nguồn
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:database, size:2
- Depends on: DB-001
- Suggested column: Backlog
- Summary: Tạo bảng import và kết nối Udemy.

### [DB-003] Thiết kế schema cho analytics và AI insights
- Assignee: Dương Trung Hiếu
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:database, type:ai, size:3
- Depends on: DB-001
- Suggested column: Backlog
- Summary: Tạo schema cho ai_insights, recommendations, reminder_logs.

### [DB-004] Implement foreign keys và constraints
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:database, size:2
- Depends on: DB-001, DB-002, DB-003
- Suggested column: Done
- Summary: Đảm bảo toàn vẹn dữ liệu và khóa ngoại.

### [DB-005] Tạo indexes cho truy vấn thường dùng
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:database, size:2
- Depends on: DB-004
- Suggested column: Done
- Summary: Tối ưu bảng cho dashboard và analytics query.

### [DB-006] Implement soft delete và audit columns
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:database, size:2
- Depends on: DB-004
- Suggested column: Done
- Summary: Bổ sung soft delete và audit timestamp.

### [DB-007] Tạo migration scripts cho tất cả bảng
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:database, size:3
- Depends on: DB-005, DB-006
- Suggested column: Done
- Summary: Tạo migration scripts chạy trên dev/staging.

### [DB-008] Tạo seed data cho môi trường phát triển
- Assignee: Dương Trung Hiếu
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:database, type:ai, size:2
- Depends on: DB-007
- Suggested column: Backlog
- Summary: Chuẩn bị dữ liệu mẫu cho demo và test.

---

## Backend Feature Tasks

### [BE-001] Triển khai Auth API
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, size:3
- Depends on: INF-001, DB-001
- Suggested column: Backlog
- Summary: Xây dựng API login, xác thực và khóa tài khoản.

### [BE-002] Triển khai Data Source API
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:backend, size:2
- Depends on: INF-004, DB-002
- Suggested column: Backlog
- Summary: Cung cấp API nhập dữ liệu và kết nối Udemy.

### [BE-003] Triển khai Upload & Import Workflow
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, size:3
- Depends on: DB-002, INF-004, INF-006
- Suggested column: Backlog
- Summary: Xử lý upload file, validate schema và background parsing.

### [BE-004] Triển khai Analytics Service
- Assignee: Dương Trung Hiếu
- Priority: High
- Estimate: 5 SP
- Labels: priority:high, type:backend, type:ai, size:5
- Depends on: DB-001, DB-003, INF-005
- Suggested column: Backlog
- Summary: Tính toán metrics dashboard và analytics cơ bản.

### [BE-005] Triển khai Drop-off Analysis API
- Assignee: Dương Trung Hiếu
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, type:ai, size:3
- Depends on: BE-004
- Suggested column: Backlog
- Summary: Trả về funnel chart và lesson-level hot spots.

### [BE-006] Triển khai AI Insights API
- Assignee: Dương Trung Hiếu
- Priority: High
- Estimate: 5 SP
- Labels: priority:high, type:backend, type:ai, size:5
- Depends on: BE-004, DB-003
- Suggested column: Backlog
- Summary: Tạo workflow gọi OpenAI và sinh đề xuất cải thiện.

### [BE-007] Triển khai Intervention API
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:backend, size:3
- Depends on: BE-004, INF-003, INF-007
- Suggested column: Backlog
- Summary: Xây dựng API list at-risk student và reminder workflow.

### [BE-008] Triển khai Agent/Workflow Layer
- Assignee: Dương Trung Hiếu
- Priority: High
- Estimate: 5 SP
- Labels: priority:high, type:backend, type:ai, size:5
- Depends on: BE-005, BE-006, BE-007
- Suggested column: Backlog
- Summary: Tạo workflow điều phối analytics và recommendations.

---

## Frontend Feature Tasks

### [FE-001] Xây dựng UI Authentication
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FE-007, BE-001
- Suggested column: Backlog
- Summary: Màn hình đăng nhập và state auth cho app.

### [FE-002] Xây dựng UI Data Integration
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FE-007, BE-002, BE-003
- Suggested column: Backlog
- Summary: Màn hình kết nối Udemy và upload file.

### [FE-003] Xây dựng UI Course Dashboard
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FE-007, BE-004
- Suggested column: Backlog
- Summary: Hiển thị KPI, course selector và overview metrics.

### [FE-004] Xây dựng UI Drop-off Analysis
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FE-007, BE-005
- Suggested column: Backlog
- Summary: Màn hình funnel chart và hot spots analysis.

### [FE-005] Xây dựng UI AI Insights
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FE-007, BE-006
- Suggested column: Backlog
- Summary: Màn hình hiển thị hypothesis và đề xuất cải thiện.

### [FE-006] Xây dựng UI Student Intervention
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FE-007, BE-007
- Suggested column: Backlog
- Summary: Màn hình list at-risk student, preview mẫu nhắc nhở và xác nhận gửi thủ công.

### [FE-007] Xây dựng Shared UI Components & State Layer
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:frontend, size:3
- Depends on: FND-002
- Suggested column: Backlog
- Summary: Tạo shared layout, components, chart components và API state layer.

---

## Cross-Feature Integration Tasks

### [INT-001] Tích hợp Authentication với toàn bộ feature
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:integration, size:3
- Depends on: BE-001, FE-001, FE-002, FE-003, FE-004, FE-005, FE-006
- Suggested column: Backlog
- Summary: Đảm bảo toàn bộ screen và API yêu cầu auth đúng chuẩn.

### [INT-002] Tích hợp Analytics → AI Insights
- Assignee: Dương Trung Hiếu
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:integration, type:ai, size:3
- Depends on: BE-005, BE-006
- Suggested column: Backlog
- Summary: Kết nối drop-off data với AI workflow.

### [INT-003] Tích hợp Intervention → Reminder Workflow
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:integration, size:3
- Depends on: BE-007, FE-006
- Suggested column: Backlog
- Summary: Link at-risk list với luồng preview, xác nhận gửi thủ công và reminder tracking workflow.

### [INT-004] Tích hợp Import Pipeline → Dashboard
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:integration, size:3
- Depends on: BE-003, BE-004
- Suggested column: Backlog
- Summary: Sau import thành công, dữ liệu tự động sẵn sàng cho dashboard.

### [INT-005] Tích hợp Cache, Queue và Notification
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:integration, size:2
- Depends on: INF-005, INF-006, INF-007
- Suggested column: Backlog
- Summary: Đảm bảo cache, queue và notification hoạt động thống nhất.

### [INT-006] Tích hợp Error Handling & UX Feedback
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:integration, size:2
- Depends on: FE-007, BE-008
- Suggested column: Backlog
- Summary: Đồng bộ empty state, loading state và error feedback giữa FE/BE.

---

## Testing Tasks

### [TST-001] Viết unit test cho backend services
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:testing, size:3
- Depends on: BE-008, FND-031
- Suggested column: Backlog
- Summary: Kiểm thử auth, analytics, import, reminder ở mức unit.

### [TST-002] Viết integration test cho repository và DB
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:testing, size:3
- Depends on: DB-008, FND-032
- Suggested column: Backlog
- Summary: Xác minh migration, query và transaction hoạt động đúng.

### [TST-003] Viết API contract test
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:testing, size:2
- Depends on: BE-008
- Suggested column: Backlog
- Summary: Kiểm tra schema response và status code cho API chính.

### [TST-004] Viết frontend component/unit test
- Assignee: Nguyễn Thị Ngọc Thư
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:testing, size:3
- Depends on: FE-001, FE-002, FE-003, FE-004, FE-005, FE-006, FE-007
- Suggested column: Backlog
- Summary: Kiểm thử form, chart, modal và state handling.

### [TST-005] Thiết kế end-to-end test cho critical user flows
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 5 SP
- Labels: priority:high, type:testing, size:5
- Depends on: INT-001, INT-002, INT-003, INT-004
- Suggested column: Backlog
- Summary: Cover login, import data, dashboard, AI insights và reminder.

### [TST-006] Thực hiện performance và security testing
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:testing, size:3
- Depends on: DEP-006
- Suggested column: Backlog
- Summary: Kiểm tra tải, bảo mật và rate limiting sau deploy staging.

---

## Release & Deployment Tasks

### [DEP-001] Containerize ứng dụng
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:devops, size:3
- Depends on: FND-035
- Suggested column: Backlog
- Summary: Tạo Dockerfile và docker-compose cho backend/frontend/database.

### [DEP-002] Cấu hình môi trường và secrets
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 2 SP
- Labels: priority:high, type:devops, size:2
- Depends on: FND-038
- Suggested column: Backlog
- Summary: Quản lý secret key, connection string và credentials.

### [DEP-003] Thiết lập CI/CD pipeline
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:devops, size:3
- Depends on: FND-037, TST-001
- Suggested column: Backlog
- Summary: Tạo pipeline build/test/deploy tự động.

### [DEP-004] Thiết lập monitoring và logging
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:devops, size:2
- Depends on: INF-008, FND-026
- Suggested column: Backlog
- Summary: Bật structured logs, metrics và alert cho API/background jobs.

### [DEP-005] Thiết lập backup và rollback
- Assignee: Phan Đức Duy
- Priority: Medium
- Estimate: 2 SP
- Labels: priority:medium, type:devops, size:2
- Depends on: DB-007, FND-039
- Suggested column: Backlog
- Summary: Chuẩn bị kịch bản backup, restore và rollback deployment.

### [DEP-006] Deploy staging và smoke test
- Assignee: Phan Đức Duy
- Priority: High
- Estimate: 3 SP
- Labels: priority:high, type:devops, size:3
- Depends on: TST-005
- Suggested column: Backlog
- Summary: Triển khai bản staging và chạy smoke test critical flows.
