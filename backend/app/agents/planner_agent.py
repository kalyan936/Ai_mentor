"""
AI Mentor - Planner Agent.

Creates personalized learning roadmaps based on user profile and goals.
Adapts roadmaps based on performance data.
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import invoke_agent
from .prompts.planner import PLANNER_SYSTEM_PROMPT, PLANNER_RESCHEDULE_PROMPT

# Curriculum structure for all topics
CURRICULUM = {
    "python": {
        "name": "Python Programming",
        "subtopics": [
            "syntax", "data_types", "control_flow", "functions", "oop",
            "file_handling", "modules", "error_handling", "decorators",
            "iterators_generators", "real_projects"
        ]
    },
    "mysql": {
        "name": "MySQL & SQL",
        "subtopics": [
            "basic_queries", "filtering", "joins", "subqueries",
            "group_by", "window_functions", "ctes", "indexing",
            "optimization", "interview_sql"
        ]
    },
    "ml": {
        "name": "Machine Learning",
        "subtopics": [
            "supervised_learning", "regression", "classification",
            "clustering", "feature_engineering", "model_evaluation",
            "bias_variance", "overfitting", "pipelines", "business_cases"
        ]
    },
    "dl": {
        "name": "Deep Learning",
        "subtopics": [
            "neural_networks", "activation_functions", "backpropagation",
            "optimization", "cnn", "rnn", "lstm", "transformers_overview",
            "practical_projects"
        ]
    },
    "nlp": {
        "name": "Natural Language Processing",
        "subtopics": [
            "text_preprocessing", "tokenization", "stemming_lemmatization",
            "embeddings", "sentiment_analysis", "text_classification",
            "seq2seq", "transformers", "nlp_projects"
        ]
    },
    "genai": {
        "name": "Generative AI",
        "subtopics": [
            "llm_basics", "prompting", "embeddings", "vector_databases",
            "rag", "hallucination_handling", "evaluation",
            "fine_tuning_overview", "genai_app_design"
        ]
    },
    "agentic": {
        "name": "Agentic AI",
        "subtopics": [
            "agents_vs_workflows", "tools", "memory", "planning",
            "react", "task_decomposition", "multi_agent_systems",
            "langgraph_orchestration", "evaluation_observability",
            "production_concerns"
        ]
    }
}


async def generate_roadmap(
    topic: str,
    level: str = "beginner",
    goals: Optional[str] = None,
    daily_study_time: int = 30,
    prior_knowledge: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a personalized learning roadmap for a topic.

    Args:
        topic: The topic slug (python, mysql, ml, etc.)
        level: Current skill level
        goals: Learning goals
        daily_study_time: Minutes per day available
        prior_knowledge: What the user already knows

    Returns:
        Structured roadmap JSON
    """
    curriculum = CURRICULUM.get(topic, {})
    topic_name = curriculum.get("name", topic)
    subtopics = curriculum.get("subtopics", [])

    user_message = f"""Create a personalized learning roadmap for:
    
Topic: {topic_name}
Available Subtopics: {', '.join(subtopics)}
Current Level: {level}
Goals: {goals or 'Master the topic'}
Daily Study Time: {daily_study_time} minutes
Prior Knowledge: {prior_knowledge or 'None specified'}

Create modules that cover all subtopics logically, with proper prerequisites and time estimates.
Adjust depth based on the learner's level. Include milestone projects every 3-4 modules."""

    logger.info(f"Generating roadmap for {topic} at {level} level")
    result = await invoke_agent(PLANNER_SYSTEM_PROMPT, user_message, parse_json=True)

    # Validate and set defaults if needed
    if "modules" not in result:
        logger.warning("Roadmap generation failed, using fallback structure")
        result = _generate_fallback_roadmap(topic, subtopics, level)

    return result


async def reschedule_roadmap(
    current_roadmap: Dict[str, Any],
    performance_data: Dict[str, Any],
    weak_areas: List[str]
) -> Dict[str, Any]:
    """Reschedule roadmap based on performance."""
    user_message = f"""Current Roadmap: {current_roadmap}
    
Performance Data: {performance_data}
Weak Areas: {weak_areas}

Adjust the roadmap based on this performance data."""

    result = await invoke_agent(PLANNER_RESCHEDULE_PROMPT, user_message, parse_json=True)
    return result


def _generate_fallback_roadmap(topic: str, subtopics: list, level: str) -> Dict[str, Any]:
    """Generate a basic roadmap structure if AI generation fails."""
    modules = []
    for i, subtopic in enumerate(subtopics):
        difficulty = "beginner" if i < len(subtopics) // 3 else (
            "intermediate" if i < 2 * len(subtopics) // 3 else "advanced"
        )
        modules.append({
            "module_id": i + 1,
            "title": subtopic.replace("_", " ").title(),
            "description": f"Learn {subtopic.replace('_', ' ')} in {topic}",
            "subtopics": [subtopic],
            "estimated_hours": 2.0,
            "difficulty": difficulty,
            "prerequisites": [subtopics[i - 1]] if i > 0 else [],
            "status": "available" if i == 0 else "locked"
        })

    return {
        "modules": modules,
        "total_estimated_hours": len(modules) * 2.0,
        "recommended_pace": "1-2 modules per week",
        "milestones": []
    }


def get_curriculum() -> Dict[str, Any]:
    """Return the full curriculum structure."""
    return CURRICULUM
