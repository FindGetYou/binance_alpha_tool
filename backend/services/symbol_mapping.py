"""
Helpers to resolve alphaId -> trading symbol.

Rules:
- If alphaId looks like a trading symbol already (ends with suffix like USDT), use as-is.
- Else, try to map via local data file backend/data/alpha_tokens.json if present.
- Else, treat alphaId as base token symbol and append suffix from config (default USDT).
"""
import json
import os
from typing import Optional

from backend.config import config

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "alpha_tokens.json")


def _load_local_tokens() -> dict:
    path = os.path.normpath(DATA_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


def resolve_symbol(alpha_id: str) -> Optional[str]:
    if not alpha_id:
        return None
    aid = alpha_id.strip().upper()
    # 1) Already a trading symbol like XYZUSDT
    if aid.endswith(config.ALPHA_SYMBOL_SUFFIX.upper()):
        return aid

    # 2) Local mapping file: expects entries like {"ALPHA_118": "KOGE"}
    local_map = _load_local_tokens()
    base = None
    if aid in local_map:
        base = str(local_map[aid]).strip().upper()
    else:
        # Maybe the alpha_id is already a base symbol like KOGE
        base = aid
    return f"{base}{config.ALPHA_SYMBOL_SUFFIX.upper()}"

