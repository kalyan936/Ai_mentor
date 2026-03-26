"""
AI Mentor - User API Routes.

Handles user registration, login, onboarding, and profile management.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.user import UserCreate, UserUpdate, UserResponse, OnboardingRequest, LoginRequest
from ...services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing = user_service.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = user_service.create_user(db, user_data)
    response = UserResponse.model_validate(user)
    if user.preferred_topics:
        response.preferred_topics = json.loads(user.preferred_topics)
    return response


@router.post("/login", response_model=UserResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Simple login - find or create user by email."""
    user = user_service.login_or_create(db, login_data.email)
    response = UserResponse.model_validate(user)
    if user.preferred_topics:
        response.preferred_topics = json.loads(user.preferred_topics)
    return response


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile."""
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    response = UserResponse.model_validate(user)
    if user.preferred_topics:
        response.preferred_topics = json.loads(user.preferred_topics)
    return response


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    """Update user profile."""
    user = user_service.update_user(db, user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    response = UserResponse.model_validate(user)
    if user.preferred_topics:
        response.preferred_topics = json.loads(user.preferred_topics)
    return response


@router.post("/onboard")
async def onboard_user(onboarding: OnboardingRequest, db: Session = Depends(get_db)):
    """Complete user onboarding with topic selection and preferences."""
    user = user_service.get_user(db, onboarding.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = UserUpdate(
        goals=onboarding.goals,
        learning_level=onboarding.current_level,
        preferred_topics=onboarding.selected_topics,
        daily_study_time=onboarding.daily_study_time,
        preferred_style=onboarding.preferred_style,
        career_goal=onboarding.career_goal,
    )
    user_service.update_user(db, onboarding.user_id, update_data)

    return {
        "message": "Onboarding completed successfully",
        "user_id": onboarding.user_id,
        "selected_topics": onboarding.selected_topics,
        "next_step": "Generate roadmaps for selected topics"
    }

