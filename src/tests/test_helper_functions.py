"""Tests for build_response CORS headers."""
from src.helper_functions import build_response
from src.constants import JSON_TYPE


def test_build_response_adds_cors_when_env_set(monkeypatch):
    monkeypatch.setenv("CORS_ALLOW_ORIGIN", "https://app.example.com")
    r = build_response(200, JSON_TYPE, {"ok": True})
    assert r["headers"]["Access-Control-Allow-Origin"] == "https://app.example.com"
    assert "Authorization" in r["headers"]["Access-Control-Allow-Headers"]


def test_build_response_no_cors_without_env(monkeypatch):
    monkeypatch.delenv("CORS_ALLOW_ORIGIN", raising=False)
    r = build_response(200, JSON_TYPE, {"ok": True})
    assert "Access-Control-Allow-Origin" not in r["headers"]


def test_build_response_204_empty_body():
    r = build_response(204, JSON_TYPE, "")
    assert r["statusCode"] == 204
    assert r["body"] == ""
