from pydantic import BaseModel, Field
from typing import List, Optional

from src.models.enums import ExchangeLabel


class ExchangeData(BaseModel):
    exchange_label: str
    symbol_label: str
    symbol: str
    tick_size: str
    min_price: str
    max_price: str
    tick_size: str

class PathParams(BaseModel):
    exchange_label: ExchangeLabel
    symbol_label: str = Field(..., min_length=1, max_length=10)


