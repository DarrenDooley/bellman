from src.models.enums import ExchangeLabel
from src.exchanges.base import BaseExchange
from src.exchanges.binance import BinanceExchange

def get_exchange(exchange_label: ExchangeLabel) -> BaseExchange:
    if exchange_label == ExchangeLabel.BINANCE:
        return BinanceExchange()
    # elif exchange_label == ExchangeLabel.OKX: todo implement OKX exchange
    #     return OkxExchange()
    else:
        raise ValueError(f"Unsupported exchange: {exchange_label}")
