from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # General
    app_title: str = "GPT-4o-mini Model API"
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
    fake_username: str = Field("test_user", description="Fake user login")
    fake_password: str = Field("1234", description="Fake user password")
    jwt_secret: str = Field("your-secret-key")
    require_auth: bool = True
    allowed_hosts: List[str] = ["*"]
    allowed_origins: List[str] = ["*"]

    # OpenAI
    openai_api_key: str = Field(default="default-openai-api-key")
    openai_model: str = "gpt-4o-mini"
    openai_max_retries: int = 3
    openai_retry_delay: float = 1.0

    # Rate limiting
    rate_limit_per_minute: int = 30

    model_config = SettingsConfigDict(env_file=".env")




@lru_cache()
def get_settings() -> Settings:
    return Settings()
