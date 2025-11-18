# app/api/cripto_rotas.py
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.infra.cliente_cripto_binance import HttpBinanceProvider
from app.infra.cliente_cripto import HttpCoinGeckoProvider


router = APIRouter(prefix="/cripto", tags=["Cripto"])


def _get_crypto_provider():
    """
    Factory para criar o provider de cripto baseado na configuração.
    Facilita a troca entre Binance, CoinGecko e Brasil Bitcoin.
    """
    provider_type = settings.crypto_provider.lower()
    timeout = settings.crypto_api_timeout
    
    if provider_type == "binance":
        return HttpBinanceProvider(timeout=timeout)
    elif provider_type == "coingecko":
        return HttpCoinGeckoProvider(timeout=timeout)
    # elif provider_type == "brasilbitcoin":
    #     return HttpBrasilBitcoinProvider(timeout=timeout)  # Implementar no futuro
    else:
        # Default: Binance
        return HttpBinanceProvider(timeout=timeout)


_provider = _get_crypto_provider()


class CriptoCotacao(BaseModel):
    """Modelo de resposta para cotação de criptomoeda."""
    simbolo: str
    nome: str
    moeda_destino: str
    taxa_cambio: float
    data_cotacao: datetime
    fonte: str  # Ex: "Binance API", "CoinGecko API", "Brasil Bitcoin API"


@router.get("/usdt-brl", response_model=CriptoCotacao)
async def obter_usdt_brl():
    """
    Obtém a cotação de USDT em BRL diretamente da Binance API.
    Sem cache - sempre atualizado em tempo real.
    """
    try:
        taxa = await _provider.buscar_usdt_brl()
        
        return CriptoCotacao(
            simbolo="USDT",
            nome="Tether",
            moeda_destino="BRL",
            taxa_cambio=taxa,
            data_cotacao=datetime.now(),
            fonte=f"{settings.crypto_provider.title()} API"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao consultar cotação USDT/BRL: {exc}"
        ) from exc


@router.get("/usdc-brl", response_model=CriptoCotacao)
async def obter_usdc_brl():
    """
    Obtém a cotação de USDC em BRL diretamente da Binance API.
    Sem cache - sempre atualizado em tempo real.
    """
    try:
        taxa = await _provider.buscar_usdc_brl()
        
        return CriptoCotacao(
            simbolo="USDC",
            nome="USD Coin",
            moeda_destino="BRL",
            taxa_cambio=taxa,
            data_cotacao=datetime.now(),
            fonte=f"{settings.crypto_provider.title()} API"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao consultar cotação USDC/BRL: {exc}"
        ) from exc


@router.get("/ambas-brl")
async def obter_ambas_brl():
    """
    Obtém as cotações de USDT e USDC em BRL de uma vez.
    Sem cache - sempre atualizado diretamente da Binance API.
    Requisições em paralelo para maior performance.
    """
    try:
        # Busca da API externa (em paralelo se o provider suportar)
        dados = await _provider.buscar_ambas_brl()
        
        fonte = f"{settings.crypto_provider.title()} API"
        
        return {
            "USDT": {
                "simbolo": "USDT",
                "nome": "Tether",
                "moeda_destino": "BRL",
                "taxa_cambio": dados.get("USDT", 0),
                "data_cotacao": datetime.now(),
                "fonte": fonte
            },
            "USDC": {
                "simbolo": "USDC",
                "nome": "USD Coin",
                "moeda_destino": "BRL",
                "taxa_cambio": dados.get("USDC", 0),
                "data_cotacao": datetime.now(),
                "fonte": fonte
            }
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao consultar cotações cripto: {exc}"
        ) from exc
