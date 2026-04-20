"""Extract Bearer token and validate JWT for protected routes."""
import jwt
import src.users_db as users_db
from src.auth_tokens import decode_and_verify


def extract_bearer_token(event) -> str | None:
    headers = event.get("headers") or {}
    # API Gateway may normalize header names to lower case
    auth = headers.get("Authorization") or headers.get("authorization")
    if not auth or not isinstance(auth, str):
        return None
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip() or None


def get_auth_context(event) -> tuple[dict | None, str | None]:
    """
    Returns (claims, error_message).
    If error_message is set, caller should return 401 with that message (or a generic one).
    """
    token = extract_bearer_token(event)
    if not token:
        return None, "Missing or invalid Authorization header"

    try:
        claims = decode_and_verify(token)
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

    jti = claims.get("jti")
    if jti and users_db.is_jti_revoked(jti):
        return None, "Token has been revoked"

    return claims, None
