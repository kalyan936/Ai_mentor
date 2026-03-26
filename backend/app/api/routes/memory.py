"""
AI Mentor - Memory API Routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.memory import MemoryStoreRequest, MemoryRetrieveRequest, MemoryResponse
from ...agents.memory_agent import MemoryAgent
from typing import List

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.post("/store")
def store_memory(request: MemoryStoreRequest, db: Session = Depends(get_db)):
    """Store a new learning memory."""
    agent = MemoryAgent(db)
    record = agent.store_memory(
        user_id=request.user_id,
        memory_type=request.memory_type,
        content=request.content,
        topic=request.topic,
        importance=request.importance,
        metadata=request.metadata,
    )
    return {"id": record.id, "message": "Memory stored successfully"}


@router.post("/retrieve")
def retrieve_memories(request: MemoryRetrieveRequest, db: Session = Depends(get_db)):
    """Retrieve relevant memories for a user."""
    agent = MemoryAgent(db)
    records = agent.retrieve_memories(
        user_id=request.user_id,
        memory_type=request.memory_type,
        topic=request.topic,
        limit=request.limit,
    )
    return [
        MemoryResponse(
            id=r.id,
            memory_type=r.memory_type,
            topic=r.topic,
            content=r.content,
            importance=r.importance,
            created_at=r.created_at,
        )
        for r in records
    ]


@router.get("/context/{user_id}")
def get_user_context(user_id: int, topic: str = None, db: Session = Depends(get_db)):
    """Get aggregated learning context for a user."""
    agent = MemoryAgent(db)
    context = agent.get_user_context(user_id, topic)
    return {"context": context}

