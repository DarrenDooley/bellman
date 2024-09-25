import json
import os
import logging
from typing import Dict, Any
from pydantic import ValidationError

from src.clients.dynamo import DynamoDBOperations
from src.models.enums import ExchangeLabel
from src.models.models import PathParams, ExchangeData
from src.exchanges import factory


logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_ops = DynamoDBOperations(table_name=os.environ.get('DYNAMODB_TABLE'))


def data_handler(exchange_label: ExchangeLabel, symbol_label: str, bypass_cache: bool = False) -> ExchangeData:
    if not bypass_cache:
        logger.info(f"Fetching cached data for {exchange_label.value} - {symbol_label}")
        
        cached_data = db_ops.get_item(exchange_label.value, symbol_label)
        if cached_data:
            return ExchangeData(**cached_data)
        
    logger.info(f"Fetching data from exchange")
    exchange_obj = factory.get_exchange(exchange_label)
    exchange_data = exchange_obj.fetch_exchange_data(exchange_label, symbol_label)
    db_ops.put_item(exchange_data.dict())

    return exchange_data


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        path_parameters = event.get('pathParameters', {}) or {}
        headers = event.get('headers', {}) or {}
        exchange = path_parameters.get('exchange')
        symbol = path_parameters.get('symbol')
        parsed_path_params = PathParams(exchange_label=exchange, symbol_label=symbol)
        bypass_cache = headers.get('X-Bypass-Cache', '').lower() == 'true'
        
        result = data_handler(parsed_path_params.exchange_label, parsed_path_params.symbol_label, bypass_cache)

        return {
            "statusCode": 200,
            "body": result.model_dump_json(),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e}")

        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        logger.error(f"An error occurred: {e}")

        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }


if __name__ == "__main__":
    event = {
        "pathParameters": {
            "exchange": "binance",
            "symbol": "BTC-USDT"
        },
        "headers": {
            "X-Bypass-Cache": "false"
        }
    }

    print(lambda_handler(event=event, context={}))