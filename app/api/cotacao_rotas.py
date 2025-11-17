# app/api/cotacao_routes.py
from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.domain.models import Cotacao
from app.infra.cache import CotacaoCache
from app.infra.cotacao_repo import CotacaoRepositoryComCache
from app.infra.cliente_externo import HttpFrankfurterProvider

router = APIRouter(prefix="/cotacao", tags=["Cotação"])

_cache = CotacaoCache(ttl_seconds=settings.cache_ttl_seconds)
_provider = HttpFrankfurterProvider(
    base_url=settings.frankfurter_base_url,
    timeout=settings.frankfurter_timeout_seconds,
)
_repo = CotacaoRepositoryComCache(provider=_provider, cache=_cache)


def _validar_moeda(value: str) -> str:
    v = value.upper()
    if len(v) != 3 or not v.isalpha():
        raise HTTPException(
            status_code=400,
            detail=f"Moeda inválida: {value}. Use códigos de 3 letras, ex: USD, EUR, BRL.",
        )
    return v


@router.get("", response_model=Cotacao)
async def obter_cotacao(
    moeda_origem: str = Query(..., description="Moeda de origem, ex: USD"),
    moeda_destino: str = Query(..., description="Moeda de destino, ex: BRL"),
):
    origem = _validar_moeda(moeda_origem)
    destino = _validar_moeda(moeda_destino)

    try:
        cotacao = await _repo.obter_cotacao(origem, destino)
    except HTTPException:
        raise
    except Exception as exc:
        # aqui você pode logar o erro bonitinho
        raise HTTPException(status_code=502, detail=f"Erro ao consultar cotação externa: {exc}") from exc

    return cotacao
