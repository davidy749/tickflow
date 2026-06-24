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
