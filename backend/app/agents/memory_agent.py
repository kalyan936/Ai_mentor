"""
AI Mentor - Memory Agent.

Manages long-term learning context. Stores and retrieves memories
about the learner's journey for personalized interactions.
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from sqlalchemy.orm import Session
from ..models.memory import MemoryRecord
from datetime import datetime


class MemoryAgent:
    """
    Agent responsible for storing and retrieving learning memories.
    Uses SQLite for structured storage and can be extended with FAISS for semantic search.
    """

    def __init__(self, db: Session):
        self.db = db

    def store_memory(
        self,
        user_id: int,
        memory_type: str,
        content: str,
        topic: Optional[str] = None,
        importance: int = 5,
        metadata: Optional[Dict] = None,
    ) -> MemoryRecord:
        """Store a new memory record."""
        record = MemoryRecord(
            user_id=user_id,
            memory_type=memory_type,
            topic=topic,
            content=content,
            importance=importance,
            metadata_json=str(metadata) if metadata else None,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        logger.info(f"Stored {memory_type} memory for user {user_id}")
        return record

    def retrieve_memories(
        self,
        user_id: int,
        memory_type: Optional[str] = None,
        topic: Optional[str] = None,
        limit: int = 10,
    ) -> List[MemoryRecord]:
        """Retrieve memories with optional filtering."""
        query = self.db.query(MemoryRecord).filter(MemoryRecord.user_id == user_id)

        if memory_type:
            query = query.filter(MemoryRecord.memory_type == memory_type)
        if topic:
            query = query.filter(MemoryRecord.topic == topic)

        records = query.order_by(
            MemoryRecord.importance.desc(),
            MemoryRecord.created_at.desc()
        ).limit(limit).all()

        return records

    def get_user_context(self, user_id: int, topic: Optional[str] = None) -> str:
        """
        Build a context string from user's memories for agent use.
        This provides personalization context to other agents.
        """
        memories = self.retrieve_memories(user_id, topic=topic, limit=20)

        if not memories:
            return "No prior learning history available."

        context_parts = []

        # Group by type
        weaknesses = [m for m in memories if m.memory_type == "weakness"]
        achievements = [m for m in memories if m.memory_type == "achievement"]
        mistakes = [m for m in memories if m.memory_type == "mistake"]
        preferences = [m for m in memories if m.memory_type == "preference"]

        if weaknesses:
            context_parts.append("Weak Areas: " + "; ".join([w.content for w in weaknesses[:5]]))
        if achievements:
            context_parts.append("Achievements: " + "; ".join([a.content for a in achievements[:5]]))
        if mistakes:
            context_parts.append("Common Mistakes: " + "; ".join([m.content for m in mistakes[:3]]))
        if preferences:
            context_parts.append("Preferences: " + "; ".join([p.content for p in preferences[:3]]))

        return " | ".join(context_parts) if context_parts else "Limited learning history available."

    def store_weakness(self, user_id: int, topic: str, content: str):
        """Convenience method to store a weakness."""
        return self.store_memory(user_id, "weakness", content, topic, importance=8)

    def store_achievement(self, user_id: int, topic: str, content: str):
        """Convenience method to store an achievement."""
        return self.store_memory(user_id, "achievement", content, topic, importance=7)

    def store_mistake(self, user_id: int, topic: str, content: str):
        """Convenience method to store a recurring mistake."""
        return self.store_memory(user_id, "mistake", content, topic, importance=6)
