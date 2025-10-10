"""Realized volatility estimators for high-frequency returns.

All estimators take a price array sampled on a (roughly) regular grid and work
on log returns internally. Conventions follow Andersen, Bollerslev, Diebold &
Labys and the realized-kernel literature (Barndorff-Nielsen et al.).
"""

from __future__ import annotations

import numpy as np

from ._validation import as_float_array, log_returns, require_min_length


def realized_variance(prices: object) -> float:
    """Sum of squared log returns — the simplest realized variance estimator.

    Consistent for integrated variance as the sampling interval shrinks, but
    biased upward in the presence of microstructure noise.
    """
    prices = as_float_array(prices, "prices")
    require_min_length(prices, 2, "realized_variance")
    r = log_returns(prices)
    return float(np.sum(r**2))


def realized_volatility(prices: object, annualize: float | None = None) -> float:
    """Square root of :func:`realized_variance`.

    Parameters
    ----------
    annualize:
        If given, multiply the result by ``sqrt(annualize)`` (e.g. pass the
        number of sampling periods per year).
    """
    rv = realized_variance(prices)
    vol = float(np.sqrt(rv))
    if annualize is not None:
        vol *= float(np.sqrt(annualize))
    return vol


# mu1 = E[|Z|] for a standard normal; the bipower scaling constant is mu1**-2.
_MU1 = np.sqrt(2.0 / np.pi)


def bipower_variation(prices: object) -> float:
    """Realized bipower variation (Barndorff-Nielsen & Shephard, 2004).

    Uses products of adjacent absolute returns, which stay finite across price
    jumps. This makes it an estimator of the *continuous* part of quadratic
    variation, so ``realized_variance - bipower_variation`` isolates the jump
    contribution.
    """
    prices = as_float_array(prices, "prices")
    require_min_length(prices, 3, "bipower_variation")
    r = np.abs(log_returns(prices))
    return float(_MU1**-2 * np.sum(r[1:] * r[:-1]))


def jump_variation(prices: object) -> float:
    """Non-negative jump component, ``max(RV - BV, 0)``."""
    return max(realized_variance(prices) - bipower_variation(prices), 0.0)


def _subsampled_rv(log_prices: np.ndarray, step: int) -> float:
    """Average realized variance over the ``step`` slow grids of a given scale."""
    totals = [
        np.sum(np.diff(log_prices[start::step]) ** 2) for start in range(step)
    ]
    return float(np.mean(totals))


def two_scale_rv(prices: object, slow_step: int = 5) -> float:
    """Two-scale realized variance (Zhang, Mykland & Aït-Sahalia, 2005).

    Combines a slow-grid average with a noise correction from the full (fast)
    grid to produce a consistent estimator under i.i.d. microstructure noise.
    """
    prices = as_float_array(prices, "prices")
    require_min_length(prices, slow_step + 2, "two_scale_rv")
    if slow_step < 2:
        raise ValueError("slow_step must be >= 2")
    lp = np.log(prices)
    n = lp.size - 1
    rv_slow = _subsampled_rv(lp, slow_step)
    rv_fast = float(np.sum(np.diff(lp) ** 2))
    n_bar = (n - slow_step + 1) / slow_step
    return float(rv_slow - (n_bar / n) * rv_fast)


def realized_kernel(prices: object, bandwidth: int = 1) -> float:
    """Flat-top Bartlett realized kernel (Barndorff-Nielsen et al., 2008).

    Adds autocovariance terms up to ``bandwidth`` lags with Bartlett weights to
    cancel the bias from serially correlated microstructure noise.
    """
    prices = as_float_array(prices, "prices")
    require_min_length(prices, bandwidth + 2, "realized_kernel")
    if bandwidth < 0:
        raise ValueError("bandwidth must be non-negative")
    r = log_returns(prices)
    gamma0 = float(np.sum(r**2))
    total = gamma0
    for h in range(1, bandwidth + 1):
        weight = 1.0 - h / (bandwidth + 1)
        gamma_h = float(np.sum(r[h:] * r[:-h]))
        total += 2.0 * weight * gamma_h
    return total
