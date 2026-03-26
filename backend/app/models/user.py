"""
AI Mentor - User Model.

Stores user profile, learning preferences, and authentication data.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from ..db.database import Base


class User(Base):
    """User profile and learning preferences."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Simple auth for MVP
    goals = Column(Text, nullable=True)  # JSON string of learning goals
    learning_level = Column(String(50), default="beginner")  # beginner/intermediate/advanced
    preferred_topics = Column(Text, nullable=True)  # JSON array of topic slugs
    daily_study_time = Column(Integer, default=30)  # minutes per day
    preferred_style = Column(String(50), default="balanced")  # visual/conceptual/hands-on/balanced
    career_goal = Column(String(255), nullable=True)
    streak_days = Column(Integer, default=0)
    total_study_minutes = Column(Float, default=0.0)
    last_active = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
