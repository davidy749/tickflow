"""Liquidity and microstructure metrics estimated from trades and quotes."""

from __future__ import annotations

import numpy as np

from ._validation import as_float_array, log_returns, require_min_length
from .types import SpreadEstimate


def roll_spread(prices: object) -> SpreadEstimate:
    """Roll (1984) effective spread from the autocovariance of price changes.

    Under Roll's model the serial covariance of successive price changes is
    ``-s**2 / 4``, so the implied half-spread is ``sqrt(-cov)``. When the sample
    covariance is positive the model is mis-specified and the estimate is
    reported as ``0.0``.
    """
    prices = as_float_array(prices, "prices")
    require_min_length(prices, 3, "roll_spread")
    dp = np.diff(prices)
    cov = float(np.cov(dp[1:], dp[:-1], bias=True)[0, 1])
    spread = 2.0 * np.sqrt(-cov) if cov < 0 else 0.0
    return SpreadEstimate(value=spread, n_obs=dp.size - 1)


def amihud_illiquidity(prices: object, volumes: object) -> float:
    """Amihud (2002) illiquidity: mean of ``|return| / dollar volume``.

    Higher values mean a given amount of trading moves the price more.
    """
    prices = as_float_array(prices, "prices")
    volumes = as_float_array(volumes, "volumes")
    require_min_length(prices, 2, "amihud_illiquidity")
    if volumes.size != prices.size:
        raise ValueError("prices and volumes must be the same length")
    r = np.abs(log_returns(prices))
    dollar_vol = volumes[1:] * prices[1:]
    mask = dollar_vol > 0
    if not np.any(mask):
        raise ValueError("no positive dollar volume to compute illiquidity")
    return float(np.mean(r[mask] / dollar_vol[mask]))
