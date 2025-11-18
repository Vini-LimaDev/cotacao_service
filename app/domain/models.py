# app/domain/models.py
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Moeda = Literal["USD", "EUR", "BRL", "JPY", "GBP", "AUD", "CAD", "CHF"]  # pode ampliar depois


class Cotacao(BaseModel):
    moeda_origem: Moeda
    moeda_destino: Moeda
    taxa_cambio: float
    data_cotacao: datetime
    fonte: Literal["cache", "api_externa"]
