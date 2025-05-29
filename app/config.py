from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # General
    app_title: str = "Language Model API"
    app_description: str = (
        "A REST API service for GPT-4o-mini language model operations"
    )
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Security
    api_key: str = Field(default="your-default-api-key", env="API_KEY")
    require_auth: bool = True
    allowed_hosts: List[str] = ["*"]
    allowed_origins: List[str] = ["*"]

    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # Rate limiting
    rate_limit_per_minute: int = 30

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
