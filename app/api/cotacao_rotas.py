# app/api/cotacao_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel

from app.core.config import settings
from app.domain.models import Cotacao
from app.infra.cache import CotacaoCache
from app.infra.cotacao_repo import CotacaoRepositoryComCache
from app.infra.cliente_externo import HttpFrankfurterProvider


class HistoricoItem(BaseModel):
    par: str
    moeda_origem: str
    moeda_destino: str
    taxa_cambio: float
    data_cotacao: str


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


@router.get("/historico", response_model=List[HistoricoItem])
async def obter_historico():
    """Retorna todas as cotações armazenadas em cache."""
    historico = []
    cache_entries = _cache.get_all()
    
    for key, entry in cache_entries.items():
        # O formato da chave é "ORIGEM->DESTINO"
        partes = key.split("->")
        if len(partes) == 2:
            origem, destino = partes
            historico.append(
                HistoricoItem(
                    par=key,
                    moeda_origem=origem,
                    moeda_destino=destino,
                    taxa_cambio=entry.valor,
                    data_cotacao=entry.atualizado_em.isoformat()
                )
            )
    
    # Ordena por data mais recente primeiro
    historico.sort(key=lambda x: x.data_cotacao, reverse=True)
    
    return historico
