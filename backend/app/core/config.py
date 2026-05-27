from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AlgoLens API"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./algolens.db"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "development-only-change-this-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # AI Providers
    DEFAULT_AI_MODEL: str = "openai"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Encryption key for storing user API keys (generate with Fernet)
    AI_KEYS_ENCRYPTION_KEY: str = ""

    # Hugging Face
    HUGGINGFACE_DEFAULT_MODEL: str = "gpt2"

    # Code Execution
    CODE_EXECUTION_TIMEOUT_SECONDS: int = 5
    MAX_CODE_LENGTH: int = 10000
    MAX_INPUT_LENGTH: int = 5000

    # Supported Languages
    SUPPORTED_LANGUAGES: list[str] = ["python", "cpp", "java", "javascript", "go"]

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("SECRET_KEY must contain at least 32 characters")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
