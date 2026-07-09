# 📋 PROJECT SPEC — Agentic SDLC

> Tài liệu tổng hợp nhanh toàn bộ thông tin cốt lõi của dự án.
> Mọi quyết định đã ghi ở đây là CHỐT — không bàn lại trong vòng 24h trừ blocker chết người.

---

## 1. 🎯 Mục tiêu & Success Criteria
> *Nguồn: BC/project_context.md, BC/product_scope.md*

**Dự án giải quyết vấn đề gì?**
- [ ] Mô tả bài toán / pain point

**Ai là người dùng?**
- [ ] Danh sách nhóm người dùng (Actor)

**MVP gồm những tính năng nào?**
- [ ] Feature 1
- [ ] Feature 2

**Tính năng KHÔNG thuộc phạm vi (Out of Scope)?**
- [ ] ...

**Điều kiện để demo/release được xem là THÀNH CÔNG:**
- [ ] Tiêu chí 1 (measurable)
- [ ] Tiêu chí 2 (measurable)

**Giả định & ràng buộc ảnh hưởng đến phạm vi:**
- [ ] ...

---

## 2. ⚙️ Tech Stack CỐ ĐỊNH
> *Nguồn: TechLead/techstack.md*

| Layer | Công nghệ | Ghi chú |
|---|---|---|
| **Frontend** | Next.js 14 + shadcn/ui + Tailwind CSS + Recharts | TanStack Query cho state |
| **Backend** | Python 3.11 + FastAPI + Uvicorn | Async ASGI, auto Swagger docs |
| **AI/Agent** | LangGraph + LangChain + OpenAI GPT-4o | Agent orchestration, Tool use, Memory |
| **Database** | PostgreSQL 16 / Redis 7 | Redis: cache + Celery broker |
| **Infrastructure** | Docker + Docker Compose | MVP local. Production: TBD |
| **CI/CD** | GitHub Actions | Lint + Test + Build |
| **Monitoring** | structlog (JSON) | Structured log + correlation_id |
| **Auth** | PyJWT + bcrypt | JWT Bearer Token |
| **Payment** | Không có | Giáo viên bán trên Udemy |
| **Notification** | SendGrid / SMTP | Email reminder cho học viên (US-006) |
| **Storage** | Local filesystem (MVP) | File CSV/XLSX upload |
| **ORM** | SQLAlchemy 2.0 + Alembic | Migration + async query |
| **Background** | Celery + Redis | Parse file, agent exec, gửi email |

> ⚠️ Stack trên KHÔNG được thay đổi trong 24h. Mọi đề xuất đổi stack → ghi vào Decision Log.

---

## 3. 🏗️ Kiến trúc Tổng quan
> *Nguồn: TechLead/architectureoverview.md, TechLead/project_struture.md, DevOps/domainmodel.md*

### 3.1 System Architecture
- **Loại kiến trúc:** `[ ] Monolith  [ ] Modular Monolith  [ ] Microservices`
- **Lý do chọn kiến trúc này:** ...
- **Các thành phần chính:**
  - Service/Module A → chịu trách nhiệm gì?
  - Service/Module B → chịu trách nhiệm gì?
- **Giao tiếp giữa các service:** `[ ] REST  [ ] gRPC  [ ] Message Queue  [ ] Event`

### 3.2 Data Flow
- Request đi qua: `Client → Gateway → Service → Repository → DB`
- Có Event / Message Queue không? `[ ] Có  [ ] Không`

### 3.3 Folder / Layer Structure
```
src/
├── controller/     # Nhận request, trả response
├── service/        # Business logic
├── repository/     # Truy cập DB
├── domain/         # Entity, Value Object, Domain Event
└── infrastructure/ # Config, External, DB connection
```

### 3.4 Domain Model
- **Business Entities:** ...
- **Aggregate Root:** ...
- **Value Objects:** ...
- **Domain Events:** ...
- **Invariants (quy tắc bất biến):** ...

### 3.5 API Contract
> *Nguồn: TechLead/apistandards.md*

- **Style:** `[ ] REST  [ ] GraphQL  [ ] gRPC`
- **URL format:** `/api/v{n}/{resource}/{id}`
- **Versioning:** Header / URL prefix
- **Response format:**
```json
{
  "success": true,
  "data": {},
  "message": "",
  "errorCode": ""
}
```
- **Auth:** `[ ] JWT Bearer  [ ] OAuth2`
- **Docs:** `[ ] Swagger/OpenAPI`

### 3.6 External Integration
- Hệ thống tích hợp với: ...
- API bắt buộc phải có: ...

---

## 4. 🧹 Coding Convention
> *Nguồn: BE/codingstandards.md, BE/databasestandards.md*

### 4.1 Naming Convention
| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| Class | PascalCase | `UserService` |
| Method | camelCase | `getUserById()` |
| Variable | camelCase | `userId` |
| File | kebab-case | `user-service.ts` |
| Folder | kebab-case | `user-management/` |
| DB Table | snake_case | `user_profiles` |
| DB Column | snake_case | `created_at` |

### 4.2 Code Style
- Formatting: (Prettier / EditorConfig)
- Lint: (ESLint / Checkstyle / ...)
- Comment: bắt buộc với mọi public method
- Documentation: JSDoc / Swagger annotation

### 4.3 Design Principles
- `[ ] SOLID`  `[ ] Clean Architecture`  `[ ] DDD`  `[ ] Repository Pattern`  `[ ] CQRS`

### 4.4 Best Practices
- **Exception Handling:** Dùng global exception handler, không để lộ stack trace ra ngoài
- **Validation:** Validate ở controller layer, không validate lại ở service
- **Logging:** Structured log (JSON), có correlation-id mỗi request
- **Dependency Injection:** Bắt buộc — không new trực tiếp

### 4.5 ❌ Forbidden (KHÔNG được làm)
- Hardcode secret / credential trong source code
- Commit trực tiếp vào `main`/`master`
- Bỏ qua migration — không được alter table thủ công
- Các anti-pattern: God Object, Magic Number, copy-paste logic

### 4.6 Database Standards
- **Primary Key:** `[ ] UUID  [ ] Auto Increment`
- **Audit columns bắt buộc:** `created_at`, `updated_at`, `deleted_at` (soft delete)
- **Migration tool:** ...
- **Quy trình migration:** code-first / script-first
- **Index:** phải có index trên FK và cột search thường dùng
- **Tối ưu query:** tránh N+1, dùng eager loading có kiểm soát

---

## 5. ✅ Danh sách Task + Definition of Done
> *Nguồn: BC/product_scope.md*

### Definition of Done (DoD) Chung
- [ ] Code đã được review và approve (ít nhất 1 reviewer)
- [ ] Unit test pass (coverage ≥ X%)
- [ ] Không có lint error
- [ ] Swagger/API doc đã cập nhật
- [ ] Migration script đã commit
- [ ] Demo chạy được trên môi trường Dev/UAT

### Danh sách Tasks Hiện Tại

| ID | Task | Assignee | Status | DoD |
|---|---|---|---|---|
| TASK-001 | ... | ... | TODO | ... |

---

## 6. 🔒 Security & Performance
> *Nguồn: DevOps/securityrules.md, DevOps/performancetargets.md*

### 6.1 Security Rules
| Chủ đề | Quy tắc |
|---|---|
| **Authentication** | Cơ chế xác thực: JWT / OAuth |
| **Authorization** | Phân quyền theo Role / Resource |
| **Data Protection** | Mã hóa dữ liệu nhạy cảm (PII) |
| **Secret Management** | Lưu secret ở Vault / Env var — không hardcode |
| **Rate Limiting** | Bật rate limit trên mọi public endpoint |
| **CORS** | Chỉ cho phép domain whitelist |
| **CSRF** | Bật CSRF protection |
| **Audit Log** | Log mọi hành động thay đổi dữ liệu |

### 6.2 Performance Targets
| Chỉ số | Mục tiêu |
|---|---|
| API Response Time | ≤ ? ms (p95) |
| Throughput | ≥ ? req/s |
| Concurrent Users | ≥ ? users |
| Availability (SLA) | ≥ ?% uptime |
| CPU Usage | ≤ ?% |
| Memory Usage | ≤ ? MB |

---

## 7. 🚀 DevOps & Environments
> *Nguồn: DevOps/devopsenvi.md*

### 7.1 Environments
| Env | Mục đích | URL |
|---|---|---|
| Local | Dev cá nhân | localhost |
| Dev | Tích hợp CI | dev.example.com |
| UAT | Test nghiệm thu | uat.example.com |
| Staging | Pre-prod | staging.example.com |
| Production | Live | example.com |

### 7.2 Deployment
- Container: `[ ] Docker  [ ] Kubernetes`
- CI/CD tool: ...
- Quy trình: `PR → CI build → Test → Deploy Dev → UAT → Staging → Prod`

### 7.3 Monitoring & Logging
- Monitor tool: ...
- Log tập trung: ...
- Backup policy: ...

---

## 8. 🤖 AI Working Rules
> *Nguồn: AIContext/aiworkingrules.md, AIContext/references.md*

### 8.1 AI phải làm gì ALWAYS
- Đọc đủ context trước khi code
- Tuân thủ coding convention (mục 4)
- Sinh đủ artifact: Unit Test, Swagger, Migration, README

### 8.2 AI KHÔNG được làm (Never)
- Hardcode credential
- Tạo file ngoài folder structure đã định
- Bỏ qua validation và error handling

### 8.3 Before Coding — AI phải đọc
- [ ] PRD / BRD / User Story
- [ ] Architecture doc (mục 3)
- [ ] API Spec (mục 3.5)
- [ ] Coding Standards (mục 4)
- [ ] Figma / Wireframe (nếu có)

### 8.4 While Coding — AI phải tuân thủ
- Đúng naming convention
- Đúng folder / layer structure
- Không vi phạm danh sách Forbidden (mục 4.5)

### 8.5 Before Finishing — AI phải kiểm tra
- [ ] Unit test đã viết chưa?
- [ ] Swagger/OpenAPI đã update chưa?
- [ ] Migration script đã có chưa?
- [ ] README đã cập nhật chưa?

### 8.6 Tài liệu tham chiếu AI cần đọc thêm
| Loại | Tài liệu |
|---|---|
| Business | PRD / BRD / User Story |
| Technical | ADR / Architecture / API Spec |
| Design | Figma / Wireframe |
| Dev | Coding Standards / Prompt Library / Knowledge Base |
| External | Vendor Docs / Framework Docs / RFC |

---

## 9. 📖 Business Domain & Glossary
> *Nguồn: BC/businessdomain.md, BC/glossary.md*

### 9.1 Domain Overview
- **Domain là gì?** ...
- **Các Business Entity chính:** ...
- **Quy trình nghiệp vụ chính:** ...
- **Business Rules luôn phải tuân thủ:** ...
- **Actors (vai trò):** ...
- **Edge Cases cần xử lý:** ...

### 9.2 Business Events
| Sự kiện | Trigger | Kết quả |
|---|---|---|
| ... | ... | ... |

### 9.3 Entity State Machine
| Entity | Trạng thái | Chuyển đổi |
|---|---|---|
| ... | [Draft → Active → Closed] | ... |

### 9.4 Glossary
| Thuật ngữ | Ý nghĩa |
|---|---|
| API | Application Programming Interface |
| SKU | Stock Keeping Unit |
| SO | Sales Order |
| PO | Purchase Order |
| ERP | Enterprise Resource Planning |
| CRM | Customer Relationship Management |

---

## 10. 📝 Decision Log
> *Mọi quyết định đã CHỐT — không bàn lại trừ khi có blocker nghiêm trọng*

| # | Ngày | Quyết định | Lý do | Người chốt |
|---|---|---|---|---|
| D-001 | YYYY-MM-DD | ... | ... | ... |

---

*Cập nhật lần cuối: 2026-07-08 | Mọi thay đổi spec phải được Team Lead approve trước khi merge.*
