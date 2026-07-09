# Project Structure — Nền tảng AI Learning Analytics

> Trả lời câu hỏi: Source code được tổ chức như thế nào?
> ⚠️ Cấu trúc được thiết kế cho AI Agentic: Các service truyền thống (analytics, intervention) trở thành "Tools" mà AI Agent orchestration layer gọi.

---

## 1. Tổng quan kiến trúc 3 lớp

```
┌─────────────────────────────────────────────────┐
│              PRESENTATION LAYER                  │
│        (Next.js Frontend + FastAPI Router)        │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│              AI AGENT LAYER (mới)                │
│   Agents → Workflows → Tools → Memory           │
│   (LangGraph orchestration)                      │
└───────────────────────┬─────────────────────────┘
                        │ gọi xuống
┌───────────────────────▼─────────────────────────┐
│              SERVICE LAYER (tools)               │
│   auth │ data_import │ analytics │ intervention  │
│   (router → service → repository → DB)           │
└─────────────────────────────────────────────────┘
```

**Nguyên tắc quan trọng:**
- Service Layer = code truyền thống, xử lý CRUD và business logic đơn
- AI Agent Layer = bộ não, orchestrate nhiều services để giải quyết bài toán phức tạp
- Router có thể gọi trực tiếp Service (cho API đơn giản như login)
- Router gọi Agent (cho API cần AI: insights, recommendations, smart reminders)

---

## 2. Folder Structure

```
project-root/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                          # FastAPI app entry point
│   │   ├── config.py                        # Pydantic Settings (.env)
│   │   ├── database.py                      # SQLAlchemy async engine + session
│   │   ├── dependencies.py                  # get_db(), get_current_teacher()
│   │   │
│   │   ├── agents/                          # ← AI AGENT LAYER (Agentic Core)
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── analyst/                     # Agent 1: Phân tích dữ liệu
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py                 # LangGraph state graph definition
│   │   │   │   ├── prompts.py               # System prompts, few-shot examples
│   │   │   │   └── nodes.py                 # Graph nodes (analyze, reason, recommend)
│   │   │   │
│   │   │   ├── advisor/                     # Agent 2: Tư vấn cải thiện (tương lai)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── nodes.py
│   │   │   │
│   │   │   ├── tools/                       # Tools = wrapper quanh services
│   │   │   │   ├── __init__.py
│   │   │   │   ├── analytics_tools.py       # get_dashboard(), get_drop_off() → LangChain Tool
│   │   │   │   ├── data_tools.py            # get_lesson_stats(), get_student_list() → Tool
│   │   │   │   ├── intervention_tools.py    # draft_reminder(), check_cooldown() → Tool
│   │   │   │   └── search_tools.py          # (tương lai) semantic search bài giảng
│   │   │   │
│   │   │   ├── memory/                      # Agent Memory
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py                # SQLAlchemy: AgentConversation, AgentMemoryEntry
│   │   │   │   └── store.py                 # PostgreSQL-backed memory store
│   │   │   │
│   │   │   └── workflows/                   # Multi-step orchestration
│   │   │       ├── __init__.py
│   │   │       ├── insight_workflow.py       # Drop-off → Analyze → Reason → Recommend
│   │   │       └── reminder_workflow.py      # Identify at-risk → Draft message → Review
│   │   │
│   │   ├── modules/                         # ← SERVICE LAYER (Business Logic + DB)
│   │   │   ├── auth/                        # US-001: Đăng nhập
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py               # POST /api/v1/auth/login
│   │   │   │   ├── service.py              # authenticate(), generate_jwt()
│   │   │   │   ├── repository.py           # get_teacher_by_email()
│   │   │   │   ├── models.py               # SQLAlchemy: Teacher
│   │   │   │   └── schemas.py              # Pydantic: LoginRequest, LoginResponse
│   │   │   │
│   │   │   ├── data_import/                 # US-002: Import dữ liệu Udemy
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py               # POST /data/upload, POST /data/udemy-connection
│   │   │   │   ├── service.py              # create_import(), connect_udemy()
│   │   │   │   ├── repository.py
│   │   │   │   ├── models.py               # DataImport, UdemyConnection
│   │   │   │   ├── schemas.py
│   │   │   │   ├── tasks.py                # Celery: parse_uploaded_file()
│   │   │   │   └── parser.py               # CSV/XLSX parsing + anonymization
│   │   │   │
│   │   │   ├── analytics/                   # US-003, US-004: Dashboard + Drop-off
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py               # GET /courses, /dashboard, /drop-off-analysis
│   │   │   │   ├── service.py              # get_dashboard(), get_drop_off_analysis()
│   │   │   │   ├── repository.py           # Aggregate queries
│   │   │   │   ├── models.py               # Course, Module, Lesson, StudentEnrollment, LearningActivity
│   │   │   │   └── schemas.py
│   │   │   │
│   │   │   └── intervention/               # US-006: Nhắc nhở học viên
│   │   │       ├── __init__.py
│   │   │       ├── router.py               # GET /at-risk-students, POST /send-reminder
│   │   │       ├── service.py              # get_at_risk_students(), send_reminders()
│   │   │       ├── repository.py
│   │   │       ├── models.py               # ReminderLog
│   │   │       ├── schemas.py
│   │   │       ├── tasks.py                # Celery: send_email_task()
│   │   │       └── template_builder.py
│   │   │
│   │   └── shared/                          # Code dùng chung
│   │       ├── __init__.py
│   │       ├── exceptions.py                # Custom exceptions + global handler
│   │       ├── response.py                  # StandardResponse[T]
│   │       ├── middleware.py                # CorrelationId, Logging
│   │       ├── security.py                  # JWT, bcrypt
│   │       ├── encryption.py                # AES encrypt/decrypt
│   │       └── utils.py                     # mask_name(), date helpers
│   │
│   ├── alembic/                             # DB migrations
│   ├── tests/
│   │   ├── test_agents/                     # Test agent workflows
│   │   │   ├── test_analyst_agent.py
│   │   │   └── test_insight_workflow.py
│   │   ├── test_auth/
│   │   ├── test_data_import/
│   │   ├── test_analytics/
│   │   └── test_intervention/
│   │
│   ├── .env.example
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── alembic.ini
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/                             # Next.js App Router
│   │   │   ├── layout.tsx                   # Root layout + providers
│   │   │   ├── page.tsx                     # Landing → redirect to /login
│   │   │   ├── login/
│   │   │   │   └── page.tsx                 # Login form
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx                 # Course list + KPI overview
│   │   │   └── courses/
│   │   │       └── [courseId]/
│   │   │           ├── page.tsx             # Course dashboard
│   │   │           ├── drop-off/
│   │   │           │   └── page.tsx         # Drop-off funnel chart
│   │   │           ├── insights/
│   │   │           │   └── page.tsx         # AI insights panel
│   │   │           └── reminders/
│   │   │               └── page.tsx         # At-risk students + send reminder
│   │   │
│   │   ├── components/                      # Reusable UI components
│   │   │   ├── ui/                          # shadcn/ui components (auto-generated)
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   └── ...
│   │   │   ├── charts/                      # Custom chart components
│   │   │   │   ├── funnel-chart.tsx         # Drop-off funnel (Recharts)
│   │   │   │   ├── timeline-chart.tsx       # Video stop timeline
│   │   │   │   └── kpi-card.tsx             # Dashboard KPI cards
│   │   │   └── layout/
│   │   │       ├── sidebar.tsx              # Navigation sidebar
│   │   │       └── header.tsx               # Top header + user menu
│   │   │
│   │   ├── lib/                             # Utilities + API client
│   │   │   ├── api.ts                       # Fetch wrapper + JWT interceptor
│   │   │   ├── utils.ts                     # cn() helper for tailwind merge
│   │   │   └── constants.ts                 # API URLs, thresholds
│   │   │
│   │   ├── hooks/                           # Custom React hooks
│   │   │   ├── use-auth.ts                  # JWT token management
│   │   │   ├── use-courses.ts               # TanStack Query: fetch courses
│   │   │   └── use-dashboard.ts             # TanStack Query: fetch dashboard
│   │   │
│   │   └── types/                           # TypeScript type definitions
│   │       ├── api.ts                       # API response types
│   │       ├── course.ts                    # Course, Lesson, Module
│   │       └── student.ts                   # Student, Reminder
│   │
│   ├── public/
│   ├── tailwind.config.ts
│   ├── components.json                      # shadcn/ui config
│   ├── next.config.js
│   ├── tsconfig.json
│   └── package.json
│
└── docs/                                    # Tài liệu dự án (từ wetransform_udemy)
```

---

## 3. Layer Structure

### Layer 1: Presentation (Router / Next.js Pages)
| Vị trí | Chức năng | Quy tắc |
|---|---|---|
| `modules/*/router.py` | Nhận HTTP request, validate, gọi Service hoặc Agent | KHÔNG chứa business logic |
| `frontend/src/app/*/page.tsx` | UI pages, gọi API, hiển thị data | KHÔNG chứa business logic |

### Layer 2: AI Agent (Orchestration) — **MỚI**
| Vị trí | Chức năng | Quy tắc |
|---|---|---|
| `agents/analyst/agent.py` | LangGraph state graph — điều phối phân tích multi-step | Gọi Tools, không truy cập DB trực tiếp |
| `agents/tools/*.py` | Wrapper quanh Service methods → LangChain Tool format | Mỗi tool = 1 function, có description rõ ràng |
| `agents/memory/store.py` | Lưu/đọc conversation history, teacher feedback | PostgreSQL-backed |
| `agents/workflows/*.py` | Chuỗi agent steps cho 1 use case cụ thể | Composable, testable |

### Layer 3: Service (Business Logic + DB)
| Vị trí | Chức năng | Quy tắc |
|---|---|---|
| `modules/*/service.py` | Business logic, invariants check | Không biết Agent tồn tại — hoạt động độc lập |
| `modules/*/repository.py` | Truy vấn DB (SQLAlchemy) | Chỉ query, không business logic |
| `modules/*/models.py` | SQLAlchemy ORM models | Mapping table ↔ Python class |
| `modules/*/schemas.py` | Pydantic DTOs | Validate input, serialize output |

### Quy tắc gọi:
```
Router → Agent → Tools → Service → Repository → DB      (AI flow)
Router → Service → Repository → DB                       (Simple flow: login, upload)
```

---

## 4. Ví dụ: Agent gọi Tools thay vì gọi OpenAI trực tiếp

### Cách cũ (KHÔNG agentic):
```python
# ai_insights/service.py
class AIInsightService:
    async def get_insights(self, lesson_id):
        stats = await self.repo.get_lesson_stats(lesson_id)
        prompt = f"Bài học có drop-off {stats.drop_off_rate}..."
        response = openai.chat.completions.create(prompt=prompt)  # 1 call, xong
        return parse(response)
```

### Cách mới (Agentic):
```python
# agents/tools/analytics_tools.py
@tool
def get_drop_off_stats(course_id: str, lesson_id: str) -> dict:
    """Lấy thống kê drop-off của bài học: tỷ lệ bỏ cuộc, số học viên, mốc dừng video."""
    service = AnalyticsService(...)
    return service.get_drop_off_analysis(course_id, lesson_id)

@tool
def get_student_behavior(lesson_id: str) -> dict:
    """Lấy hành vi chi tiết: thời gian xem trung bình, mốc giây dừng nhiều nhất."""
    service = AnalyticsService(...)
    return service.get_video_timeline(lesson_id)

# agents/analyst/agent.py
from langgraph.graph import StateGraph

def create_analyst_agent():
    graph = StateGraph(AnalystState)
    graph.add_node("analyze", analyze_data)      # Gọi get_drop_off_stats tool
    graph.add_node("reason", reason_why)          # LLM suy luận nguyên nhân
    graph.add_node("recommend", generate_recs)    # LLM đề xuất hành động
    graph.add_node("review", human_review)        # Giáo viên approve/reject
    
    graph.add_edge("analyze", "reason")
    graph.add_edge("reason", "recommend")
    graph.add_edge("recommend", "review")
    
    return graph.compile()
```

**Lợi ích:**
- Agent TỰ QUYẾT ĐỊNH gọi tool nào, theo thứ tự nào
- Có thể thêm tool mới mà không sửa Agent code
- Memory giúp Agent nhớ feedback → đề xuất tốt hơn theo thời gian
- Tương lai: thêm Agent mới (Advisor, Engagement) mà không phá vỡ code cũ

---

## 5. Shared Components

| File | Chức năng | Dùng ở đâu |
|---|---|---|
| `shared/exceptions.py` | Custom exceptions + global handler | Mọi module + agents |
| `shared/response.py` | StandardResponse[T] wrapper | Mọi router |
| `shared/middleware.py` | CorrelationId, Logging | main.py |
| `shared/security.py` | JWT, bcrypt | auth module |
| `shared/encryption.py` | AES encrypt/decrypt | data_import, intervention |
| `shared/utils.py` | mask_name(), date helpers | data_import, intervention |

---

## 6. Configuration

### `.env.example`
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/learning_analytics

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI / LLM
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
LANGCHAIN_TRACING_V2=true
LANGSMITH_API_KEY=your-langsmith-key       # Agent tracing & debugging

# Email
SENDGRID_API_KEY=your-sendgrid-key-here
FROM_EMAIL=noreply@learning-analytics.com

# Encryption
AES_SECRET_KEY=your-32-byte-encryption-key

# App
APP_ENV=development
LOG_LEVEL=INFO
```

### `docker-compose.yml` (5 services)
```yaml
services:
  api:           # FastAPI backend
  frontend:      # Next.js frontend
  db:            # PostgreSQL 16
  redis:         # Redis 7 (cache + Celery broker)
  celery:        # Celery worker (parse file, agent execution, send email)
```

---

*Cập nhật: 2026-07-09 | Owner: AI Engineering (Phan Đức Duy)*