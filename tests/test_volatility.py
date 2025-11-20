import numpy as np
import pytest

from tickflow import (
    bipower_variation,
    har_features,
    jump_variation,
    realized_kernel,
    realized_variance,
    realized_volatility,
    two_scale_rv,
)
from tickflow.exceptions import InsufficientDataError


def test_realized_variance_matches_manual():
    prices = np.array([100.0, 101.0, 100.5, 102.0])
    r = np.diff(np.log(prices))
    assert realized_variance(prices) == pytest.approx(np.sum(r**2))


def test_realized_volatility_annualization():
    prices = np.array([100.0, 101.0, 100.0, 101.0])
    base = realized_volatility(prices)
    ann = realized_volatility(prices, annualize=252)
    assert ann == pytest.approx(base * np.sqrt(252))


def test_jump_variation_non_negative(rng):
    prices = 100 * np.exp(np.cumsum(rng.normal(0, 0.001, 200)))
    assert jump_variation(prices) >= 0.0


def test_bipower_below_rv_with_jump():
    # a single large jump inflates RV far more than bipower variation
    prices = np.concatenate([np.full(50, 100.0), np.full(50, 110.0)])
    prices = prices + np.linspace(0, 0.01, 100)
    assert bipower_variation(prices) < realized_variance(prices)


def test_two_scale_and_kernel_run(rng):
    prices = 100 * np.exp(np.cumsum(rng.normal(0, 0.0005, 300)))
    assert two_scale_rv(prices, slow_step=5) > 0
    assert realized_kernel(prices, bandwidth=2) > 0


def test_insufficient_data():
    with pytest.raises(InsufficientDataError):
        realized_variance([100.0])


def test_har_features_shape(rng):
    rv = rng.uniform(0.1, 0.2, 60)
    feats = har_features(rv)
    assert list(feats.columns) == ["rv_d", "rv_w", "rv_m", "target"]
    assert len(feats) == 60 - 22  # 22-day lookback drops the first rows
