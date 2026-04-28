import uuid
import os
import boto3
from datetime import datetime

TABLE_NAME = "api_keys"


def get_table():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    dynamodb = boto3.resource("dynamodb", region_name=region)
    return dynamodb.Table(TABLE_NAME)


def create_api_key(owner: str) -> str:
    table = get_table()

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
    table = get_table()

    response = table.get_item(Key={"api_key": api_key})
    return response.get("Item")


def is_valid_api_key(api_key: str) -> bool:
    item = get_api_key(api_key)

    if not item:
        return False

    if "expires_at" in item:
        if datetime.utcnow().isoformat() > item["expires_at"]:
            return False

    return True