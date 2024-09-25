from abc import ABC, abstractmethod
from src.models.enums import ExchangeLabel

class BaseExchange(ABC):
    def __init__(self, name: ExchangeLabel):
        self.name = name

    @abstractmethod
    def fetch_exchange_data(self, symbol_label: str) -> dict:
        pass

    @abstractmethod
    def parse_exchange_data(self, symbol_label: str) -> dict:
        pass
