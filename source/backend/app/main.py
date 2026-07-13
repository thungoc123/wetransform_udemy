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

@app.get("/health", tags=["System"])
async def root_health():
    return {"status": "ok", "service": "AI Learning Analytics API"}
