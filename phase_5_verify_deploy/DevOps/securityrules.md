Trả lời câu hỏi: Hệ thống cần tuân thủ những nguyên tắc bảo mật nào?

Authentication
Cơ chế xác thực?
Authorization
Phân quyền thế nào?
Data Protection
Dữ liệu nào cần mã hóa?
Secret Management
- Local/Dev: Lưu bằng file `.env` (không bao giờ commit file này lên git, chỉ commit `.env.example`).
- CI/CD & Production: Sử dụng Github Actions Secrets để tự động pass biến môi trường vào Docker Image khi deploy. Các secret bao gồm `DATABASE_URL`, `JWT_SECRET_KEY`, `OPENAI_API_KEY`, v.v.
API Security
Rate limiting?
CORS?
CSRF?
Audit
Những hành động nào cần log?
