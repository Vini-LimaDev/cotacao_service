# app/domain/ports.py
from abc import ABC, abstractmethod

from .models import Cotacao


class CotacaoProvider(ABC):
    @abstractmethod
    async def buscar_cotacao(self, moeda_origem: str, moeda_destino: str) -> float:
        """
        Busca a taxa de câmbio na API externa.
        Retorna apenas o valor numérico (taxa_cambio).
        """
        raise NotImplementedError


class CotacaoRepository(ABC):
    @abstractmethod
    async def obter_cotacao(self, moeda_origem: str, moeda_destino: str) -> Cotacao:
        """
        Retorna a cotação (com origem, destino, taxa, data e fonte),
        usando cache quando possível.
        """
        raise NotImplementedError
