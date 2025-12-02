import numpy as np
import pytest

from tickflow import implementation_shortfall, twap, vwap


def test_vwap_weights_by_volume():
    prices = np.array([100.0, 102.0])
    volumes = np.array([9.0, 1.0])
    assert vwap(prices, volumes) == pytest.approx((100 * 9 + 102 * 1) / 10)


def test_twap_is_mean():
    prices = np.array([100.0, 101.0, 102.0])
    assert twap(prices) == pytest.approx(101.0)


def test_vwap_requires_positive_volume():
    with pytest.raises(ValueError):
        vwap([100.0], [0.0])


def test_implementation_shortfall_buy_cost():
    # bought above arrival -> positive shortfall (a cost)
    cost = implementation_shortfall(100.0, [100.5, 100.5], [1, 1], side=1)
    assert cost == pytest.approx(0.5)


def test_implementation_shortfall_sell_cost():
    cost = implementation_shortfall(100.0, [99.5], [1], side=-1)
    assert cost == pytest.approx(0.5)
