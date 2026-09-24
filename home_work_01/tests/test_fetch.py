"""Fetch tests: AC-11 (HTTP 401/404/5xx/timeout/non-JSON via mock) and key
loading. All HTTP is mocked; no real request is made and no key is read from the
environment (R-TC-5)."""

from __future__ import annotations

import pytest
import requests

from ingestion import fetch
from ingestion.config import ENV_KEY_NAME
from ingestion.fetch import FetchError, fetch_raw, load_api_key

# Deliberately NOT shaped like a real CWA key: the fetch stage does not validate
# key format, so a plain placeholder keeps the key-format secret scan free of
# self-inflicted matches.
DUMMY_KEY = "test-dummy-key-not-a-real-cwa-key"


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text="", raise_json=False):
        self.status_code = status_code
        self._payload = payload
        self.text = text
        self._raise_json = raise_json

    def json(self):
        if self._raise_json:
            raise ValueError("no JSON")
        return self._payload


def _patch_get(monkeypatch, response=None, exc=None):
    def fake_get(url, **kwargs):
        # The key must be sent in the Authorization header, never in params/URL.
        assert kwargs["headers"]["Authorization"] == DUMMY_KEY
        if exc is not None:
            raise exc
        return response

    monkeypatch.setattr(fetch.requests, "get", fake_get)


def test_success(monkeypatch):
    payload = {"success": "true", "result": {"resource_id": "F-D0047-091"}}
    _patch_get(monkeypatch, FakeResponse(200, payload))
    assert fetch_raw(DUMMY_KEY) == payload


@pytest.mark.parametrize("status", [401, 404, 500, 503])
def test_http_error_status(monkeypatch, status):
    _patch_get(
        monkeypatch,
        FakeResponse(status, {"message": "boom"}),
    )
    with pytest.raises(FetchError) as exc:
        fetch_raw(DUMMY_KEY)
    assert str(status) in str(exc.value)


def test_timeout(monkeypatch):
    _patch_get(monkeypatch, exc=requests.Timeout())
    with pytest.raises(FetchError) as exc:
        fetch_raw(DUMMY_KEY)
    assert "timed out" in str(exc.value).lower()


def test_non_json_body(monkeypatch):
    _patch_get(monkeypatch, FakeResponse(200, raise_json=True, text="<html>"))
    with pytest.raises(FetchError) as exc:
        fetch_raw(DUMMY_KEY)
    assert "json" in str(exc.value).lower()


def test_success_false(monkeypatch):
    _patch_get(
        monkeypatch,
        FakeResponse(200, {"success": "false", "result": {"resource_id": "F-D0047-091"}}),
    )
    with pytest.raises(FetchError):
        fetch_raw(DUMMY_KEY)


def test_wrong_resource_id(monkeypatch):
    _patch_get(
        monkeypatch,
        FakeResponse(200, {"success": "true", "result": {"resource_id": "F-OTHER"}}),
    )
    with pytest.raises(FetchError) as exc:
        fetch_raw(DUMMY_KEY)
    assert "resource_id" in str(exc.value)


def test_error_message_never_leaks_key(monkeypatch):
    _patch_get(monkeypatch, FakeResponse(401, {"message": "Authorization key is not correct."}))
    with pytest.raises(FetchError) as exc:
        fetch_raw(DUMMY_KEY)
    assert DUMMY_KEY not in str(exc.value)


# --- key loading (R-ING-2) -----------------------------------------------------


def test_load_api_key_reads_value(tmp_path):
    env = tmp_path / ".env"
    env.write_text(f"{ENV_KEY_NAME}=CWA-abc-123\n", encoding="utf-8")
    assert load_api_key(env) == "CWA-abc-123"


def test_load_api_key_missing_file(tmp_path):
    with pytest.raises(FetchError):
        load_api_key(tmp_path / "nope.env")


def test_load_api_key_empty_value_message_has_no_value(tmp_path):
    env = tmp_path / ".env"
    env.write_text(f"{ENV_KEY_NAME}=\n", encoding="utf-8")
    with pytest.raises(FetchError) as exc:
        load_api_key(env)
    assert "empty" in str(exc.value).lower()
