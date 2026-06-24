import numpy as np

from tickflow import lee_mykland_jumps


def test_no_jumps_in_smooth_series(rng):
    prices = 100 * np.exp(np.cumsum(rng.normal(0, 0.0005, 600)))
    results = lee_mykland_jumps(prices, window=270, alpha=0.01)
    flagged = sum(r.is_jump for r in results)
    # a calm random walk should rarely trip the detector
    assert flagged <= 2


def test_detects_injected_jump(rng):
    returns = rng.normal(0, 0.0005, 600)
    returns[400] += 0.05  # large isolated jump
    prices = 100 * np.exp(np.cumsum(returns))
    results = lee_mykland_jumps(prices, window=270, alpha=0.01)
    assert any(r.is_jump for r in results)
