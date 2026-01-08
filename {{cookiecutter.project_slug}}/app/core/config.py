"""
Application configuration using pydantic-settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "{{cookiecutter.project_name}}"
    APP_VERSION: str = "{{cookiecutter.version}}"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]  # Дефолт для разработки
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./{{cookiecutter.project_slug}}.db"
    
    # Security
    SECRET_KEY: str = "change-this-to-random-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Singleton instance
settings = Settings()
