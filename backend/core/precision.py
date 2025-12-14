"""
Decimal helpers with ROUND_HALF_UP and fixed 8-decimal quantization by default.
"""
from decimal import Decimal, getcontext, localcontext
from typing import Union

from backend.config import config

Number = Union[int, float, str, Decimal]

# Use a reasonably high precision for intermediate math
getcontext().prec = 36


def to_decimal(val: Number) -> Decimal:
    # String conversion avoids binary float artifacts
    return val if isinstance(val, Decimal) else Decimal(str(val))


def quantize(val: Number, places: int = None) -> Decimal:
    """Quantize to fixed decimal places using ROUND_HALF_UP.
    Only round at the boundary to keep intermediate precision.
    """
    d = to_decimal(val)
    p = config.DECIMAL_PLACES if places is None else places
    q = Decimal('1e-' + str(p))
    with localcontext() as ctx:
        ctx.rounding = config.ROUNDING_MODE
        return d.quantize(q, rounding=config.ROUNDING_MODE)


round_price = quantize  # alias for clarity
