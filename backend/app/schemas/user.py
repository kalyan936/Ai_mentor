"""
AI Mentor - User Schemas.

Pydantic models for user-related API request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=255)
    password: Optional[str] = Field(None, min_length=6)
    goals: Optional[str] = None
    learning_level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    preferred_topics: Optional[List[str]] = None
    daily_study_time: int = Field(default=30, ge=10, le=480)
    preferred_style: str = Field(default="balanced")
    career_goal: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = None
    goals: Optional[str] = None
    learning_level: Optional[str] = None
    preferred_topics: Optional[List[str]] = None
    daily_study_time: Optional[int] = None
    preferred_style: Optional[str] = None
    career_goal: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user API response."""
    id: int
    name: str
    email: str
    goals: Optional[str] = None
    learning_level: str
    preferred_topics: Optional[List[str]] = None
    daily_study_time: int
    preferred_style: str
    career_goal: Optional[str] = None
    streak_days: int = 0
    total_study_minutes: float = 0.0
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class OnboardingRequest(BaseModel):
    """Schema for initial onboarding assessment."""
    user_id: int
    selected_topics: List[str] = Field(..., min_length=1)
    current_level: str = Field(default="beginner")
    prior_knowledge: Optional[str] = None
    goals: str
    daily_study_time: int = Field(default=30, ge=10, le=480)
    preferred_style: str = Field(default="balanced")
    career_goal: Optional[str] = None


class LoginRequest(BaseModel):
    """Simple login schema for MVP."""
    email: str
    password: Optional[str] = None
