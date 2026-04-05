"""Tests for auth register, login, logout."""
import json
import os
import pytest
import bcrypt
import jwt
from unittest.mock import patch
from botocore.exceptions import ClientError

from src.auth_service import register, login, logout


@pytest.fixture(autouse=True)
def jwt_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "unit-test-jwt-secret-at-least-32-bytes-long")


def _event(body=None, headers=None):
    ev = {"httpMethod": "POST", "path": "/api/auth/x"}
    if body is not None:
        ev["body"] = body if isinstance(body, str) else json.dumps(body)
    if headers:
        ev["headers"] = headers
    return ev


class TestRegister:
    def test_invalid_json(self):
        r = register(_event("not json"))
        assert r["statusCode"] == 400

    def test_missing_email(self):
        r = register(_event({"password": "longenough", "name": "N"}))
        assert r["statusCode"] == 400

    def test_password_too_short(self):
        r = register(_event({"email": "a@b.com", "password": "short", "name": "N"}))
        assert r["statusCode"] == 400

    def test_duplicate_email(self):
        with patch("src.auth_service.users_db.get_user_by_email", return_value={"user_id": "x"}):
            r = register(_event({"email": "a@b.com", "password": "longenough", "name": "N"}))
        assert r["statusCode"] == 409

    def test_success(self):
        with patch("src.auth_service.users_db.get_user_by_email", return_value=None), patch(
            "src.auth_service.users_db.create_user"
        ) as mock_create:
            r = register(_event({"email": "New@B.com", "password": "longenough", "name": "User"}))
        assert r["statusCode"] == 201
        mock_create.assert_called_once()
        args = mock_create.call_args[0]
        assert args[1] == "new@b.com"  # normalized
        body = json.loads(r["body"])
        assert body["email"] == "new@b.com"
        assert body["name"] == "User"
        assert "userId" in body

    def test_dynamodb_error(self):
        err = ClientError(
            {"Error": {"Code": "x", "Message": "ddb fail"}},
            "PutItem",
        )
        with patch("src.auth_service.users_db.get_user_by_email", return_value=None), patch(
            "src.auth_service.users_db.create_user", side_effect=err
        ):
            r = register(_event({"email": "a@b.com", "password": "longenough", "name": "N"}))
        assert r["statusCode"] == 503


class TestLogin:
    def test_invalid_json(self):
        r = login(_event("x"))
        assert r["statusCode"] == 400

    def test_unknown_user(self):
        with patch("src.auth_service.users_db.get_user_by_email", return_value=None):
            r = login(_event({"email": "a@b.com", "password": "longenough"}))
        assert r["statusCode"] == 401

    def test_wrong_password(self):
        h = bcrypt.hashpw(b"right", bcrypt.gensalt()).decode("utf-8")
        user = {"user_id": "u1", "email": "a@b.com", "password_hash": h}
        with patch("src.auth_service.users_db.get_user_by_email", return_value=user):
            r = login(_event({"email": "a@b.com", "password": "wrongpass"}))
        assert r["statusCode"] == 401

    def test_success(self):
        h = bcrypt.hashpw(b"mypassword", bcrypt.gensalt()).decode("utf-8")
        user = {"user_id": "u1", "email": "a@b.com", "password_hash": h}
        with patch("src.auth_service.users_db.get_user_by_email", return_value=user):
            r = login(_event({"email": "a@b.com", "password": "mypassword"}))
        assert r["statusCode"] == 200
        body = json.loads(r["body"])
        assert body["tokenType"] == "Bearer"
        assert "accessToken" in body
        assert body["expiresIn"] > 0
        claims = jwt.decode(
            body["accessToken"],
            "unit-test-jwt-secret-at-least-32-bytes-long",
            algorithms=["HS256"],
        )
        assert claims["sub"] == "u1"
        assert claims["email"] == "a@b.com"


class TestLogout:
    def test_missing_authorization(self):
        r = logout(_event(headers={}))
        assert r["statusCode"] == 401

    def test_success_records_revocation_when_table_configured(self, monkeypatch):
        monkeypatch.setenv("REVOCATIONS_TABLE_NAME", "rev-table")
        token = jwt.encode(
            {"sub": "u1", "email": "a@b.com", "jti": "jid-1", "exp": 9999999999, "iat": 1},
            "unit-test-jwt-secret-at-least-32-bytes-long",
            algorithm="HS256",
        )
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        with patch("src.auth_service.users_db.put_revoked_jti") as mock_rev:
            r = logout(
                _event(headers={"Authorization": f"Bearer {token}"})
            )
        assert r["statusCode"] == 204
        mock_rev.assert_called_once_with("jid-1", 9999999999)
