from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.domain.models import Cotacao
from app.infra.cache import CotacaoCache
from app.infra.cotacao_repo import CotacaoRepositoryComCache
from app.infra.cliente_externo import FakeCotacaoProvider

router = APIRouter(prefix="/cotacao", tags=["Cotação"])

# “singletons” simples só pra esse serviço
_cache = CotacaoCache(ttl_seconds=settings.cache_ttl_seconds)
_provider = FakeCotacaoProvider()
_repo = CotacaoRepositoryComCache(provider=_provider, cache=_cache)


@router.get("", response_model=Cotacao)
async def obter_cotacao(
    moeda: str = Query(..., min_length=3, max_length=3, description="Código da moeda, ex: USD"),
):
    moeda_normalizada = moeda.upper()

    if not moeda_normalizada.isalpha():
        raise HTTPException(status_code=400, detail="Moeda deve conter apenas letras (ex: USD, EUR).")

    try:
        cotacao = await _repo.obter_cotacao(moeda_normalizada)
    except Exception as exc:  # em algo real, logaria isso bonitinho
        raise HTTPException(status_code=502, detail=f"Erro ao obter cotação: {exc}") from exc

    return cotacao
