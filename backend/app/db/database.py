"""
AI Mentor - Database Connection & Session Management.

Uses SQLAlchemy async engine with SQLite for the MVP.
Provides session dependency injection for FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from ..core.config import get_settings

settings = get_settings()

# SQLite engine (synchronous for simplicity in MVP)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=settings.debug,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db() -> Session:
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables."""
    from ..models import user, roadmap, progress, quiz, code_submission, memory, project  # noqa
    Base.metadata.create_all(bind=engine)
