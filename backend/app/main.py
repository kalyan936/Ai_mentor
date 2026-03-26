"""
AI Mentor - FastAPI Application Entry Point.

Main application with all routes, CORS, and startup/shutdown events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.logging_config import setup_logging
from .db.database import init_db

# Initialize logging
setup_logging()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and services on startup."""
    init_db()
    from loguru import logger
    logger.info(f"🚀 {settings.app_name} v{settings.app_version} started")
    logger.info(f"📚 LLM Provider: {settings.llm_provider} | Model: {settings.llm_model}")
    logger.info(f"💾 Database: {settings.database_url}")
    yield


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Adaptive Learning Platform with Multi-Agent System",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
from .api.routes.users import router as users_router
from .api.routes.roadmap import router as roadmap_router
from .api.routes.lessons import router as lessons_router
from .api.routes.quiz import router as quiz_router
from .api.routes.code import router as code_router
from .api.routes.progress import router as progress_router
from .api.routes.memory import router as memory_router
from .api.routes.projects import router as projects_router

app.include_router(users_router, prefix="/api")
app.include_router(roadmap_router, prefix="/api")
app.include_router(lessons_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")
app.include_router(code_router, prefix="/api")
app.include_router(progress_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(projects_router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    """API health check."""
    return {"status": "healthy", "llm_provider": settings.llm_provider}
