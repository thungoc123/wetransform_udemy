from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from modules
from app.modules.auth import router as auth_router
from app.modules.data_import import router as data_import_router
from app.modules.analytics import router as analytics_router
from app.modules.intervention import router as intervention_router

app = FastAPI(
    title="AI Learning Analytics API",
    description="Backend API for AI Learning Analytics Platform",
    version="1.0.0"
)

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

# Basic CORS configuration (will be expanded in FND-015)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
from app.dependencies import get_db

@app.get("/health", tags=["System"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint to verify API and Database connection."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "service": "AI Learning Analytics API"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "service": "AI Learning Analytics API", "details": str(e)}
