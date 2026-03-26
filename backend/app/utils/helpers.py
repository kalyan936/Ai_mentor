"""Utility helpers."""


def format_topic_name(slug: str) -> str:
    """Convert topic slug to display name."""
    names = {
        "python": "Python Programming",
        "mysql": "MySQL & SQL",
        "ml": "Machine Learning",
        "dl": "Deep Learning",
        "nlp": "Natural Language Processing",
        "genai": "Generative AI",
        "agentic": "Agentic AI",
    }
    return names.get(slug, slug.replace("_", " ").title())


def format_subtopic_name(slug: str) -> str:
    """Convert subtopic slug to display name."""
    return slug.replace("_", " ").title()


TOPIC_ICONS = {
    "python": "🐍",
    "mysql": "🗄️",
    "ml": "🤖",
    "dl": "🧠",
    "nlp": "💬",
    "genai": "✨",
    "agentic": "🤝",
}


MASTERY_COLORS = {
    "novice": "#6B7280",
    "beginner": "#3B82F6",
    "intermediate": "#F59E0B",
    "proficient": "#10B981",
    "expert": "#8B5CF6",
}
