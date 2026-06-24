import numpy as np
import pytest

from tickflow import amihud_illiquidity, effective_spread, kyle_lambda, roll_spread


def test_roll_spread_recovers_known_spread(rng):
    # simulate a fundamental random walk plus bid-ask bounce of half-spread s/2
    n = 5000
    s = 0.04
    efficient = np.cumsum(rng.normal(0, 0.01, n))
    bounce = (s / 2) * rng.choice([-1, 1], n)
    observed = 100 + efficient + bounce
    est = roll_spread(observed)
    assert est.value == pytest.approx(s, abs=0.01)
    assert est.n_obs == n - 2


def test_roll_spread_zero_when_positive_cov():
    prices = np.array([100.0, 101.0, 102.0, 103.0, 104.0])
    assert roll_spread(prices).value == 0.0


def test_amihud_positive(rng):
    prices = 100 + np.cumsum(rng.normal(0, 0.1, 100))
    volumes = rng.uniform(100, 1000, 100)
    assert amihud_illiquidity(prices, volumes) > 0


def test_effective_spread_sign():
    # buyer-initiated trade above the mid is a positive cost
    val = effective_spread([100.1], [100.0], [1])
    assert val > 0


def test_kyle_lambda_slope():
    flow = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    dp = 0.5 * flow  # exact linear impact
    assert kyle_lambda(flow, dp) == pytest.approx(0.5)
