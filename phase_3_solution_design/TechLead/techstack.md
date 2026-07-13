# Tech Stack — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: Dự án sử dụng công nghệ gì?
> Mọi lựa chọn công nghệ đều được truy ngược về yêu cầu nghiệp vụ cụ thể từ Phase 1 & 2.
> ⚠️ Dự án định hướng AI Agentic trong tương lai — tech stack được chọn để hỗ trợ điều đó.

---

## Frontend

| Hạng mục | Công nghệ | Phiên bản | Lý do chọn |
|---|---|---|---|
| **Framework** | Next.js | 14.x (App Router) | SSR + API Routes + file-based routing. Nền tảng production-ready, dễ deploy Vercel. Tương lai có thể dùng Server Actions cho AI streaming |
| **UI Library** | shadcn/ui + Radix UI | latest | Nhẹ, composable, không lock-in. Copy component vào project, full control. Đẹp mặc định |
| **Styling** | Tailwind CSS | 3.x | shadcn/ui yêu cầu Tailwind. Utility-first, nhanh, nhất quán |
| **Charts** | Recharts | 2.x | Biểu đồ phễu (Funnel) cho US-004, timeline cho video stop analysis. Native React |
| **State Management** | TanStack Query (React Query) | 5.x | Quản lý server state + caching API. App đọc data nhiều hơn ghi |
| **HTTP Client** | fetch (native) + SWR fallback | — | Next.js tích hợp fetch với caching. Không cần Axios |
| **Icons** | Lucide React | latest | shadcn/ui dùng Lucide mặc định. Nhẹ, tree-shakeable |

---

## Backend

| Hạng mục | Công nghệ | Phiên bản | Lý do chọn |
|---|---|---|---|
| **Language** | Python | 3.11+ | Hệ sinh thái AI/ML mạnh nhất. LangChain, LangGraph, OpenAI SDK đều Python-first |
| **Framework** | FastAPI | 0.110+ | Async native, auto Swagger, type-safe. Dễ expose functions thành Agent Tools |
| **Runtime** | Uvicorn | 0.29+ | ASGI server cho FastAPI |
| **ORM** | SQLAlchemy | 2.0+ | Async support, relationship management |
| **Validation** | Pydantic | 2.x | DTO validation + tích hợp native với FastAPI và LangChain |

---

## AI / Agent Layer (Quan trọng — Định hướng Agentic)

| Hạng mục | Công nghệ | Phiên bản | Lý do chọn |
|---|---|---|---|
| **Agent Framework** | LangGraph | 0.2+ | Đồ thị trạng thái (state graph) cho multi-step agent workflows. Kiểm soát flow tốt hơn LangChain thuần. Hỗ trợ human-in-the-loop (giáo viên approve/reject) |
| **LLM Client** | LangChain Core + OpenAI | latest | Abstraction layer — dễ swap model (GPT-4o → Claude → Local LLM) mà không sửa code agent |
| **Tool Framework** | LangChain Tools | latest | Wrap các service hiện có (analytics, intervention) thành Tools mà Agent gọi được |
| **Memory** | LangChain Memory + PostgreSQL | latest | Agent nhớ context: teacher feedback trước đó, đề xuất đã bỏ qua |
| **Embedding (tương lai)** | OpenAI Embeddings + pgvector | latest | Semantic search trên nội dung bài giảng để AI hiểu context |

**Tại sao chọn LangGraph thay vì chỉ gọi OpenAI API trực tiếp?**
> Gọi OpenAI trực tiếp = 1 prompt → 1 response. Không có planning, không có memory, không có tool use.
> LangGraph = Agent tự lập kế hoạch → gọi nhiều tools → tổng hợp kết quả → hỏi ý kiến giáo viên → điều chỉnh.
> Ví dụ: Agent phân tích bài học → thấy drop-off cao → tự động gọi tool `get_video_timeline()` → phát hiện dừng ở phút 4:30 → sinh đề xuất "chia video tại phút 4:30" → hỏi giáo viên approve.

---

## Database

| Hạng mục | Công nghệ | Phiên bản | Lý do chọn |
|---|---|---|---|
| **Database chính** | PostgreSQL | 16.x | Quan hệ phức tạp. UUID native. JSON column cho LLM raw response. Tương lai: pgvector cho embedding |
| **Cache / Broker** | Redis | 7.x | Cache Dashboard results. Message broker cho Celery |
| **Vector Store (tương lai)** | pgvector (extension) | — | Lưu embedding nội dung bài giảng cho semantic search. Không cần DB riêng |

---

## Infrastructure

| Hạng mục | Công nghệ | Phiên bản | Lý do chọn |
|---|---|---|---|
| **Container** | Docker + Docker Compose | 24.x / 2.x | Gộp tất cả services: API + DB + Redis + Celery + Next.js |
| **Cloud (tương lai)** | Chưa xác định | — | MVP local Docker. Production: AWS/GCP/Vercel |

---

## DevOps

| Hạng mục | Công nghệ | Lý do chọn |
|---|---|---|
| **CI/CD** | GitHub Actions | Repo trên GitHub, tích hợp native |
| **Logging** | structlog (JSON) | Structured log + correlation_id. Agent execution trace |

---

## Third-party

| Hạng mục | Công nghệ | Lý do chọn |
|---|---|---|
| **Auth** | PyJWT + bcrypt | JWT Bearer Token (API Spec đã chốt) |
| **LLM Provider** | OpenAI (GPT-4o) | MVP dùng GPT-4o. LangChain abstraction cho phép đổi provider sau |
| **Background Jobs** | Celery + Redis | Parse file, agent execution dài, gửi email |
| **File Parsing** | pandas + openpyxl | Parse CSV/XLSX từ Udemy |
| **Migration** | Alembic | Chuẩn migration cho SQLAlchemy |
| **Email** | SendGrid / SMTP | Reminder cho học viên (US-006) |
| **Storage** | Local filesystem (MVP) | File CSV/XLSX upload. Production → S3/GCS |

---

## Tổng quan Dependencies

### Backend (requirements.txt)
```
# Core
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Database
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
alembic>=1.13.0

# Auth
pyjwt>=2.8.0
bcrypt>=4.1.0
python-multipart>=0.0.9

# Background Jobs
celery>=5.3.0
redis>=5.0.0

# Data Processing
pandas>=2.2.0
openpyxl>=3.1.0

# AI / Agent (Agentic Architecture)
langchain-core>=0.2.0
langchain-openai>=0.1.0
langgraph>=0.2.0
openai>=1.30.0

# Email
sendgrid>=6.11.0

# Logging
structlog>=24.1.0

# Dev Tools
black>=24.0.0
ruff>=0.4.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

### Frontend (package.json)
```
next: ^14.0.0
react: ^18.0.0
tailwindcss: ^3.0.0
@radix-ui/react-*
class-variance-authority
clsx
tailwind-merge
lucide-react
recharts: ^2.0.0
@tanstack/react-query: ^5.0.0
```

---

> ⚠️ Stack trên KHÔNG được thay đổi trừ khi có blocker nghiêm trọng. Mọi đề xuất đổi stack → ghi vào Decision Log trong Spec.md.

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*
