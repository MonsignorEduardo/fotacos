"""Application settings using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str = Field(
        default="sqlite://fotacos.db",
        description="SQLite database URL",
    )

    upload_dir: Path = Field(
        default=Path("public/picts"),
        description="Directory for uploaded photos",
    )

    api_host: str = Field(default="127.0.0.1", description="API host address")
    api_port: int = Field(default=8000, description="API port")
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        description="CORS allowed origins",
    )

    thumbnail_size: int = Field(
        default=300,
        description="Thumbnail size (width and height in pixels)",
    )
    thumbnail_quality: int = Field(
        default=85,
        description="JPEG quality for thumbnails (1-100)",
    )

    debug: bool = Field(
        default=False,
        description="Debug mode for development",
    )

    def ensure_directories(self) -> None:
        """Create upload and thumbnail directories if they don't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
