"""
AI Mentor - Roadmap API Routes.

Handles roadmap generation, retrieval, and progression.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...schemas.roadmap import RoadmapGenerateRequest, RoadmapResponse
from ...services.roadmap_service import create_roadmap, get_roadmap, get_all_roadmaps, advance_stage
from ...agents.planner_agent import get_curriculum

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


@router.post("/generate")
async def generate_roadmap(request: RoadmapGenerateRequest, db: Session = Depends(get_db)):
    """Generate a personalized learning roadmap using the Planner Agent."""
    curriculum = get_curriculum()
    if request.topic not in curriculum:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid topic. Choose from: {', '.join(curriculum.keys())}"
        )

    roadmap = await create_roadmap(
        db=db,
        user_id=request.user_id,
        topic=request.topic,
        level=request.current_level,
        goals=request.goals,
        daily_study_time=request.daily_study_time,
    )
    return roadmap


@router.get("/curriculum/all")
def get_all_curriculum():
    """Get the full curriculum structure."""
    return get_curriculum()


@router.get("/{user_id}/{topic}")
def get_user_roadmap(user_id: int, topic: str, db: Session = Depends(get_db)):
    """Get the active roadmap for a user and topic."""
    roadmap = get_roadmap(db, user_id, topic)
    if not roadmap:
        raise HTTPException(status_code=404, detail="No active roadmap found for this topic")
    return roadmap


@router.get("/{user_id}")
def get_user_roadmaps(user_id: int, db: Session = Depends(get_db)):
    """Get all roadmaps for a user."""
    return get_all_roadmaps(db, user_id)


@router.post("/advance/{roadmap_id}")
def advance_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    """Advance to the next stage in a roadmap."""
    result = advance_stage(db, roadmap_id)
    if not result:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return result

