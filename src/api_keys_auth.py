from src.api_keys_db import get_api_key


def extract_api_key(event):
    headers = event.get("headers", {}) or {}

    # Handle case variations
    return (
        headers.get("x-api-key")
        or headers.get("X-Api-Key")
        or headers.get("X-API-KEY")
    )


def require_api_key(event):
    key = extract_api_key(event)

    if not key:
        return False, {
            "statusCode": 403,
            "body": "Missing API key"
        }

    item = get_api_key(key)

    if not item:
        return False, {
            "statusCode": 403,
            "body": "Invalid API key"
        }

    # check active flag (defaults True if not present)
    if not item.get("active", True):
        return False, {
            "statusCode": 403,
            "body": "API key revoked"
        }

    # return owner email
    return True, item["owner"]