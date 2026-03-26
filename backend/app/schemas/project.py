"""
AI Mentor - Project Schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProjectSuggestionRequest(BaseModel):
    """Request project suggestions."""
    user_id: int
    topic: str
    difficulty: Optional[str] = None


class ProjectSuggestionResponse(BaseModel):
    """Suggested project."""
    title: str
    description: str
    topic: str
    difficulty: str
    requirements: List[str]
    learning_outcomes: List[str]
    estimated_hours: float
    skills_practiced: List[str]
    starter_guidance: Optional[str] = None


class ProjectSubmitRequest(BaseModel):
    """Submit a project for review."""
    user_id: int
    project_title: str
    topic: str
    description: str
    submitted_code: Optional[str] = None
    repo_link: Optional[str] = None


class ProjectReviewResponse(BaseModel):
    """Project review from mentor agent."""
    submission_id: int
    score: float
    feedback: str
    strengths: List[str]
    improvements: List[str]
    skills_demonstrated: List[str]
    next_steps: List[str]

    model_config = {
        "from_attributes": True
    }


class TutorChatRequest(BaseModel):
    """Chat request to the tutor agent."""
    user_id: int
    message: str
    topic: Optional[str] = None
    subtopic: Optional[str] = None
    context: Optional[str] = None  # lesson/quiz/coding/general


class TutorChatResponse(BaseModel):
    """Tutor agent chat response."""
    response: str
    suggested_followup: List[str] = []
    related_topics: List[str] = []
    code_examples: Optional[List[Dict[str, str]]] = None
