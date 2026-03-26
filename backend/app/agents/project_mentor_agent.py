"""
AI Mentor - Project Mentor Agent.

Recommends projects, guides implementation, and reviews submissions.
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import invoke_agent
from .prompts.project_mentor import PROJECT_MENTOR_SUGGEST_PROMPT, PROJECT_MENTOR_REVIEW_PROMPT


async def suggest_project(
    topic: str,
    level: str = "beginner",
    completed_topics: Optional[List[str]] = None,
    weak_areas: Optional[List[str]] = None,
    career_goal: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a project suggestion tailored to the learner."""
    user_message = PROJECT_MENTOR_SUGGEST_PROMPT.format(
        topic=topic,
        level=level,
        completed_topics=", ".join(completed_topics or []),
        weak_areas=", ".join(weak_areas or []),
        career_goal=career_goal or "General mastery",
    )

    logger.info(f"Suggesting project for {topic} at {level} level")
    result = await invoke_agent(
        "You are an expert project mentor for learning.",
        user_message,
        parse_json=True
    )

    # Ensure required fields
    result.setdefault("title", f"{topic.title()} Practice Project")
    result.setdefault("topic", topic)
    result.setdefault("difficulty", level)
    result.setdefault("requirements", [])
    result.setdefault("learning_outcomes", [])
    result.setdefault("estimated_hours", 5.0)
    result.setdefault("skills_practiced", [])

    return result


async def review_project(
    title: str,
    topic: str,
    description: str,
    code: Optional[str] = None,
    requirements: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Review a submitted project."""
    user_message = PROJECT_MENTOR_REVIEW_PROMPT.format(
        title=title,
        topic=topic,
        description=description,
        code=code or "No code submitted",
        requirements=", ".join(requirements or []),
    )

    result = await invoke_agent(
        "You are an expert project reviewer and mentor.",
        user_message,
        parse_json=True
    )

    result.setdefault("score", 0)
    result.setdefault("feedback", "Review could not be completed")
    result.setdefault("strengths", [])
    result.setdefault("improvements", [])
    result.setdefault("skills_demonstrated", [])
    result.setdefault("next_steps", [])

    return result
