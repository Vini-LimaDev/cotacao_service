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

    def _is_valid(self, entry: CacheEntry) -> bool:
        agora = datetime.utcnow()
        return agora - entry.atualizado_em <= timedelta(seconds=self._ttl)

    def get(self, moeda: str) -> Optional[CacheEntry]:
        moeda = moeda.upper()
        with self._lock:
            entry = self._data.get(moeda)
            if not entry:
                return None
            if not self._is_valid(entry):
                # Expirado: remove e devolve None
                self._data.pop(moeda, None)
                return None
            return entry

    def set(self, moeda: str, valor: float) -> CacheEntry:
        moeda = moeda.upper()
        entry = CacheEntry(valor=valor, atualizado_em=datetime.utcnow())
        with self._lock:
            self._data[moeda] = entry
        return entry
