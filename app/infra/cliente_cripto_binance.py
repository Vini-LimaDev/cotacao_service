# app/infra/cliente_cripto_binance.py
import httpx
import asyncio
from typing import Dict


class HttpBinanceProvider:
    """
    Adapter para a Binance API.
    Documentação: https://binance-docs.github.io/apidocs/spot/en/
    """

    def __init__(self, base_url: str = "https://api.binance.com/api/v3", timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = 3
        self._retry_delay = 1  # segundos

    async def _fetch_price(self, symbol: str) -> float:
        """
        Busca o preço de um par de trading na Binance.
        
        Args:
            symbol: Par de trading (ex: "USDTBRL", "USDCBRL")
        
        Returns:
            Preço atual do par
        """
        url = f"{self._base_url}/ticker/price"
        params = {"symbol": symbol.upper()}

        last_exception = None
        
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url, params=params)

                # Tratamento de rate limit
                if resp.status_code == 429:
                    if attempt < self._max_retries - 1:
                        wait_time = self._retry_delay * (2 ** attempt)
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        raise httpx.HTTPStatusError(
                            f"Rate limit atingido após {self._max_retries} tentativas",
                            request=resp.request,
                            response=resp
                        )

                resp.raise_for_status()
                data = resp.json()
                
                if "price" not in data:
                    raise ValueError(f"Preço não encontrado para {symbol}")
                
                return float(data["price"])
                
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
        
        if last_exception:
            raise last_exception
        raise ValueError(f"Falha ao buscar preço de {symbol}")

    async def buscar_usdt_brl(self) -> float:
        """Busca a cotação de USDT em BRL."""
        return await self._fetch_price("USDTBRL")

    async def buscar_usdc_brl(self) -> float:
        """Busca a cotação de USDC em BRL."""
        return await self._fetch_price("USDCBRL")

    async def buscar_ambas_brl(self) -> Dict[str, float]:
        """
        Busca USDT e USDC em BRL em paralelo para maior performance.
        """
        try:
            # Executa ambas as requisições em paralelo
            usdt_task = self.buscar_usdt_brl()
            usdc_task = self.buscar_usdc_brl()
            
            usdt_price, usdc_price = await asyncio.gather(usdt_task, usdc_task)
            
            return {
                "USDT": usdt_price,
                "USDC": usdc_price
            }
        except Exception as e:
            # Se uma falhar, tenta pegar pelo menos uma
            resultado = {}
            try:
                resultado["USDT"] = await self.buscar_usdt_brl()
            except:
                pass
            
            try:
                resultado["USDC"] = await self.buscar_usdc_brl()
            except:
                pass
            
            if not resultado:
                raise ValueError(f"Nenhuma cotação encontrada: {str(e)}")
            
            return resultado
