import random
from typing import Dict

from app.domain.portas import CotacaoProvider


class FakeCotacaoProvider(CotacaoProvider):
    """
    Simula uma API externa de cotação.
    Você pode deixar fixo ou gerar uma variaçãozinha aleatória.
    """

    _base_valores: Dict[str, float] = {
        "USD": 5.40,
        "EUR": 6.00,
        "BRL": 1.00,
    }

    async def buscar_cotacao(self, moeda: str) -> float:
        moeda = moeda.upper()
        base = self._base_valores.get(moeda, 4.00)

        # variaçãozinha de +/- 2%
        fator = 1 + random.uniform(-0.02, 0.02)
        valor = base * fator
        return round(valor, 4)
