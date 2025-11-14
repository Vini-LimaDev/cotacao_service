from datetime import datetime
from typing import Literal

from pydantic import BaseModel

class Cotacao(BaseModel):
    id: int
    moeda_origem: Literal['USD', 'EUR', 'BRL', 'JPY']
    moeda_destino: Literal['USD', 'EUR', 'BRL', 'JPY']
    taxa_cambio: float
    data_cotacao: datetime