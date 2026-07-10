# Infrastructure Tasks — AI Learning Analytics MVP

Dựa trên Architecture Overview, Tech Stack, Project Structure và API Standards để xây dựng các module hạ tầng dùng chung cho toàn bộ hệ thống.

| Task ID | Task Name | Mục tiêu | Phụ thuộc | Resource |
| --- | --- | --- | --- | --- |
| **INF-001** | Xây dựng Authentication Module | Triển khai xác thực người dùng, JWT, quản lý session và khóa tài khoản sau nhiều lần đăng nhập sai | Foundation Tasks | Architecture Overview, API Specification, Tech Stack |
| **INF-002** | Xây dựng Authorization Module | Thiết lập phân quyền cho giáo viên và kiểm soát truy cập theo course / lesson | Foundation Tasks | Architecture Overview, API Specification |
| **INF-003** | Xây dựng Email Service | Cung cấp service gửi email nhắc nhở, template và trạng thái delivery | Foundation Tasks | Architecture Overview, Tech Stack, User Stories |
| **INF-004** | Xây dựng File Storage Abstraction | Hỗ trợ lưu trữ file upload CSV/XLSX từ Udemy và quản lý lifecycle file | Foundation Tasks | Architecture Overview, API Specification |
| **INF-005** | Xây dựng Cache Service | Cache kết quả dashboard, analytics và insights để giảm query chi phí | Foundation Tasks | Architecture Overview, Tech Stack |
| **INF-006** | Xây dựng Queue & Background Job Infrastructure | Cài đặt Celery/Redis, retry policy, task monitoring cho import và reminder | Foundation Tasks | Architecture Overview, Tech Stack |
| **INF-007** | Xây dựng Notification Service | Hỗ trợ gửi thông báo tới giáo viên và học viên qua nhiều kênh | Foundation Tasks | Architecture Overview, User Stories |
| **INF-008** | Xây dựng Audit Logging & Config Management | Ghi log hành động hệ thống, cấu hình môi trường và correlation ID cho tracing | Foundation Tasks | Architecture Overview, Coding Standards |
