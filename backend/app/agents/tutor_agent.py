"""
AI Mentor - Tutor Agent.

Teaches topics adaptively, answers questions, and provides personalized lessons.
Adapts explanation style based on learner level and preferences.
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import invoke_agent
from .prompts.tutor import TUTOR_SYSTEM_PROMPT, TUTOR_LESSON_PROMPT, TUTOR_CHAT_PROMPT


async def teach_lesson(
    topic: str,
    subtopic: str,
    level: str = "beginner",
    style: str = "balanced",
    background: Optional[str] = None
) -> str:
    """
    Generate a comprehensive lesson on a topic/subtopic.

    Returns:
        Formatted lesson content string
    """
    system_prompt = TUTOR_SYSTEM_PROMPT.format(
        topic=topic,
        level=level,
        subtopic=subtopic,
        style=style,
        context="lesson"
    )

    user_message = TUTOR_LESSON_PROMPT.format(
        topic=topic,
        subtopic=subtopic,
        level=level,
        background=background or "No specific background provided"
    )

    logger.info(f"Generating lesson: {topic}/{subtopic} at {level} level")
    response = await invoke_agent(system_prompt, user_message, parse_json=False)
    return response


async def chat_with_tutor(
    message: str,
    topic: Optional[str] = None,
    subtopic: Optional[str] = None,
    level: str = "beginner",
    style: str = "balanced",
    history: Optional[str] = None
) -> Dict[str, Any]:
    """
    Handle a chat interaction with the tutor agent.

    Returns:
        Dict with response, suggested followups, and related topics
    """
    system_prompt = TUTOR_SYSTEM_PROMPT.format(
        topic=topic or "general",
        level=level,
        subtopic=subtopic or "general",
        style=style,
        context="chat"
    )

    user_message = TUTOR_CHAT_PROMPT.format(
        question=message,
        topic=topic or "not specified",
        subtopic=subtopic or "not specified",
        level=level,
        history=history or "No recent history"
    )

    response_text = await invoke_agent(system_prompt, user_message, parse_json=False)

    return {
        "response": response_text,
        "suggested_followup": _generate_followups(topic, subtopic),
        "related_topics": _get_related_topics(topic, subtopic),
    }


def _generate_followups(topic: Optional[str], subtopic: Optional[str]) -> List[str]:
    """Generate contextual follow-up question suggestions."""
    followups = [
        f"Can you give me a practical example?",
        f"What are common mistakes to avoid?",
        f"How is this used in real projects?",
    ]
    if topic:
        followups.append(f"What should I learn next in {topic}?")
    if subtopic:
        followups.append(f"Can you quiz me on {subtopic}?")
    return followups[:4]


def _get_related_topics(topic: Optional[str], subtopic: Optional[str]) -> List[str]:
    """Get related topics for exploration."""
    topic_relations = {
        "python": ["data_types", "functions", "oop", "error_handling"],
        "mysql": ["joins", "subqueries", "optimization"],
        "ml": ["feature_engineering", "model_evaluation", "pipelines"],
        "dl": ["neural_networks", "cnn", "transformers_overview"],
        "nlp": ["tokenization", "embeddings", "transformers"],
        "genai": ["prompting", "rag", "vector_databases"],
        "agentic": ["tools", "memory", "multi_agent_systems"],
    }
    return topic_relations.get(topic, [])[:3]
