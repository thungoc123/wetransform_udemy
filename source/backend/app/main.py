from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.shared.logger import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo structlog khi app khởi động
    setup_logging()
    yield
    # Cleanup nếu cần

tags_metadata = [
    {
        "name": "Auth",
        "description": "Operations with authentication and teachers.",
    },
    {
        "name": "System",
        "description": "Health checks and system operations.",
    },
]

app = FastAPI(
    title="AI Learning Analytics API",
    description="Backend API for AI Learning Analytics Platform. Tích hợp AI để phân tích điểm dừng và cảnh báo học sinh.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

from fastapi.middleware.cors import CORSMiddleware

# Import routers from modules
from app.modules.auth import router as auth_router
from app.modules.data_import import router as data_import_router
from app.modules.analytics import router as analytics_router
from app.modules.intervention import router as intervention_router

from fastapi.exceptions import RequestValidationError
from app.shared.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    global_exception_handler
)

# Register Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Import custom middleware
from app.shared.middleware import SecurityHeadersMiddleware, LoggingMiddleware
from app.shared.rate_limit import RateLimitMiddleware

# Add Logging Middleware first so it wraps everything
app.add_middleware(LoggingMiddleware)

# Add Rate Limit Middleware
app.add_middleware(RateLimitMiddleware)

# Add Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Advanced CORS configuration (FND-015)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", # Next.js frontend
        # Add production frontend URL here later
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Include module routers
app.include_router(auth_router)
app.include_router(data_import_router)
app.include_router(analytics_router)
app.include_router(intervention_router)

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.shared.dependencies.database import get_db

@app.get("/health", tags=["System"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint to verify API and Database connection."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "service": "AI Learning Analytics API"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "service": "AI Learning Analytics API", "details": str(e)}
