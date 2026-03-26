"""
AI Mentor - Core Configuration Module.

Manages application settings using pydantic-settings with .env file support.
All configuration is centralized here for clean environment management.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    app_name: str = "AI Mentor"
    app_version: str = "1.0.0"
    debug: bool = True
    log_level: str = "INFO"

    # LLM Provider
    llm_provider: str = "groq"
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # LLM Model
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # Database
    database_url: str = "sqlite:///./ai_mentor.db"

    # Vector Store
    vector_store_path: str = "./data/vector_store"

    # Code Execution
    code_execution_timeout: int = 10
    code_execution_max_memory_mb: int = 256

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 8501
    backend_url: str = "http://localhost:8000"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()
