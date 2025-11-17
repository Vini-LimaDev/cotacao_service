# app/infra/cache.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import RLock
from typing import Dict, Optional


@dataclass
class CacheEntry:
    valor: float
    atualizado_em: datetime


class CotacaoCache:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl = ttl_seconds
        self._data: Dict[str, CacheEntry] = {}
        self._lock = RLock()

    def _key(self, moeda_origem: str, moeda_destino: str) -> str:
        return f"{moeda_origem.upper()}->{moeda_destino.upper()}"

    def _is_valid(self, entry: CacheEntry) -> bool:
        agora = datetime.utcnow()
        return agora - entry.atualizado_em <= timedelta(seconds=self._ttl)

    def get(self, moeda_origem: str, moeda_destino: str) -> Optional[CacheEntry]:
        key = self._key(moeda_origem, moeda_destino)
        with self._lock:
            entry = self._data.get(key)
            if not entry:
                return None
            if not self._is_valid(entry):
                self._data.pop(key, None)
                return None
            return entry

    def set(self, moeda_origem: str, moeda_destino: str, valor: float) -> CacheEntry:
        key = self._key(moeda_origem, moeda_destino)
        entry = CacheEntry(valor=valor, atualizado_em=datetime.utcnow())
        with self._lock:
            self._data[key] = entry
        return entry
