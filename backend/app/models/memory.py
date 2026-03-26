"""
AI Mentor - Memory Record Model.

Stores long-term learning memories for personalization, including
weak areas, mistakes, achievements, and learning patterns.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base


class MemoryRecord(Base):
    """Long-term learning memory for AI personalization."""
    __tablename__ = "memory_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    memory_type = Column(String(50), nullable=False)
    # Types: weakness, mistake, achievement, preference, note, milestone, feedback
    topic = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)  # The memory content
    importance = Column(Integer, default=5)  # 1-10 importance score
    embedding_id = Column(String(255), nullable=True)  # Reference to FAISS vector
    metadata_json = Column(Text, nullable=True)  # Additional metadata
    created_at = Column(DateTime, server_default=func.now())
