# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.
    """
    cache_ttl_seconds: int = Field(default=60, description="TTL do cache em segundos")

    frankfurter_base_url: str = Field(
        default="https://api.frankfurter.app",
        description="Base URL da Frankfurter API",
    )
    frankfurter_timeout_seconds: float = Field(
        default=5.0,
        description="Timeout em segundos para chamadas HTTP externas",
    )

    # Crypto Provider
    crypto_provider: str = Field(
        default="binance",
        description="Provider de cotações cripto: 'binance', 'coingecko' ou 'brasilbitcoin'",
    )
    crypto_api_timeout: float = Field(
        default=10.0,
        description="Timeout para requisições de cripto em segundos",
    )

    # Database
    database_url: str = Field(
        default="postgresql://cotacao_user:cotacao_pass@localhost:5432/cotacao_db",
        description="URL de conexão com o banco de dados PostgreSQL",
    )

    # Auth / JWT
    secret_key: str = Field(
        default="sua-chave-secreta-super-segura-mude-em-producao",
        description="Chave secreta para geração de tokens JWT",
    )
    algorithm: str = Field(
        default="HS256",
        description="Algoritmo de criptografia para JWT",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Tempo de expiração do token de acesso em minutos",
    )

    class Config:
        env_prefix = "COTACAO_"


settings = Settings()
