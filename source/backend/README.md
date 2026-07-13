# AI Learning Analytics Platform

Nền tảng AI Learning Analytics kết hợp kiến trúc Agentic AI giúp giáo viên phân tích mức độ tương tác (drop-off) và tự động hóa quy trình hỗ trợ học viên (intervention).

## 🚀 Công nghệ sử dụng
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery.
- **AI/Agent Layer**: LangGraph, LangChain, OpenAI.
- **Frontend**: Next.js 14 (App Router), Tailwind CSS, shadcn/ui.

---

## 🛠 Hướng dẫn cài đặt & Khởi chạy dự án (Local Development)

### 1. Yêu cầu hệ thống cơ bản
- **Python:** 3.11 trở lên
- **Node.js:** 18.x trở lên
- **Database / Cache:** PostgreSQL (16+) và Redis (7+)
- **Docker & Docker Compose** (Nếu muốn chạy DB/Cache thông qua container)

### 2. Khởi chạy Backend (FastAPI + AI Agents)

Mở terminal và trỏ vào thư mục backend:
```bash
cd source/backend
```

**Bước 1: Tạo môi trường ảo (Virtual Environment)**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Trên macOS/Linux
# Hoặc: .venv\Scripts\activate (Trên Windows)
```

**Bước 2: Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

**Bước 3: Cấu hình biến môi trường**
Copy file mẫu để tạo file `.env`:
```bash
cp .env.example .env
```
*(Hãy điền các thông số kết nối Database, OpenAI API Key, JWT Secret... vào file `.env`)*

**Bước 4: Khởi chạy Server Backend**
```bash
uvicorn app.main:app --reload
```
API server sẽ chạy tại: `http://localhost:8000`
Swagger UI Documentation: `http://localhost:8000/docs`

---

### 3. Khởi chạy Frontend (Next.js)

Mở một tab terminal mới và trỏ vào thư mục frontend:
```bash
cd source/frontend
```

**Bước 1: Cài đặt package**
```bash
npm install
# Hoặc: pnpm install / yarn install
```

**Bước 2: Chạy Frontend Server**
```bash
npm run dev
```
Giao diện người dùng sẽ chạy tại: `http://localhost:3000`

---

## 🐳 Khởi chạy bằng Docker (Dành cho Staging/Production)

Nếu bạn không muốn cài đặt thủ công, bạn có thể khởi chạy toàn bộ dịch vụ (API, DB, Redis, Celery, Frontend) bằng Docker Compose (Đang cập nhật cấu hình ở phase sau):

```bash
cd source
docker-compose up --build -d
```

---

## 🏗 Cấu trúc dự án

- `/source/backend/app/main.py`: Entrypoint của FastAPI.
- `/source/backend/app/modules/`: Chứa các API module (auth, data_import, analytics, intervention).
- `/source/backend/app/agents/`: Chứa các luồng xử lý AI (LangGraph orchestration).
- `/source/frontend/src/app/`: Chứa UI Layout và Pages (Next.js).
