from decimal import Decimal

from backend.services.alpha_price_service import _aggregate_prices


def test_aggregate_prices_vwap_and_avg():
    trades = [
        {"p": "1.00000000", "q": "2.0"},
        {"p": "2.00000000", "q": "1.0"},
        {"p": "1.50000000", "q": "3.0"},
    ]
    res = _aggregate_prices(trades)
    # last price is last trade's price
    assert str(res["last"]) == "1.50000000"
    # avg = (1+2+1.5)/3 = 1.5
    assert str(res["avg"]) == "1.50000000"
    # vwap = (1*2 + 2*1 + 1.5*3) / (2+1+3) = (2 + 2 + 4.5) / 6 = 8.5/6 = 1.416666...
    assert str(res["vwap"]) == "1.41666667"
