"""
AI Mentor - Progress & Dashboard API Routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...services.progress_service import (
    get_dashboard_data, get_topic_progress, get_weak_areas, update_progress
)
from ...schemas.progress import ProgressUpdate

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/dashboard/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive dashboard data for a user."""
    return get_dashboard_data(db, user_id)


@router.get("/{user_id}/{topic}")
def get_progress(user_id: int, topic: str, db: Session = Depends(get_db)):
    """Get progress for a specific topic."""
    return get_topic_progress(db, user_id, topic)


@router.post("/update")
def update_user_progress(request: ProgressUpdate, db: Session = Depends(get_db)):
    """Update learning progress."""
    progress = update_progress(
        db, request.user_id, request.topic, request.subtopic,
        status=request.status,
        score=request.score,
        time_spent=request.time_spent_minutes,
    )
    return {
        "topic": progress.topic,
        "subtopic": progress.subtopic,
        "status": progress.status,
        "mastery_level": progress.mastery_level,
        "score": progress.score,
    }


@router.get("/weak-areas/{user_id}")
def get_user_weak_areas(user_id: int, db: Session = Depends(get_db)):
    """Get identified weak areas for a user."""
    return get_weak_areas(db, user_id)

