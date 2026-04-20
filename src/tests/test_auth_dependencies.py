"""Tests for Bearer extraction and auth context."""
import jwt
import pytest
from unittest.mock import patch

from src.auth_dependencies import extract_bearer_token, get_auth_context


def test_extract_bearer_missing():
    assert extract_bearer_token({}) is None
    assert extract_bearer_token({"headers": {}}) is None


def test_extract_bearer_ok():
    tok = extract_bearer_token(
        {"headers": {"Authorization": "Bearer abc.def.ghi"}}
    )
    assert tok == "abc.def.ghi"


def test_get_auth_context_revoked(monkeypatch):
    secret = "test-jwt-secret-must-be-at-least-32-chars"
    monkeypatch.setenv("JWT_SECRET", secret)
    token = jwt.encode(
        {"sub": "u", "email": "a@b.com", "jti": "j1", "exp": 9999999999, "iat": 1},
        secret,
        algorithm="HS256",
    )
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    with patch("src.auth_dependencies.users_db.is_jti_revoked", return_value=True):
        claims, err = get_auth_context(
            {"headers": {"Authorization": f"Bearer {token}"}}
        )
    assert claims is None
    assert err == "Token has been revoked"
