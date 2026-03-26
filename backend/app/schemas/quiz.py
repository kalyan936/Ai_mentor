"""
AI Mentor - Quiz Schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class QuizQuestion(BaseModel):
    """A single quiz question."""
    question_id: int
    question: str
    question_type: str  # mcq/true_false/short_answer/code
    options: Optional[List[str]] = None  # For MCQ
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: str = "medium"
    points: int = 10


class QuizGenerateRequest(BaseModel):
    """Request to generate a quiz."""
    user_id: int
    topic: str
    subtopic: Optional[str] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard|adaptive)$")
    num_questions: int = Field(default=5, ge=1, le=20)
    question_types: List[str] = ["mcq", "true_false", "short_answer"]


class QuizSubmitRequest(BaseModel):
    """Submit quiz answers."""
    user_id: int
    quiz_id: Optional[int] = None
    topic: str
    subtopic: Optional[str] = None
    questions: List[Dict[str, Any]]  # Question objects
    answers: List[str]  # User's answers
    time_taken_seconds: Optional[int] = None


class QuizResultResponse(BaseModel):
    """Quiz result with feedback."""
    quiz_id: int
    score: float
    total_questions: int
    correct_count: int
    results: List[Dict[str, Any]]  # Per-question results
    feedback: str
    weak_areas: List[str]
    recommendations: List[str]
    mastery_update: Optional[Dict[str, Any]] = None

    model_config = {
        "from_attributes": True
    }
