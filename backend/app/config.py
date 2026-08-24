"""
Agent OS Configuration
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # Temporal is the only durable workflow path in D0.
    TEMPORAL_ADDRESS: str = "localhost:7233"
    TEMPORAL_NAMESPACE: str = "default"
    TEMPORAL_TASK_QUEUE: str = "agent-os-d0"

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

    @property
    def cors_allow_credentials(self) -> bool:
        """Disable credentials when any origin is a wildcard."""
        return "*" not in self.CORS_ORIGINS

    # LLM Providers
    OPENAI_API_KEY: str = ""
    OPENAI_EXECUTION_ENABLED: bool = False
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TIMEOUT_SECONDS: float = 30.0
    D2_MAX_INPUT_CHARS: int = 12000
    D2_MAX_OUTPUT_TOKENS: int = 256
    D2_RUN_BUDGET_USD: float | None = None
    ANTHROPIC_API_KEY: str = ""

    # Memory
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
