"""
Calculation logic for price diff range using ROUND_HALF_UP with 8 decimals.
"""
from decimal import Decimal
from typing import Dict

from backend.core.precision import to_decimal, quantize


def compute_fee_usdt(fee_amount_token, price_now) -> Decimal:
    """fee_usdt = fee_amount_token * price_now"""
    fee = to_decimal(fee_amount_token) * to_decimal(price_now)
    # Round only at boundary
    return quantize(fee)


def compute_diff_range(price_now, per_volume, waste_lower, waste_upper, fee_amount_token) -> Dict[str, Decimal]:
    """Inverse solve price diff x from waste bounds.
    x = (estimate_waste - fee_usdt) * price_now / per_volume
    Returns absolute price diffs in quote currency per token.
    """
    price_now_d = to_decimal(price_now)
    per_volume_d = to_decimal(per_volume)
    if per_volume_d <= 0 or price_now_d <= 0:
        raise ValueError("price_now and per_volume must be > 0")

    fee_usdt = to_decimal(fee_amount_token) * price_now_d
    token_amount = (per_volume_d - fee_usdt) / price_now_d
    lower = to_decimal(waste_lower) / token_amount
    upper = to_decimal(waste_upper) / token_amount

    # Normalize ordering and quantize
    lo = quantize(lower)
    up = quantize(upper)
    if up < lo:
        lo, up = up, lo
    return {"diff_lower": lo, "diff_upper": up}
