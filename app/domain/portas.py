from abc import ABC, abstractmethod

from .models import Cotacao

class CotacaoProvider(ABC):
    @abstractmethod
    async def buscar_cotacao(self, moeda: str) -> float:        
        """
        Busca o valor da cotação em alguma fonte externa (API real ou fake).
        Deve retornar apenas o valor numérico.
        """
        raise NotImplementedError
    
class CotacaoRepository(ABC):
    @abstractmethod
    async def obter_cotacao(self, moeda: str) -> Cotacao:
        """
        Retorna a cotação da moeda, usando cache quando possível.
        """
        raise NotImplementedError