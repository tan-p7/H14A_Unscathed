"""Register, login, and logout HTTP handlers (JSON)."""
import json
import re
import uuid
from datetime import datetime, timezone
from json import JSONDecodeError

import bcrypt
from botocore.exceptions import ClientError

from src.helper_functions import build_response
from src.constants import JSON_TYPE
import src.users_db as users_db
from src.auth_tokens import create_access_token, decode_and_verify
import jwt

MIN_PASSWORD_LENGTH = 8
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _parse_json_body(body: str) -> dict | None:
    if not body:
        return None
    try:
        return json.loads(body)
    except JSONDecodeError:
        return None


def register(event):
    """POST /api/auth/register — JSON { email, password, name }."""
    body = _parse_json_body(event.get("body") or "")
    if body is None:
        return build_response(400, JSON_TYPE, "Invalid JSON body")

    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    name = (body.get("name") or "").strip()

    if not email or not EMAIL_RE.match(email):
        return build_response(400, JSON_TYPE, "Valid email is required")
    if not isinstance(password, str) or len(password) < MIN_PASSWORD_LENGTH:
        return build_response(
            400, JSON_TYPE, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
        )
    if not name:
        return build_response(400, JSON_TYPE, "Name is required")

    if users_db.get_user_by_email(email):
        return build_response(409, JSON_TYPE, "Email already registered")

    user_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        users_db.create_user(user_id, email, pw_hash, name, created_at)
    except ClientError as e:
        print("Error:", e)
        return build_response(503, JSON_TYPE, e.response["Error"]["Message"])

    return build_response(
        201,
        JSON_TYPE,
        {"userId": user_id, "email": email, "name": name},
    )


def login(event):
    """POST /api/auth/login — JSON { email, password }."""
    body = _parse_json_body(event.get("body") or "")
    if body is None:
        return build_response(400, JSON_TYPE, "Invalid JSON body")

    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    if not email:
        return build_response(400, JSON_TYPE, "Email is required")

    user = users_db.get_user_by_email(email)
    if not user:
        return build_response(401, JSON_TYPE, "Invalid email or password")

    stored = user.get("password_hash") or ""
    if not bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8")):
        return build_response(401, JSON_TYPE, "Invalid email or password")

    token, _jti, expires_in = create_access_token(user["user_id"], user["email"])
    return build_response(
        200,
        JSON_TYPE,
        {
            "accessToken": token,
            "tokenType": "Bearer",
            "expiresIn": expires_in,
        },
    )


def logout(event):
    """POST /api/auth/logout — Bearer token; records jti in revocations table if configured."""
    from src.auth_dependencies import extract_bearer_token

    token = extract_bearer_token(event)
    if not token:
        return build_response(401, JSON_TYPE, "Missing or invalid Authorization header")

    try:
        claims = decode_and_verify(token)
    except jwt.ExpiredSignatureError:
        return build_response(401, JSON_TYPE, "Token has expired")
    except jwt.InvalidTokenError:
        return build_response(401, JSON_TYPE, "Invalid token")

    jti = claims.get("jti")
    exp = claims.get("exp")
    if jti and isinstance(exp, (int, float)):
        users_db.put_revoked_jti(jti, int(exp))

    return build_response(204, JSON_TYPE, "")
