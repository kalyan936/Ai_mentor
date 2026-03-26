"""
AI Mentor - Project Submission Model.

Stores project-based learning submissions, reviews, and feedback.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base


class ProjectSubmission(Base):
    """Records project submissions and mentor feedback."""
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_title = Column(String(255), nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="intermediate")
    description = Column(Text, nullable=False)
    requirements_json = Column(Text, nullable=True)  # JSON array of project requirements
    submitted_code = Column(Text, nullable=True)
    repo_link = Column(String(500), nullable=True)
    status = Column(String(50), default="suggested")  # suggested/in_progress/submitted/reviewed
    feedback = Column(Text, nullable=True)  # Mentor agent feedback
    score = Column(Float, nullable=True)  # 0-100 score
    skills_demonstrated = Column(Text, nullable=True)  # JSON array
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
