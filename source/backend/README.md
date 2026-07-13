# WeTransform Backend - AI Learning Analytics Platform

Nền tảng AI Learning Analytics kết hợp kiến trúc Agentic AI giúp giáo viên phân tích mức độ tương tác (drop-off) và tự động hóa quy trình hỗ trợ học viên (intervention).

---

## 🚀 Công nghệ & Kiến trúc
- **Ngôn ngữ & Framework**: Python 3.11+, FastAPI (Async).
- **Database & ORM**: PostgreSQL, SQLAlchemy, Alembic (Migration).
- **Cache**: Redis.
- **AI/Agent Layer**: LangGraph, LangChain, OpenAI.
- **Code Quality**: Ruff, Black, Mypy, Pre-commit.
- **Testing**: Pytest, TestContainers (dành cho Integration test).
- **Observability**: OpenTelemetry (Tracing), Prometheus (Metrics), Jaeger (Traces).
- **DevOps**: Docker, Docker Compose, GitHub Actions (CI/CD).

---

## 🛠 Hướng dẫn Khởi chạy (Local Development)

### 1. Yêu cầu hệ thống
- **Python:** 3.11 trở lên.
- **Docker & Docker Compose:** Yêu cầu bắt buộc để chạy các service phụ trợ (Postgres, Redis, Jaeger, Prometheus).
- **Git**

### 2. Cấu hình môi trường

Mở terminal và di chuyển vào thư mục backend:
```bash
cd source/backend
```

**Bước 1: Tạo môi trường ảo (Virtual Environment)**
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # Trên macOS/Linux
# Hoặc: .venv\Scripts\activate (Trên Windows)
```

**Bước 2: Cài đặt thư viện & Pre-commit Hooks**
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt git hooks (Ruff, Black, Mypy) để tự động kiểm tra code khi commit
pre-commit install
```

**Bước 3: Cấu hình biến môi trường**
Sao chép file mẫu để tạo file `.env`:
```bash
cp .env.example .env
```
Mở file `.env` và điền đầy đủ các thông tin:
- `DATABASE_URL=postgresql+asyncpg://admin:admin_password@localhost:5432/learning_analytics`
- `REDIS_URL=redis://localhost:6379/0`
- `OPENAI_API_KEY=sk-...` (Bắt buộc cho AI Agents)
- Các cấu hình bảo mật khác (`JWT_SECRET_KEY`, `AES_SECRET_KEY`).

### 3. Khởi động các Services bằng Docker
Khởi động cơ sở dữ liệu, Cache và các công cụ Observability (Jaeger, Prometheus):
```bash
docker-compose up -d
```
*Các services sẽ chạy ở các port sau:*
- **PostgreSQL**: `5432`
- **Redis**: `6379`
- **Jaeger UI**: `http://localhost:16686`
- **Prometheus UI**: `http://localhost:9090`

### 4. Khởi chạy Backend API
Khởi chạy FastAPI server (tự động reload khi có thay đổi code):
```bash
uvicorn app.main:app --reload
```
- **API Base URL**: `http://localhost:8000`
- **Health Check**: `http://localhost:8000/health`
- **Swagger UI (Docs)**: `http://localhost:8000/docs`
- **Metrics (Prometheus)**: `http://localhost:8000/metrics`

---

## 🧪 Kiểm thử (Testing)

Dự án sử dụng `pytest` cho Unit Test và Integration Test.

```bash
# Chạy toàn bộ tests
pytest

# Chạy test với thông tin coverage
pytest --cov=app tests/
```

---

## 🧹 Code Quality & Linting

Chúng tôi sử dụng `pre-commit` để đảm bảo code luôn sạch sẽ và đúng chuẩn trước khi push.
Bạn có thể chạy kiểm tra thủ công bằng lệnh:
```bash
pre-commit run --all-files
```

Các công cụ được tích hợp:
- **Ruff**: Linter cực nhanh.
- **Black**: Tự động format code (độ dài dòng 88).
- **Mypy**: Kiểm tra kiểu dữ liệu tĩnh (Static type checking).
- Tự động xóa trailing whitespace và fix end-of-file.

---

## 🏗 Cấu trúc thư mục

Kiến trúc backend được chia thành các lớp chức năng tách biệt chặt chẽ (Modular Architecture):

```text
app/
├── main.py              # Entrypoint của ứng dụng FastAPI
├── config.py            # Quản lý biến môi trường (Pydantic Settings)
├── database.py          # Cấu hình kết nối DB (SQLAlchemy Async)
├── agents/              # [Phase 6] Chứa các LangGraph AI Agents (Advisor, Analyst...)
├── modules/             # Các domain-driven modules
│   ├── auth/            # Tính năng đăng nhập, phân quyền (RBAC)
│   ├── analytics/       # API lấy dữ liệu thống kê, biểu đồ
│   └── intervention/    # Quản lý các chiến dịch hỗ trợ học viên
└── shared/              # Tiện ích dùng chung toàn hệ thống
    ├── audit.py         # Ghi log sự kiện Audit Trail
    ├── observability.py # OpenTelemetry (Tracing, Metrics)
    ├── exceptions.py    # Error handling chuẩn hóa (AppException)
    ├── response.py      # Format Standard Response
    └── security.py      # Mã hóa mật khẩu, JWT...
```

---

## 🚀 CI/CD & Triển khai
- Dự án sử dụng **GitHub Actions** để tự động hóa quá trình Build, Test và Linting khi có Pull Request.
- Ứng dụng Backend cũng như toàn bộ dịch vụ phụ trợ đều đã được định nghĩa trong `docker-compose.yml`.
- Quy trình Backup dữ liệu tự động đã được thiết lập (sử dụng scripts trong `scripts/backup_db.sh`).
