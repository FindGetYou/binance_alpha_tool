"""
Thin client for Binance REST API.
"""
from typing import Any, Dict, List, Optional
from decimal import Decimal

from backend.config import config
from backend.core.http_client import get_async_client, request_with_retries


async def fetch_agg_trades(symbol: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch recent aggregate trades from Binance.
    Returns list of dicts with keys: p (price), q (qty), T (timestamp), etc.
    """
    lim = limit or config.DEFAULT_TRADES_LIMIT
    url = f"{config.BINANCE_REST_BASE}/bapi/defi/v1/public/alpha-trade/agg-trades"
    params = {"symbol": symbol, "limit": lim}
    async with get_async_client() as client:
        resp = await request_with_retries(client, "GET", url, params=params)
        resp.raise_for_status()
        return resp.json().get("data")


def parse_price_qty(trade: Dict[str, Any]) -> (Decimal, Decimal):
    # price is under 'p', qty under 'q'
    p = Decimal(str(trade.get("p", "0")))
    q = Decimal(str(trade.get("q", "0")))
    return p, q

