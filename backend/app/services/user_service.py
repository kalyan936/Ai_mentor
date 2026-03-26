"""
AI Mentor - User Service.

Business logic for user management, onboarding, and profile operations.
"""

import json
from typing import Optional, List
from sqlalchemy.orm import Session
from loguru import logger
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user."""
    user = User(
        name=user_data.name,
        email=user_data.email,
        goals=user_data.goals,
        learning_level=user_data.learning_level,
        preferred_topics=json.dumps(user_data.preferred_topics) if user_data.preferred_topics else None,
        daily_study_time=user_data.daily_study_time,
        preferred_style=user_data.preferred_style,
        career_goal=user_data.career_goal,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Created user: {user.name} (ID: {user.id})")
    return user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, update_data: UserUpdate) -> Optional[User]:
    """Update user profile."""
    user = get_user(db, user_id)
    if not user:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)
    if "preferred_topics" in update_dict and update_dict["preferred_topics"]:
        update_dict["preferred_topics"] = json.dumps(update_dict["preferred_topics"])

    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def login_or_create(db: Session, email: str, name: str = "Learner") -> User:
    """Simple login: find existing user or create new one."""
    user = get_user_by_email(db, email)
    if user:
        return user
    return create_user(db, UserCreate(name=name, email=email))
