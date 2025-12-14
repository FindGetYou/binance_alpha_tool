"""
Service for Alpha token price snapshot.
Fetches recent agg trades and computes last, average and vwap prices.
"""
from typing import Dict, List, Any
from datetime import datetime, timezone
from decimal import Decimal

from backend.services.binance_client import fetch_agg_trades, parse_price_qty
from backend.services.symbol_mapping import resolve_symbol
from backend.core.precision import quantize, to_decimal


def _aggregate_prices(trades: List[Dict[str, Any]]) -> Dict[str, Decimal]:
    if not trades:
        raise ValueError("No trades available for aggregation")
    # last price: last trade's price
    last_p = None
    sum_p = Decimal("0")
    sum_pq = Decimal("0")
    sum_q = Decimal("0")
    for t in trades:
        p, q = parse_price_qty(t)
        last_p = p
        sum_p += p
        sum_pq += p * q
        sum_q += q
    count = Decimal(str(len(trades)))
    avg = sum_p / count
    vwap = (sum_pq / sum_q) if sum_q > 0 else last_p
    return {
        "last": quantize(last_p),
        "avg": quantize(avg),
        "vwap": quantize(vwap),
    }


async def fetch_alpha_price(alpha_id: str) -> Dict:
    symbol = resolve_symbol(alpha_id)
    if not symbol:
        raise ValueError("Unable to resolve symbol from alphaId")
    trades = await fetch_agg_trades(symbol)
    metrics = _aggregate_prices(trades)
    ts = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    return {
        "symbol": symbol,
        "price_now": metrics["last"],
        "price_avg": metrics["avg"],
        "price_vwap": metrics["vwap"],
        "timestamp": ts,
    }
