"""
AI Mentor - Code Submission Schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CodingChallengeRequest(BaseModel):
    """Request to generate a coding challenge."""
    user_id: int
    topic: str
    subtopic: Optional[str] = None
    difficulty: str = Field(default="medium")


class CodingChallengeResponse(BaseModel):
    """Generated coding challenge."""
    challenge_id: str
    title: str
    description: str
    requirements: List[str]
    starter_code: Optional[str] = None
    test_cases: Optional[List[Dict[str, Any]]] = None
    hints: List[str] = []
    difficulty: str
    estimated_minutes: int
    topic: str
    subtopic: Optional[str] = None


class CodeSubmitRequest(BaseModel):
    """Submit code for evaluation."""
    user_id: int
    topic: str
    subtopic: Optional[str] = None
    prompt: str
    submitted_code: str
    language: str = "python"


class CodeResultResponse(BaseModel):
    """Code evaluation result."""
    submission_id: int
    execution_output: Optional[str] = None
    execution_status: str  # success/error/timeout
    errors: Optional[str] = None
    score: float
    feedback: str
    suggestions: List[str]
    best_practices: List[str] = []

    model_config = {
        "from_attributes": True
    }


class DebugRequest(BaseModel):
    """Request to debug code."""
    user_id: int
    code: str
    error_message: Optional[str] = None
    expected_behavior: Optional[str] = None
    topic: Optional[str] = None


class DebugResponse(BaseModel):
    """Debugging agent response."""
    issue_summary: str
    root_cause: str
    corrected_code: str
    explanation: str
    best_practices: List[str]
    related_concepts: List[str] = []
