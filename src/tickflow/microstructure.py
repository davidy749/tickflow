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


def effective_spread(
    trade_price: object, mid_price: object, side: object
) -> float:
    """Mean effective spread: ``2 * side * (trade_price - mid) / mid``.

    ``side`` is ``+1`` for buyer-initiated trades and ``-1`` for seller-
    initiated. The result is a relative (fraction-of-price) spread.
    """
    p = as_float_array(trade_price, "trade_price")
    mid = as_float_array(mid_price, "mid_price")
    s = as_float_array(side, "side")
    if not (p.size == mid.size == s.size):
        raise ValueError("trade_price, mid_price and side must be equal length")
    require_min_length(p, 1, "effective_spread")
    return float(np.mean(2.0 * s * (p - mid) / mid))


def kyle_lambda(signed_volume: object, price_change: object) -> float:
    """Kyle's lambda: price impact per unit of signed order flow.

    Estimated as the OLS slope of ``price_change`` on ``signed_volume``; larger
    values indicate a less liquid, more impactful market.
    """
    x = as_float_array(signed_volume, "signed_volume")
    y = as_float_array(price_change, "price_change")
    if x.size != y.size:
        raise ValueError("signed_volume and price_change must be equal length")
    require_min_length(x, 2, "kyle_lambda")
    var = float(np.var(x))
    if var == 0:
        raise ValueError("signed_volume has zero variance")
    cov = float(np.cov(x, y, bias=True)[0, 1])
    return cov / var
