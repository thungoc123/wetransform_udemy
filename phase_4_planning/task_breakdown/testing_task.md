# Testing Tasks — AI Learning Analytics MVP

Dựa trên User Stories, API Specification và Screen Specification để xây dựng chiến lược kiểm thử toàn diện cho product.

| Task ID | Task Name | Mục tiêu | Phụ thuộc | Resource |
| --- | --- | --- | --- | --- |
| **TST-001** | Viết unit test cho backend services | Kiểm thử auth, analytics, import, reminder logic ở mức unit | Backend Feature Tasks | User Stories, API Specification, Architecture Overview |
| **TST-002** | Viết integration test cho repository và DB | Xác nhận truy vấn, migration và transaction hoạt động đúng | Database Tasks | Database Standards, Domain Model |
| **TST-003** | Viết API contract test | Kiểm tra response schema, status code và business rules cho các API chính | Backend Feature Tasks | API Specification, User Stories |
| **TST-004** | Viết frontend component/unit test | Kiểm thử form, chart, modal, table và state handling | Frontend Feature Tasks | Screen Specifications, Design System |
| **TST-005** | Thiết kế end-to-end test cho critical user flows | Cover login, import data, dashboard, AI insights và reminder | Cross-Feature Integration Tasks | User Flows, Screen Flows, User Stories |
| **TST-006** | Thực hiện performance và security testing | Kiểm tra tải, bảo mật, rate limiting và xử lý lỗi | Release & Deployment Tasks | Architecture Overview, API Specification, Security Rules |
