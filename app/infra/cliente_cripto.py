# app/infra/cliente_cripto.py
import httpx
import asyncio
from typing import Dict


class HttpCoinGeckoProvider:
    """
    Adapter para a CoinGecko API.
    Documentação: https://docs.coingecko.com/reference/introduction
    """

    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3", timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = 3
        self._retry_delay = 2  # segundos

    async def buscar_cotacao_cripto(self, cripto_ids: str, moeda_destino: str = "brl") -> Dict[str, float]:
        """
        Busca a cotação de criptomoedas na CoinGecko API com retry.
        
        Args:
            cripto_ids: IDs das criptos separados por vírgula (ex: "tether,usd-coin")
            moeda_destino: Moeda de destino (padrão: "brl")
        
        Returns:
            Dict com as cotações, ex: {"tether": {"brl": 5.45}, "usd-coin": {"brl": 5.46}}
        
        Raises:
            httpx.HTTPStatusError se a resposta for inválida.
            ValueError se a cotação não for encontrada na resposta.
        """
        url = f"{self._base_url}/simple/price"
        params = {
            "ids": cripto_ids,
            "vs_currencies": moeda_destino.lower()
        }

        last_exception = None
        
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url, params=params)

                # Se for 429 (rate limit), aguarda mais tempo
                if resp.status_code == 429:
                    if attempt < self._max_retries - 1:
                        wait_time = self._retry_delay * (2 ** attempt)  # backoff exponencial
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        raise httpx.HTTPStatusError(
                            f"Rate limit atingido após {self._max_retries} tentativas",
                            request=resp.request,
                            response=resp
                        )

                # Levanta exceção HTTP se status >= 400
                resp.raise_for_status()

                data = resp.json()
                
                if not data:
                    raise ValueError(
                        f"Cotação para {cripto_ids} não encontrada na CoinGecko."
                    )

                return data
                
            except httpx.HTTPStatusError as e:
                last_exception = e
                if attempt < self._max_retries - 1 and e.response.status_code != 429:
                    await asyncio.sleep(self._retry_delay)
                    continue
                raise
            except Exception as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    await asyncio.sleep(self._retry_delay)
                    continue
                raise
        
        # Se chegou aqui, todas as tentativas falharam
        if last_exception:
            raise last_exception
        raise ValueError("Falha ao buscar cotação após múltiplas tentativas")

    async def buscar_usdt_brl(self) -> float:
        """Busca a cotação de USDT em BRL."""
        data = await self.buscar_cotacao_cripto("tether", "brl")
        
        if "tether" not in data or "brl" not in data["tether"]:
            raise ValueError("Cotação USDT/BRL não encontrada")
        
        return float(data["tether"]["brl"])

    async def buscar_usdc_brl(self) -> float:
        """Busca a cotação de USDC em BRL."""
        data = await self.buscar_cotacao_cripto("usd-coin", "brl")
        
        if "usd-coin" not in data or "brl" not in data["usd-coin"]:
            raise ValueError("Cotação USDC/BRL não encontrada")
        
        return float(data["usd-coin"]["brl"])

    async def buscar_ambas_brl(self) -> Dict[str, float]:
        """Busca USDT e USDC em BRL de uma vez."""
        data = await self.buscar_cotacao_cripto("tether,usd-coin", "brl")
        
        resultado = {}
        
        if "tether" in data and "brl" in data["tether"]:
            resultado["USDT"] = float(data["tether"]["brl"])
        
        if "usd-coin" in data and "brl" in data["usd-coin"]:
            resultado["USDC"] = float(data["usd-coin"]["brl"])
        
        if not resultado:
            raise ValueError("Nenhuma cotação encontrada")
        
        return resultado
