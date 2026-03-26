"""
AI Mentor - Roadmap Schemas.

Pydantic models for roadmap generation and retrieval.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class RoadmapModule(BaseModel):
    """A single module in the learning roadmap."""
    module_id: int
    title: str
    description: str
    subtopics: List[str]
    estimated_hours: float
    difficulty: str  # beginner/intermediate/advanced
    prerequisites: List[str] = []
    status: str = "locked"  # locked/available/in_progress/completed


class RoadmapGenerateRequest(BaseModel):
    """Request to generate a personalized roadmap."""
    user_id: int
    topic: str = Field(..., description="Topic slug: python, mysql, ml, dl, nlp, genai, agentic")
    current_level: str = Field(default="beginner")
    goals: Optional[str] = None
    daily_study_time: int = Field(default=30)


class RoadmapResponse(BaseModel):
    """Full roadmap response."""
    id: int
    user_id: int
    topic: str
    modules: List[RoadmapModule]
    current_stage: int
    total_stages: int
    next_recommended_task: Optional[Dict[str, Any]] = None
    status: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class NextTaskResponse(BaseModel):
    """Recommended next learning action."""
    task_type: str  # lesson/quiz/coding_challenge/project/revision
    topic: str
    subtopic: str
    title: str
    description: str
    estimated_minutes: int
    priority: str  # high/medium/low
    reason: str  # Why this task is recommended
