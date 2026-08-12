"""
Agent OS Configuration
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # App
    APP_NAME: str = "Agent OS Control Plane"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./agent_os.db"
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6381/0"

    # Security
    # Secrets and bootstrap credentials must be supplied by the environment.
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # No account is created when these values are empty.
    ADMIN_EMAIL: str = ""
    ADMIN_PASSWORD: str = ""

    # CORS
    CORS_ORIGINS: List[str] = []

    # LLM Providers
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Memory
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
