from binance.spot import Spot as BinanceClient
import os
import logging

from src.exchanges.base import BaseExchange
from src.models.enums import ExchangeLabel
from src.models.models import ExchangeData

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class BinanceExchange(BaseExchange):
    def __init__(self):
        super().__init__(ExchangeLabel.BINANCE)

    def parse_exchange_data(self, exchange_label, symbol_label, exchange_info: dict) -> ExchangeData:
        symbol_data = exchange_info['symbols'][0]
        price_filter = next(filter(lambda x: x['filterType'] == 'PRICE_FILTER', symbol_data['filters']))
        return ExchangeData(
            exchange_label=exchange_label,
            symbol_label=symbol_label,
            symbol=symbol_data['symbol'],
            min_price = price_filter["minPrice"],
            max_price = price_filter["maxPrice"],
            tick_size = price_filter["tickSize"]
        )
       
    def fetch_exchange_data(self, exchange_label, symbol_label: str):
        api_key = os.environ.get('BINANCE_API_KEY')
        api_secret = os.environ.get('BINANCE_API_SECRET')
        symbol = symbol_label.replace("-", "")

        binance_client = BinanceClient(api_key, api_secret)

        try:
            exchange_info = binance_client.exchange_info(symbol=symbol)

            return self.parse_exchange_data(exchange_label, symbol_label, exchange_info)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            
            raise e # todo: use custom exception class here
