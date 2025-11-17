# app/infra/cotacao_repo.py
from app.domain.models import Cotacao
from app.domain.portas import CotacaoProvider, CotacaoRepository
from app.infra.cache import CotacaoCache


class CotacaoRepositoryComCache(CotacaoRepository):
    def __init__(self, provider: CotacaoProvider, cache: CotacaoCache) -> None:
        self._provider = provider
        self._cache = cache

    async def obter_cotacao(self, moeda_origem: str, moeda_destino: str) -> Cotacao:
        """
        Obtém a cotação entre duas moedas.
        Consulta o cache antes de fazer uma chamada externa.
        """
        moeda_origem = moeda_origem.upper()
        moeda_destino = moeda_destino.upper()

        # 1. tenta cache
        entry = self._cache.get(moeda_origem, moeda_destino)
        if entry:
            return Cotacao(
                moeda_origem=moeda_origem,
                moeda_destino=moeda_destino,
                taxa_cambio=entry.valor,
                data_cotacao=entry.atualizado_em,
                fonte="cache",
            )

        # 2. se não tiver ou expirou, chama provider externo
        valor = await self._provider.buscar_cotacao(moeda_origem, moeda_destino)
        entry = self._cache.set(moeda_origem, moeda_destino, valor)

        return Cotacao(
            moeda_origem=moeda_origem,
            moeda_destino=moeda_destino,
            taxa_cambio=entry.valor,
            data_cotacao=entry.atualizado_em,
            fonte="api_externa",
        )
