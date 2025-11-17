# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    cache_ttl_seconds: int = Field(default=60, description="TTL do cache em segundos")

    frankfurter_base_url: str = Field(
        default="https://api.frankfurter.app",
        description="Base URL da Frankfurter API",
    )
    frankfurter_timeout_seconds: float = Field(
        default=5.0,
        description="Timeout em segundos para chamadas HTTP externas",
    )

    class Config:
        env_prefix = "COTACAO_"


settings = Settings()
