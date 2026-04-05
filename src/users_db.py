"""DynamoDB access for Users and optional JWT revocation records."""
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# TODO: Set USERS_TABLE_NAME, USERS_EMAIL_GSI_NAME in Lambda environment (or CDK/Terraform).
USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME", "TODO_USERS_TABLE")
EMAIL_GSI_NAME = os.environ.get("USERS_EMAIL_GSI_NAME", "EmailIndex")

# Optional: JWT revocation list (partition key `jti`, TTL attribute `ttl` — enable TTL on this attribute in console).

_REGION = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
_dynamodb = boto3.resource("dynamodb", region_name=_REGION)


def users_table():
    return _dynamodb.Table(USERS_TABLE_NAME)


def revocations_table():
    name = os.environ.get("REVOCATIONS_TABLE_NAME", "")
    if not name:
        return None
    return _dynamodb.Table(name)


def get_user_by_email(email: str):
    """Return user item or None."""
    tbl = users_table()
    resp = tbl.query(
        IndexName=EMAIL_GSI_NAME,
        KeyConditionExpression=Key("email").eq(email),
        Limit=1,
    )
    items = resp.get("Items", [])
    return items[0] if items else None


def create_user(user_id: str, email: str, password_hash: str, name: str, created_at: str):
    """Insert user. Caller must ensure email is not already registered."""
    users_table().put_item(
        Item={
            "user_id": user_id,
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "created_at": created_at,
        }
    )


def put_revoked_jti(jti: str, ttl_epoch: int):
    """Record revoked token id until ttl_epoch (Unix seconds). Table must have TTL enabled on `ttl`."""
    tbl = revocations_table()
    if tbl is None:
        return
    tbl.put_item(Item={"jti": jti, "ttl": ttl_epoch})


def is_jti_revoked(jti: str) -> bool:
    tbl = revocations_table()
    if tbl is None:
        return False
    try:
        resp = tbl.get_item(Key={"jti": jti})
        return "Item" in resp
    except ClientError as e:
        print("Error:", e)
        return False
