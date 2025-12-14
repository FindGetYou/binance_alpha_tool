from decimal import Decimal

from backend.core.precision import quantize
from backend.services.calculation_service import compute_diff_range


def test_quantize_round_half_up():
    assert str(quantize(Decimal('0.123456784'))) == '0.12345678'
    assert str(quantize(Decimal('0.123456785'))) == '0.12345679'


def test_compute_diff_range_basic():
    # price_now = 1 USDT/token, per_volume = 100 USDT
    # fee_amount_token = 2 tokens => fee_usdt = 2
    # waste_lower = 3 => x = (3-2)*1/100 = 0.01
    # waste_upper = 5 => x = (5-2)*1/100 = 0.03
    result = compute_diff_range(
        price_now=Decimal('1'),
        per_volume=Decimal('100'),
        waste_lower=Decimal('3'),
        waste_upper=Decimal('5'),
        fee_amount_token=Decimal('2'),
    )
    assert str(result['diff_lower']) == '0.01000000'
    assert str(result['diff_upper']) == '0.03000000'


def test_compute_diff_range_invalid():
    try:
        compute_diff_range(0, 0, 0, 0, 0)
        assert False, 'Expected ValueError'
    except ValueError:
        pass
