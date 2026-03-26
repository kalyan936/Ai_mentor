"""
AI Mentor - Progress Schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProgressUpdate(BaseModel):
    """Update lesson progress."""
    user_id: int
    topic: str
    subtopic: str
    status: str = "in_progress"
    score: Optional[float] = None
    time_spent_minutes: Optional[float] = None


class ProgressResponse(BaseModel):
    """Individual lesson progress response."""
    id: int
    topic: str
    subtopic: str
    status: str
    score: float
    attempts: int
    mastery_level: str
    time_spent_minutes: float

    model_config = {
        "from_attributes": True
    }


class TopicMastery(BaseModel):
    """Mastery summary for a topic."""
    topic: str
    overall_mastery: float  # 0-100
    mastery_level: str
    completed_subtopics: int
    total_subtopics: int
    avg_score: float
    total_time_minutes: float
    weak_areas: List[str]
    strong_areas: List[str]


class DashboardResponse(BaseModel):
    """Full dashboard data."""
    user_name: str
    streak_days: int
    total_study_minutes: float
    topics_mastery: List[TopicMastery]
    recent_activity: List[Dict[str, Any]]
    recommended_next: Optional[Dict[str, Any]] = None
    overall_progress: float  # 0-100 overall completion
    achievements: List[Dict[str, Any]] = []
