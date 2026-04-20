"""JWT creation and verification for auth."""
import os
import time
import uuid
import jwt

JWT_ALGORITHM = "HS256"


def _jwt_secret() -> str:
    return os.environ.get("JWT_SECRET", "TODO_DEV_JWT_SECRET_CHANGE_ME")


def _jwt_expiry_seconds() -> int:
    return int(os.environ.get("JWT_EXPIRY_SECONDS", "3600"))


def create_access_token(user_id: str, email: str) -> tuple[str, str, int]:
    """
    Returns (token, jti, expires_in_seconds).
    """
    jti = str(uuid.uuid4())
    now = int(time.time())
    ttl = _jwt_expiry_seconds()
    exp = now + ttl
    payload = {
        "sub": user_id,
        "email": email,
        "jti": jti,
        "iat": now,
        "exp": exp,
    }
    secret = _jwt_secret()
    token = jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token, jti, ttl


def decode_and_verify(token: str) -> dict:
    """Decode JWT or raise jwt.InvalidTokenError subclasses."""
    return jwt.decode(token, _jwt_secret(), algorithms=[JWT_ALGORITHM])
