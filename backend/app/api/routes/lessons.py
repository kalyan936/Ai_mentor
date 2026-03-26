"""
AI Mentor - Lesson & Tutor API Routes.

Handles lesson delivery and AI tutor chat interactions.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.project import TutorChatRequest, TutorChatResponse
from ...agents.tutor_agent import teach_lesson, chat_with_tutor
from ...agents.memory_agent import MemoryAgent
from ...services.progress_service import update_progress

router = APIRouter(prefix="/lessons", tags=["Lessons & Tutor"])


@router.post("/start")
async def start_lesson(
    user_id: int,
    topic: str,
    subtopic: str,
    level: str = "beginner",
    db: Session = Depends(get_db),
):
    """Start a lesson on a specific topic/subtopic."""
    # Get prior context from memory
    memory_agent = MemoryAgent(db)
    context = memory_agent.get_user_context(user_id, topic)

    # Generate lesson
    lesson_content = await teach_lesson(
        topic=topic,
        subtopic=subtopic,
        level=level,
        background=context,
    )

    # Update progress
    update_progress(db, user_id, topic, subtopic, status="in_progress")

    return {
        "topic": topic,
        "subtopic": subtopic,
        "content": lesson_content,
        "level": level,
    }


@router.post("/chat", response_model=TutorChatResponse)
async def tutor_chat(request: TutorChatRequest, db: Session = Depends(get_db)):
    """Chat with the AI tutor agent."""
    # Get prior context
    memory_agent = MemoryAgent(db)
    context = memory_agent.get_user_context(request.user_id, request.topic)

    response = await chat_with_tutor(
        message=request.message,
        topic=request.topic,
        subtopic=request.subtopic,
        history=context,
    )

    return TutorChatResponse(**response)


@router.post("/complete")
async def complete_lesson(
    user_id: int,
    topic: str,
    subtopic: str,
    time_spent_minutes: float = 0,
    db: Session = Depends(get_db),
):
    """Mark a lesson as completed."""
    progress = update_progress(
        db, user_id, topic, subtopic,
        status="completed",
        score=100.0,
        time_spent=time_spent_minutes,
    )

    # Store achievement in memory
    memory_agent = MemoryAgent(db)
    memory_agent.store_achievement(
        user_id, topic,
        f"Completed lesson: {subtopic.replace('_', ' ').title()}"
    )

    return {
        "message": "Lesson completed!",
        "mastery_level": progress.mastery_level,
        "topic": topic,
        "subtopic": subtopic,
    }

