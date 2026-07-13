from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # AI / LLM
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"
    LANGCHAIN_TRACING_V2: Optional[str] = "false"
    LANGSMITH_API_KEY: Optional[str] = None

    # Email
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@learning-analytics.com"

    # Encryption
    AES_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Global settings instance
settings = Settings()
