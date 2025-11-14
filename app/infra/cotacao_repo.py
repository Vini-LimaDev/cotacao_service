from app.domain.models import Cotacao
from app.domain.portas import CotacaoProvider, CotacaoRepository
from app.infra.cache import CotacaoCache


class CotacaoRepositoryComCache(CotacaoRepository):
    def __init__(self, provider: CotacaoProvider, cache: CotacaoCache) -> None:
        self._provider = provider
        self._cache = cache

    async def obter_cotacao(self, moeda: str) -> Cotacao:
        moeda = moeda.upper()

        # 1. tenta cache
        entry = self._cache.get(moeda)
        if entry:
            return Cotacao(
                moeda=moeda,
                valor=entry.valor,
                atualizado_em=entry.atualizado_em,
                fonte="cache",
            )

        # 2. se não tiver ou expirou, chama provider externo
        valor = await self._provider.buscar_cotacao(moeda)
        entry = self._cache.set(moeda, valor)

        return Cotacao(
            moeda=moeda,
            valor=entry.valor,
            atualizado_em=entry.atualizado_em,
            fonte="api_externa",
        )
