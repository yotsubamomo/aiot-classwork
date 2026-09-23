"""Fetch stage: acquire the raw F-D0047-091 JSON with the user's own CWA key.

This is the only module that touches the network or the key. The key is read from
the untracked ``.env`` and passed straight to the request header; it is never
printed, logged, echoed into an error message, or written to any file. Request
headers are never logged (R-SEC-1, R-SEC-2).
"""

from __future__ import annotations

from pathlib import Path

import requests

from . import config


class FetchError(RuntimeError):
    """A network / response failure that must abort ingestion.

    Messages carry the HTTP status and the CWA-provided message, never the key.
    """


def load_api_key(env_path: str | Path) -> str:
    """Read ``CWA_API_KEY`` from a ``.env`` file.

    Raises :class:`FetchError` with a key-free message if the file or the variable
    is missing or empty.
    """
    path = Path(env_path)
    if not path.is_file():
        raise FetchError(
            f"env file not found at {path}; copy .env.example to .env and set "
            f"{config.ENV_KEY_NAME}"
        )
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name, _, value = stripped.partition("=")
        if name.strip() == config.ENV_KEY_NAME:
            key = value.strip().strip('"').strip("'")
            if not key:
                raise FetchError(
                    f"{config.ENV_KEY_NAME} is empty in {path}; set your own CWA key"
                )
            return key
    raise FetchError(f"{config.ENV_KEY_NAME} not found in {path}")


def fetch_raw(
    api_key: str,
    *,
    url: str = config.CWA_DATASTORE_URL,
    params: dict | None = None,
    timeout: int = config.REQUEST_TIMEOUT_SECONDS,
) -> dict:
    """Fetch and validate one F-D0047-091 response, returning the parsed JSON.

    Confirms HTTP 200, ``success == "true"`` and ``result.resource_id`` equal to
    the teacher-named dataset id. Any deviation raises :class:`FetchError`.
    """
    request_params = config.REQUEST_PARAMS if params is None else params
    headers = {"Authorization": api_key}
    try:
        response = requests.get(
            url, headers=headers, params=request_params, timeout=timeout
        )
    except requests.Timeout as exc:
        raise FetchError(f"request to {url} timed out after {timeout}s") from exc
    except requests.RequestException as exc:
        # str(exc) may include the URL but never the header value.
        raise FetchError(f"request to {url} failed: {exc}") from exc

    if response.status_code != 200:
        raise FetchError(
            f"CWA returned HTTP {response.status_code}: "
            f"{_safe_message(response)}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise FetchError(
            f"CWA response was not valid JSON (HTTP {response.status_code})"
        ) from exc

    _validate_payload(data)
    return data


def _validate_payload(data: dict) -> None:
    """Confirm the success flag and dataset id (R-ING-3)."""
    success = str(data.get("success", "")).lower()
    if success != "true":
        raise FetchError(
            f"CWA response did not report success (success={data.get('success')!r})"
        )
    resource_id = (data.get("result") or {}).get("resource_id")
    if resource_id != config.RESOURCE_ID:
        raise FetchError(
            f"CWA response resource_id was {resource_id!r}, "
            f"expected {config.RESOURCE_ID!r}"
        )


def _safe_message(response: requests.Response) -> str:
    """Best-effort CWA error text, without ever exposing request headers/key."""
    try:
        payload = response.json()
    except ValueError:
        return response.text[:200]
    if isinstance(payload, dict):
        return str(payload.get("message", payload))
    return str(payload)[:200]
