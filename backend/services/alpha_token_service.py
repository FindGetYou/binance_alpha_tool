"""
Service for Alpha token list.

Strategy:
- If config.ALPHA_TOKENS_API is set, fetch from there.
- Else, try to load local backend/data/alpha_tokens.json (keys: alphaId -> symbol).
- Else, return empty list.
"""
import json
import os
import logging
from typing import List, Dict
from urllib.parse import urlparse

from backend.config import config
from backend.core.http_client import get_async_client, request_with_retries

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "alpha_tokens.json")
logger = logging.getLogger("app.alpha_tokens")


async def fetch_alpha_tokens() -> List[Dict[str, str]]:
    # 1) External API if provided
    if config.ALPHA_TOKENS_API:
        src = config.ALPHA_TOKENS_API.strip()
        # 1) If src looks like a URL with scheme, try HTTP fetch
        parsed = urlparse(src)
        if parsed.scheme in ("http", "https"):
            try:
                async with get_async_client() as client:
                    resp = await request_with_retries(client, "GET", src)
                    resp.raise_for_status()
                    raw = resp.json()
            except Exception as e:
                logger.error("alpha tokens fetch failed from %s: %s", src, e)
                raw = None
            if raw is not None:
                # Accept array or wrapped object like { data: [...] } or mapping { alphaId: symbol }
                data = raw.get("data") if isinstance(raw, dict) and "data" in raw else raw
                out: List[Dict[str, str]] = []
                if isinstance(data, list):
                    for item in data:
                        if not isinstance(item, dict):
                            continue
                        symbol = item.get("symbol") or item.get("baseSymbol") or item.get("name")
                        alpha_id = item.get("alphaId") or item.get("id") or symbol
                        if symbol and alpha_id:
                            out.append({"symbol": str(symbol), "alphaId": str(alpha_id)})
                    return out
                if isinstance(data, dict):
                    for k, v in data.items():
                        out.append({"symbol": str(v), "alphaId": str(k)})
                    return out
                return out
        else:
            # 2) If src is a path, try to read local JSON file
            path = os.path.expanduser(src)
            if os.path.isabs(path) or os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        raw = json.load(f)
                    if isinstance(raw, list):
                        out: List[Dict[str, str]] = []
                        for item in raw:
                            if isinstance(item, dict) and "symbol" in item and ("alphaId" in item or "id" in item):
                                out.append({"symbol": str(item["symbol"]), "alphaId": str(item.get("alphaId") or item.get("id"))})
                        return out
                    if isinstance(raw, dict):
                        return [{"symbol": str(v), "alphaId": str(k)} for k, v in raw.items()]
                except Exception as e:
                    logger.error("alpha tokens load from file failed %s: %s", path, e)

    # 2) Local file fallback
    path = os.path.normpath(DATA_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [{"symbol": v, "alphaId": k} for k, v in raw.items()]

    # 3) Empty list
    return []
