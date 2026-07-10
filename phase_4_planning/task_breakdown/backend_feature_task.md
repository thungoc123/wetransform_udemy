# Backend Feature Tasks — AI Learning Analytics MVP

Dựa trên User Stories, API Specification và Architecture Overview để triển khai các nghiệp vụ backend cho từng feature.

| Task ID | Task Name | Mục tiêu | Phụ thuộc | Resource |
| --- | --- | --- | --- | --- |
| **BE-001** | Triển khai Auth API | Xây dựng endpoint login, xác thực tài khoản, xử lý lỗi đăng nhập và khóa tài khoản | Infrastructure Tasks | API Specification, User Stories, Architecture Overview |
| **BE-002** | Triển khai Data Source API | Cung cấp API lấy các phương thức nhập dữ liệu và thiết lập kết nối Udemy | Infrastructure Tasks | API Specification, User Stories |
| **BE-003** | Triển khai Upload & Import Workflow | Xử lý upload file CSV/XLSX, validate schema, lưu import job và chạy background parsing | Database Tasks | API Specification, Architecture Overview |
| **BE-004** | Triển khai Analytics Service | Tính toán dashboard overview, completion rate, drop-off rate, active/inactive/at-risk students | Database Tasks | API Specification, User Stories, Architecture Overview |
| **BE-005** | Triển khai Drop-off Analysis API | Xây dựng API trả về funnel chart và lesson-level hot spots | Analytics Service | API Specification, User Stories |
| **BE-006** | Triển khai AI Insights API | Tạo workflow gọi OpenAI, sinh giả thuyết và đề xuất cải thiện cho bài học | Analytics Service | API Specification, User Stories, Architecture Overview |
| **BE-007** | Triển khai Intervention API | Xây dựng API lấy danh sách at-risk students và gửi reminder với spam guard | Infrastructure Tasks | API Specification, User Stories |
| **BE-008** | Triển khai Agent/Workflow Layer | Tạo workflow điều phối dữ liệu analytics và AI recommendations cho luồng nâng cao | Backend Feature Tasks | Architecture Overview, User Stories |
