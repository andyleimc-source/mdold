"""OAuth token management for Mingdao v1 API."""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE_API_URL = "https://api.mingdao.com"


def _find_project_root() -> Path:
    """Walk up from cwd to find .env or .secrets.json, fallback to package dir."""
    # First try: directory containing this source file (works regardless of cwd)
    pkg_dir = Path(__file__).resolve().parent.parent.parent
    if (pkg_dir / ".env").exists() or (pkg_dir / ".secrets.json").exists():
        return pkg_dir
    # Second try: walk up from cwd
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        if (d / ".env").exists() or (d / ".secrets.json").exists():
            return d
        if d == d.parent:
            break
    return pkg_dir


ROOT = _find_project_root()
ENV_PATH = ROOT / ".env"
SECRETS_PATH = ROOT / ".secrets.json"


def load_dotenv(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def get_env_config() -> dict[str, str]:
    load_dotenv()
    return {
        "app_key": os.getenv("MINGDAO_APP_KEY", ""),
        "app_secret": os.getenv("MINGDAO_APP_SECRET", ""),
        "redirect_uri": os.getenv("MINGDAO_REDIRECT_URI", ""),
    }


def load_secrets() -> dict[str, Any]:
    if not SECRETS_PATH.exists():
        return {}
    return json.loads(SECRETS_PATH.read_text(encoding="utf-8"))


def save_secrets(data: dict[str, Any]) -> None:
    SECRETS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _http_get(url: str, params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None and v != ""})
    req_url = f"{url}?{query}" if query else url
    req = urllib.request.Request(
        req_url,
        headers={"Accept": "application/json", "User-Agent": "mdold/0.1"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_authorize_url(app_key: str, redirect_uri: str) -> str:
    params = {"app_key": app_key, "redirect_uri": redirect_uri, "state": "mcp-auth"}
    return f"{BASE_API_URL}/oauth2/authorize?{urllib.parse.urlencode(params)}"


def exchange_code(*, app_key: str, app_secret: str, redirect_uri: str, code: str) -> dict[str, Any]:
    resp = _http_get(f"{BASE_API_URL}/oauth2/access_token", {
        "app_key": app_key, "app_secret": app_secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri, "code": code, "format": "json",
    })
    if resp.get("success") and resp.get("access_token"):
        now = int(time.time())
        stored = load_secrets()
        stored.update({
            "app_key": app_key, "app_secret": app_secret, "redirect_uri": redirect_uri,
            "access_token": resp["access_token"],
            "refresh_token": resp.get("refresh_token", ""),
            "expires_in": resp.get("expires_in", ""),
            "issued_at": now,
            "expires_at": now + int(resp.get("expires_in") or 0),
        })
        save_secrets(stored)
    return resp


def _refresh_token(*, app_key: str, app_secret: str, refresh_token: str) -> dict[str, Any]:
    resp = _http_get(f"{BASE_API_URL}/oauth2/access_token", {
        "app_key": app_key, "app_secret": app_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token, "format": "json",
    })
    if resp.get("success") and resp.get("access_token"):
        now = int(time.time())
        stored = load_secrets()
        stored.update({
            "app_key": app_key, "app_secret": app_secret,
            "access_token": resp["access_token"],
            "refresh_token": resp.get("refresh_token", refresh_token),
            "expires_in": resp.get("expires_in", ""),
            "issued_at": now,
            "expires_at": now + int(resp.get("expires_in") or 0),
        })
        save_secrets(stored)
    return resp


def _get_stored_auth() -> dict[str, Any]:
    config = get_env_config()
    secrets = load_secrets()
    return {
        "app_key": secrets.get("app_key") or config["app_key"],
        "app_secret": secrets.get("app_secret") or config["app_secret"],
        "redirect_uri": secrets.get("redirect_uri") or config["redirect_uri"],
        "access_token": secrets.get("access_token", ""),
        "refresh_token": secrets.get("refresh_token", ""),
        "expires_at": secrets.get("expires_at", 0),
    }


def _is_valid(auth: dict[str, Any]) -> bool:
    token = auth.get("access_token", "")
    expires_at = int(auth.get("expires_at") or 0)
    if not token:
        return False
    if not expires_at:
        return True
    return time.time() < (expires_at - 60)


def ensure_access_token() -> str:
    auth = _get_stored_auth()
    if _is_valid(auth):
        return str(auth["access_token"])

    if auth.get("refresh_token") and auth.get("app_key") and auth.get("app_secret"):
        resp = _refresh_token(
            app_key=str(auth["app_key"]),
            app_secret=str(auth["app_secret"]),
            refresh_token=str(auth["refresh_token"]),
        )
        if resp.get("success") and resp.get("access_token"):
            return str(resp["access_token"])

    if auth.get("app_key") and auth.get("redirect_uri"):
        url = build_authorize_url(str(auth["app_key"]), str(auth["redirect_uri"]))
        raise RuntimeError(
            "Token expired and cannot be refreshed. Re-authorize in browser:\n"
            f"{url}\n"
            "Then run: mdold exchange-code <code>"
        )

    raise RuntimeError("Missing app_key / redirect_uri. Check .env or .secrets.json.")
