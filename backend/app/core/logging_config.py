"""
AI Mentor - Logging Configuration.

Uses loguru for structured, colorful logging with rotation and formatting.
"""

import sys
from loguru import logger
from .config import get_settings


def setup_logging():
    """Configure application-wide logging."""
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Console handler with color
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # File handler with rotation
    logger.add(
        "logs/ai_mentor.log",
        rotation="10 MB",
        retention="7 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
    )

    logger.info(f"Logging configured at level: {settings.log_level}")
    return logger
