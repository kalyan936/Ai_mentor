"""
AI Mentor - Code Submission Model.

Stores coding challenges, user submissions, execution results, and agent feedback.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base


class CodeSubmission(Base):
    """Records coding challenge submissions and evaluations."""
    __tablename__ = "code_submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String(100), nullable=False)
    subtopic = Column(String(200), nullable=True)
    difficulty = Column(String(50), default="medium")
    prompt = Column(Text, nullable=False)  # The coding challenge description
    submitted_code = Column(Text, nullable=False)
    language = Column(String(50), default="python")
    execution_output = Column(Text, nullable=True)
    execution_status = Column(String(50), nullable=True)  # success/error/timeout
    errors = Column(Text, nullable=True)
    agent_feedback = Column(Text, nullable=True)  # Detailed agent review
    score = Column(Float, default=0.0)  # 0-100
    suggestions = Column(Text, nullable=True)  # JSON array of improvement suggestions
    created_at = Column(DateTime, server_default=func.now())
