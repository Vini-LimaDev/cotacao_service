# app/infra/external_client.py
import httpx
import asyncio
from typing import Optional

from app.domain.portas import CotacaoProvider


class HttpFrankfurterProvider(CotacaoProvider):
    """
    Adapter para a Frankfurter API.
    Documentação: https://www.frankfurter.app/docs/
    """

    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 3) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def buscar_cotacao(self, moeda_origem: str, moeda_destino: str) -> float:
        """
        Busca a cotação entre duas moedas na Frankfurter API.
        Raises httpx.HTTPStatusError se a resposta for inválida.
        Raises ValueError se a cotação não for encontrada na resposta.
        Raises httpx.TimeoutException se a requisição demorar muito.
        """
        moeda_origem = moeda_origem.upper()
        moeda_destino = moeda_destino.upper()

        url = f"{self._base_url}/latest"
        params = {"from": moeda_origem, "to": moeda_destino}

        last_error: Optional[Exception] = None
        
        for tentativa in range(self._max_retries):
            try:
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
            
            except httpx.TimeoutException as e:
                last_error = e
                if tentativa < self._max_retries - 1:
                    await asyncio.sleep(1 * (tentativa + 1))  # Backoff exponencial
                    continue
                raise ValueError(f"A API de cotações demorou muito para responder após {self._max_retries} tentativas. Tente novamente.")
            
            except httpx.ConnectError as e:
                last_error = e
                if tentativa < self._max_retries - 1:
                    await asyncio.sleep(1 * (tentativa + 1))
                    continue
                raise ValueError(f"Não foi possível conectar à API de cotações após {self._max_retries} tentativas. Verifique sua conexão.")
            
            except httpx.HTTPStatusError as e:
                # Não faz retry em erros HTTP (4xx, 5xx)
                raise ValueError(f"API retornou erro {e.response.status_code}: {e.response.text}")
            
            except Exception as e:
                # Outros erros não esperados
                last_error = e
                if tentativa < self._max_retries - 1:
                    await asyncio.sleep(1 * (tentativa + 1))
                    continue
                raise
        
        # Se chegou aqui, todas as tentativas falharam
        if last_error:
            raise last_error
