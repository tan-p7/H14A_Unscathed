import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('api_keys')


def create_api_key(owner: str) -> str:
    api_key = str(uuid.uuid4())

    table.put_item(
        Item={
        "api_key": api_key,
        "owner": owner,
        "scope": "full",
        "active": True,
        "created_at": datetime.utcnow().isoformat()
        }
    )

    return api_key


def get_api_key(api_key: str):
    response = table.get_item(
        Key={"api_key": api_key}
    )
    return response.get("Item")


def is_valid_api_key(api_key: str) -> bool:
    item = get_api_key(api_key)

    if not item:
        return False

    # Optional expiry check
    if "expires_at" in item:
        if datetime.utcnow().isoformat() > item["expires_at"]:
            return False

    return True