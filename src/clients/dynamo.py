import boto3
import logging
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DynamoDBOperations:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(name=table_name)

    def get_item(self, exchange: str, symbol: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(Key={'exchange': exchange, 'symbol': symbol})
            return response.get('Item')
        except ClientError as e:
            logger.error(f"Error fetching from DynamoDB: {e.response['Error']['Message']}")
            return None

    def put_item(self, item: Dict[str, Any]) -> bool:
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            logger.error(f"Error storing in DynamoDB: {e.response['Error']['Message']}")
            return False
