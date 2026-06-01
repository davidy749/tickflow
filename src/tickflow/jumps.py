"""Non-parametric jump detection for high-frequency returns."""

from __future__ import annotations

import numpy as np

from ._constants import MU1
from ._validation import as_float_array, log_returns, require_min_length
from .types import FloatArray, JumpTestResult


def _local_volatility(returns: FloatArray, window: int) -> FloatArray:
    """Rolling bipower estimate of instantaneous volatility (Lee & Mykland)."""
    abs_prod = np.abs(returns[1:] * returns[:-1])
    bpv = np.full(returns.size, np.nan)
    for i in range(window, returns.size):
        bpv[i] = np.sqrt(np.mean(abs_prod[i - window : i]) / MU1**2)
    return bpv


def lee_mykland_jumps(
    prices: object, window: int = 270, alpha: float = 0.01
) -> list[JumpTestResult]:
    """Detect jumps with the Lee & Mykland (2008) statistic.

    Each return is standardised by a local bipower volatility; the maximum of a
    large number of such statistics follows a Gumbel law, which sets the
    critical threshold for significance level ``alpha``.
    """
    prices = as_float_array(prices, "prices")
    require_min_length(prices, window + 2, "lee_mykland_jumps")
    r = log_returns(prices)
    sigma = _local_volatility(r, window)

    n = np.sum(~np.isnan(sigma))
    c = (2.0 * np.log(n)) ** 0.5 / MU1
    s_n = 1.0 / (c * MU1)
    beta = c - (np.log(np.pi) + np.log(np.log(n))) / (2.0 * c * MU1)
    threshold = -np.log(-np.log(1.0 - alpha)) * s_n + beta

    results: list[JumpTestResult] = []
    for i in range(r.size):
        if np.isnan(sigma[i]) or sigma[i] == 0:
            continue
        stat = abs(r[i]) / sigma[i]
        results.append(
            JumpTestResult(
                statistic=float(stat),
                threshold=float(threshold),
                is_jump=bool(stat > threshold),
            )
        )
    return results
