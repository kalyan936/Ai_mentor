"""
AI Mentor - Memory Schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MemoryStoreRequest(BaseModel):
    """Store a new memory."""
    user_id: int
    memory_type: str  # weakness/mistake/achievement/preference/note/milestone
    topic: Optional[str] = None
    content: str
    importance: int = Field(default=5, ge=1, le=10)
    metadata: Optional[Dict[str, Any]] = None


class MemoryRetrieveRequest(BaseModel):
    """Retrieve relevant memories."""
    user_id: int
    query: str
    memory_type: Optional[str] = None
    topic: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)


class MemoryResponse(BaseModel):
    """A memory record response."""
    id: int
    memory_type: str
    topic: Optional[str] = None
    content: str
    importance: int
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
