"""
AI Mentor - Scoring Engine.

Provides scoring heuristics for mastery calculation, topic progression,
and adaptive difficulty adjustment.
"""

from typing import Dict, Any, List, Optional
from loguru import logger


def calculate_mastery_level(score: float, attempts: int) -> str:
    """
    Calculate mastery level based on score and attempt history.

    Mastery Levels:
        novice    : < 30% or first attempt
        beginner  : 30-50%
        intermediate: 50-70%
        proficient: 70-90%
        expert    : > 90% with low attempts
    """
    if attempts == 0:
        return "novice"

    if score >= 90 and attempts <= 2:
        return "expert"
    elif score >= 70:
        return "proficient"
    elif score >= 50:
        return "intermediate"
    elif score >= 30:
        return "beginner"
    else:
        return "novice"


def calculate_topic_mastery(subtopic_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate overall topic mastery from subtopic performance.

    Returns:
        Dict with overall_mastery, level, and weak/strong areas
    """
    if not subtopic_scores:
        return {
            "overall_mastery": 0,
            "mastery_level": "novice",
            "weak_areas": [],
            "strong_areas": []
        }

    scores = [s.get("score", 0) for s in subtopic_scores]
    avg_score = sum(scores) / len(scores)

    weak_areas = [
        s.get("subtopic", "unknown")
        for s in subtopic_scores
        if s.get("score", 0) < 50
    ]

    strong_areas = [
        s.get("subtopic", "unknown")
        for s in subtopic_scores
        if s.get("score", 0) >= 70
    ]

    return {
        "overall_mastery": round(avg_score, 1),
        "mastery_level": calculate_mastery_level(avg_score, len(subtopic_scores)),
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "completed": len([s for s in subtopic_scores if s.get("status") == "completed"]),
        "total": len(subtopic_scores),
    }


def recommend_difficulty(current_mastery: float, recent_scores: List[float]) -> str:
    """Recommend difficulty level based on performance."""
    if not recent_scores:
        return "easy"

    avg_recent = sum(recent_scores[-5:]) / len(recent_scores[-5:])

    if avg_recent >= 85:
        return "hard"
    elif avg_recent >= 60:
        return "medium"
    else:
        return "easy"


def should_add_revision(
    topic: str,
    subtopic: str,
    score: float,
    attempts: int,
    mistakes_count: int = 0
) -> bool:
    """Determine if a revision session should be added."""
    if score < 50 and attempts >= 2:
        return True
    if mistakes_count >= 3:
        return True
    if score < 30:
        return True
    return False


def calculate_next_action(
    progress_data: List[Dict],
    weak_areas: List[str],
    current_streak: int = 0
) -> Dict[str, Any]:
    """
    Determine the best next learning action using simple heuristics.

    Priority:
    1. Revision needed for weak areas → quiz/lesson on weak topic
    2. In-progress topics → continue current lesson
    3. New available topics → start next lesson
    4. All complete → suggest project or advanced challenge
    """
    # Check for weak areas needing revision
    if weak_areas:
        return {
            "task_type": "revision",
            "topic": weak_areas[0],
            "subtopic": weak_areas[0],
            "title": f"Review: {weak_areas[0].replace('_', ' ').title()}",
            "description": "Let's strengthen your understanding of this topic",
            "estimated_minutes": 15,
            "priority": "high",
            "reason": "This topic needs more practice based on your recent scores"
        }

    # Find in-progress or next available topics
    in_progress = [p for p in progress_data if p.get("status") == "in_progress"]
    if in_progress:
        topic = in_progress[0]
        return {
            "task_type": "lesson",
            "topic": topic.get("topic", ""),
            "subtopic": topic.get("subtopic", ""),
            "title": f"Continue: {topic.get('subtopic', '').replace('_', ' ').title()}",
            "description": "Pick up where you left off",
            "estimated_minutes": 20,
            "priority": "medium",
            "reason": "You have an active lesson to complete"
        }

    not_started = [p for p in progress_data if p.get("status") == "not_started"]
    if not_started:
        topic = not_started[0]
        return {
            "task_type": "lesson",
            "topic": topic.get("topic", ""),
            "subtopic": topic.get("subtopic", ""),
            "title": f"Start: {topic.get('subtopic', '').replace('_', ' ').title()}",
            "description": "Ready to learn something new!",
            "estimated_minutes": 25,
            "priority": "medium",
            "reason": "This is the next topic in your roadmap"
        }

    return {
        "task_type": "project",
        "topic": "general",
        "subtopic": "capstone",
        "title": "Build a Project!",
        "description": "You've covered the fundamentals. Time to apply your knowledge!",
        "estimated_minutes": 60,
        "priority": "low",
        "reason": "All current topics are completed"
    }
