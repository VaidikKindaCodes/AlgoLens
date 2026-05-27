from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AlgoLens API"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./algolens.db"
    SECRET_KEY: str = "development-only-change-this-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

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
