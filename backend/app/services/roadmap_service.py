"""
AI Mentor - Roadmap Service.

Business logic for roadmap generation, storage, and retrieval.
"""

import json
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from loguru import logger
from ..models.roadmap import Roadmap
from ..agents.planner_agent import generate_roadmap as ai_generate_roadmap


async def create_roadmap(
    db: Session,
    user_id: int,
    topic: str,
    level: str = "beginner",
    goals: Optional[str] = None,
    daily_study_time: int = 30,
) -> Dict[str, Any]:
    """Generate and store a personalized roadmap."""
    # Generate roadmap via AI agent
    roadmap_data = await ai_generate_roadmap(
        topic=topic,
        level=level,
        goals=goals,
        daily_study_time=daily_study_time,
    )

    modules = roadmap_data.get("modules", [])

    # Store in database
    roadmap = Roadmap(
        user_id=user_id,
        topic=topic,
        roadmap_json=json.dumps(roadmap_data),
        current_stage=0,
        total_stages=len(modules),
        status="active",
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)

    logger.info(f"Created roadmap for user {user_id}, topic: {topic}, modules: {len(modules)}")

    return {
        "id": roadmap.id,
        "user_id": user_id,
        "topic": topic,
        "modules": modules,
        "current_stage": 0,
        "total_stages": len(modules),
        "next_recommended_task": _get_next_task(modules),
        "status": "active",
        "created_at": str(roadmap.created_at),
    }


def get_roadmap(db: Session, user_id: int, topic: str) -> Optional[Dict[str, Any]]:
    """Get the active roadmap for a user and topic."""
    roadmap = db.query(Roadmap).filter(
        Roadmap.user_id == user_id,
        Roadmap.topic == topic,
        Roadmap.status == "active"
    ).order_by(Roadmap.created_at.desc()).first()

    if not roadmap:
        return None

    roadmap_data = json.loads(roadmap.roadmap_json)

    return {
        "id": roadmap.id,
        "user_id": roadmap.user_id,
        "topic": roadmap.topic,
        "modules": roadmap_data.get("modules", []),
        "current_stage": roadmap.current_stage,
        "total_stages": roadmap.total_stages,
        "next_recommended_task": json.loads(roadmap.next_recommended_task) if roadmap.next_recommended_task else None,
        "status": roadmap.status,
        "created_at": str(roadmap.created_at),
    }


def get_all_roadmaps(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Get all roadmaps for a user."""
    roadmaps = db.query(Roadmap).filter(
        Roadmap.user_id == user_id
    ).order_by(Roadmap.created_at.desc()).all()

    result = []
    for roadmap in roadmaps:
        data = json.loads(roadmap.roadmap_json)
        result.append({
            "id": roadmap.id,
            "topic": roadmap.topic,
            "current_stage": roadmap.current_stage,
            "total_stages": roadmap.total_stages,
            "status": roadmap.status,
            "modules_count": len(data.get("modules", [])),
        })
    return result


def advance_stage(db: Session, roadmap_id: int) -> Optional[Dict[str, Any]]:
    """Advance to the next stage in the roadmap."""
    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        return None

    if roadmap.current_stage < roadmap.total_stages - 1:
        roadmap.current_stage += 1

        # Unlock next module
        roadmap_data = json.loads(roadmap.roadmap_json)
        modules = roadmap_data.get("modules", [])
        if roadmap.current_stage < len(modules):
            modules[roadmap.current_stage]["status"] = "available"
            roadmap.roadmap_json = json.dumps(roadmap_data)

        roadmap.next_recommended_task = json.dumps(_get_next_task(modules, roadmap.current_stage))
        db.commit()
        return {"current_stage": roadmap.current_stage, "status": "advanced"}
    else:
        roadmap.status = "completed"
        db.commit()
        return {"current_stage": roadmap.current_stage, "status": "completed"}


def _get_next_task(modules: list, current_idx: int = 0) -> Dict[str, Any]:
    """Get the next recommended task from modules."""
    if current_idx < len(modules):
        module = modules[current_idx]
        return {
            "type": "lesson",
            "module_id": module.get("module_id", current_idx + 1),
            "title": module.get("title", ""),
            "subtopics": module.get("subtopics", []),
        }
    return {"type": "completed", "title": "All modules completed!"}
