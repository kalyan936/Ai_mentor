"""
AI Mentor - Lesson Progress Model.

Tracks per-topic, per-subtopic progress with mastery levels and attempt counts.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base


class LessonProgress(Base):
    """Tracks learning progress for each topic and subtopic."""
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String(100), nullable=False, index=True)
    subtopic = Column(String(200), nullable=False)
    status = Column(String(50), default="not_started")  # not_started/in_progress/completed/needs_review
    score = Column(Float, default=0.0)  # 0-100
    attempts = Column(Integer, default=0)
    mastery_level = Column(String(50), default="novice")  # novice/beginner/intermediate/proficient/expert
    time_spent_minutes = Column(Float, default=0.0)
    last_accessed = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)  # AI-generated notes about performance
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
