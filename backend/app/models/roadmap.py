"""
AI Mentor - Roadmap Model.

Stores AI-generated personalized learning roadmaps with progress tracking.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base


class Roadmap(Base):
    """Personalized learning roadmap for a user."""
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String(100), nullable=False)  # python, mysql, ml, dl, nlp, genai, agentic
    roadmap_json = Column(Text, nullable=False)  # Full roadmap structure as JSON
    current_stage = Column(Integer, default=0)  # Current module index
    total_stages = Column(Integer, default=0)
    next_recommended_task = Column(Text, nullable=True)  # JSON of next action
    status = Column(String(50), default="active")  # active/completed/paused
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
