# app/infra/external_client.py
import httpx

from app.domain.portas import CotacaoProvider


class HttpFrankfurterProvider(CotacaoProvider):
    """
    Adapter para a Frankfurter API.
    Documentação: https://www.frankfurter.app/docs/
    """

    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def buscar_cotacao(self, moeda_origem: str, moeda_destino: str) -> float:
        """
        Busca a cotação entre duas moedas na Frankfurter API.
        Raises httpx.HTTPStatusError se a resposta for inválida.
        Raises ValueError se a cotação não for encontrada na resposta.
        """
        moeda_origem = moeda_origem.upper()
        moeda_destino = moeda_destino.upper()

        url = f"{self._base_url}/latest"
        params = {"from": moeda_origem, "to": moeda_destino}

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.get(url, params=params)

        # Levanta exceção HTTP se status >= 400
        resp.raise_for_status()

        data = resp.json()
        rates = data.get("rates") or {}

        if moeda_destino not in rates:
            raise ValueError(
                f"Cotação {moeda_origem}->{moeda_destino} não encontrada na Frankfurter."
            )

        valor = rates[moeda_destino]
        return float(valor)
