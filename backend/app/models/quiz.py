"""
AI Mentor - Quiz Result Model.

Stores quiz attempts, answers, scores, and agent feedback.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base


class QuizResult(Base):
    """Records quiz attempts and results."""
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String(100), nullable=False)
    subtopic = Column(String(200), nullable=True)
    difficulty = Column(String(50), default="medium")  # easy/medium/hard
    questions_json = Column(Text, nullable=False)  # JSON array of questions
    answers_json = Column(Text, nullable=True)  # JSON array of user answers
    correct_answers_json = Column(Text, nullable=True)  # JSON array of correct answers
    score = Column(Float, default=0.0)  # Percentage score
    total_questions = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    feedback = Column(Text, nullable=True)  # AI-generated feedback
    weak_areas = Column(Text, nullable=True)  # JSON array of weak topics identified
    time_taken_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
