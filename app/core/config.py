from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    cache_ttl_seconds: int = Field(default=60, description="Tempo de vida do cache em segundos")

    class Config:
        env_prefix = "COTACAO_"
        
settings = Settings()