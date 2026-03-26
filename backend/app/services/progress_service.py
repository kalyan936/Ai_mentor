"""
AI Mentor - Progress Service.

Business logic for tracking learning progress, mastery, and analytics.
"""

import json
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from loguru import logger
from ..models.progress import LessonProgress
from ..models.quiz import QuizResult
from ..models.code_submission import CodeSubmission
from ..models.user import User
from ..evaluation.scorer import (
    calculate_mastery_level,
    calculate_topic_mastery,
    calculate_next_action,
)


def update_progress(
    db: Session,
    user_id: int,
    topic: str,
    subtopic: str,
    status: str = "in_progress",
    score: Optional[float] = None,
    time_spent: Optional[float] = None,
) -> LessonProgress:
    """Update or create progress record for a subtopic."""
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.topic == topic,
        LessonProgress.subtopic == subtopic,
    ).first()

    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            topic=topic,
            subtopic=subtopic,
            status=status,
            attempts=0,
            score=0.0,
            time_spent_minutes=0.0,
        )
        db.add(progress)

    progress.status = status
    progress.attempts += 1
    progress.last_accessed = datetime.utcnow()

    if score is not None:
        current_score = progress.score or 0.0
        progress.score = max(current_score, score)  # Keep best score
        progress.mastery_level = calculate_mastery_level(progress.score, progress.attempts)

    if time_spent:
        current_time = progress.time_spent_minutes or 0.0
        progress.time_spent_minutes = current_time + time_spent

    db.commit()
    db.refresh(progress)
    return progress


def get_topic_progress(db: Session, user_id: int, topic: str) -> List[Dict[str, Any]]:
    """Get all progress records for a topic."""
    records = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.topic == topic,
    ).all()

    return [{
        "subtopic": r.subtopic,
        "status": r.status,
        "score": r.score,
        "attempts": r.attempts,
        "mastery_level": r.mastery_level,
        "time_spent_minutes": r.time_spent_minutes,
    } for r in records]


def get_dashboard_data(db: Session, user_id: int) -> Dict[str, Any]:
    """Build comprehensive dashboard data."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Get all progress data
    all_progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id
    ).all()

    # Group by topic
    topics_data = {}
    for p in all_progress:
        if p.topic not in topics_data:
            topics_data[p.topic] = []
        topics_data[p.topic].append({
            "subtopic": p.subtopic,
            "score": p.score,
            "status": p.status,
            "mastery_level": p.mastery_level,
        })

    # Calculate mastery per topic
    topics_mastery = []
    all_weak_areas = []
    for topic, subtopics in topics_data.items():
        mastery = calculate_topic_mastery(subtopics)
        topics_mastery.append({
            "topic": topic,
            "overall_mastery": mastery["overall_mastery"],
            "mastery_level": mastery["mastery_level"],
            "completed_subtopics": mastery["completed"],
            "total_subtopics": mastery["total"],
            "avg_score": mastery["overall_mastery"],
            "total_time_minutes": sum(p.time_spent_minutes for p in all_progress if p.topic == topic),
            "weak_areas": mastery["weak_areas"],
            "strong_areas": mastery["strong_areas"],
        })
        all_weak_areas.extend(mastery["weak_areas"])

    # Recent activity
    recent = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id
    ).order_by(LessonProgress.last_accessed.desc()).limit(5).all()

    recent_activity = [{
        "topic": r.topic,
        "subtopic": r.subtopic,
        "status": r.status,
        "score": r.score,
        "time": str(r.last_accessed) if r.last_accessed else None,
    } for r in recent]

    # Recommended next action
    progress_list = [{
        "topic": p.topic,
        "subtopic": p.subtopic,
        "status": p.status,
        "score": p.score,
    } for p in all_progress]

    next_action = calculate_next_action(progress_list, all_weak_areas)

    # Overall progress
    total_completed = len([p for p in all_progress if p.status == "completed"])
    total_items = len(all_progress) if all_progress else 1
    overall = (total_completed / total_items * 100) if total_items > 0 else 0

    return {
        "user_name": user.name,
        "streak_days": user.streak_days,
        "total_study_minutes": user.total_study_minutes,
        "topics_mastery": topics_mastery,
        "recent_activity": recent_activity,
        "recommended_next": next_action,
        "overall_progress": round(overall, 1),
        "achievements": _get_achievements(user, all_progress),
    }


def get_weak_areas(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Identify weak areas across all topics."""
    weak = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.score < 50,
        LessonProgress.attempts >= 1,
    ).order_by(LessonProgress.score.asc()).all()

    return [{
        "topic": w.topic,
        "subtopic": w.subtopic,
        "score": w.score,
        "attempts": w.attempts,
        "mastery_level": w.mastery_level,
        "recommendation": "Review this topic and take a quiz to strengthen understanding"
    } for w in weak]


def _get_achievements(user: User, progress: list) -> List[Dict[str, Any]]:
    """Calculate achievement badges."""
    achievements = []

    total_completed = len([p for p in progress if p.status == "completed"])
    if total_completed >= 1:
        achievements.append({"name": "First Step", "icon": "🎯", "description": "Completed your first lesson"})
    if total_completed >= 10:
        achievements.append({"name": "Dedicated Learner", "icon": "📚", "description": "Completed 10 lessons"})
    if total_completed >= 25:
        achievements.append({"name": "Knowledge Seeker", "icon": "🏆", "description": "Completed 25 lessons"})
    if user.streak_days >= 7:
        achievements.append({"name": "Week Warrior", "icon": "🔥", "description": "7-day learning streak"})

    expert_topics = len([p for p in progress if p.mastery_level == "expert"])
    if expert_topics >= 1:
        achievements.append({"name": "Mastery Achieved", "icon": "⭐", "description": "Expert level in a topic"})

    return achievements
