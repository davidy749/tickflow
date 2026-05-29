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


def quoted_spread(bid: object, ask: object, relative: bool = True) -> float:
    """Mean quoted spread ``ask - bid``.

    With ``relative=True`` (default) the spread is divided by the mid, giving a
    fraction-of-price figure that is comparable across instruments.
    """
    b = as_float_array(bid, "bid")
    a = as_float_array(ask, "ask")
    if b.size != a.size:
        raise ValueError("bid and ask must be equal length")
    require_min_length(b, 1, "quoted_spread")
    spread = a - b
    if relative:
        spread = 2.0 * spread / (a + b)
    return float(np.mean(spread))


def corwin_schultz(high: object, low: object) -> float:
    """Corwin-Schultz (2012) high-low bid-ask spread estimator.

    Recovers the spread from the ratio of two-day to one-day high-low ranges,
    which separates the volatility and spread contributions. Negative estimates
    (a sign of low volatility relative to the spread) are floored at zero.
    """
    h = as_float_array(high, "high")
    low_ = as_float_array(low, "low")
    if h.size != low_.size:
        raise ValueError("high and low must be equal length")
    require_min_length(h, 2, "corwin_schultz")

    beta = np.log(h[:-1] / low_[:-1]) ** 2 + np.log(h[1:] / low_[1:]) ** 2
    h2 = np.maximum(h[:-1], h[1:])
    l2 = np.minimum(low_[:-1], low_[1:])
    gamma = np.log(h2 / l2) ** 2

    const = 3.0 - 2.0 * np.sqrt(2.0)
    alpha = (np.sqrt(2.0 * beta) - np.sqrt(beta)) / const - np.sqrt(gamma / const)
    spread = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))
    return float(np.mean(np.maximum(spread, 0.0)))


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


def effective_spread(trade_price: object, mid_price: object, side: object) -> float:
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
