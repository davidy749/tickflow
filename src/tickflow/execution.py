"""Execution benchmarks: VWAP, TWAP and implementation shortfall."""

from __future__ import annotations

import numpy as np

from ._validation import as_float_array, require_min_length


def vwap(prices: object, volumes: object) -> float:
    """Volume-weighted average price."""
    p = as_float_array(prices, "prices")
    v = as_float_array(volumes, "volumes")
    if p.size != v.size:
        raise ValueError("prices and volumes must be equal length")
    require_min_length(p, 1, "vwap")
    total = float(np.sum(v))
    if total <= 0:
        raise ValueError("total volume must be positive")
    return float(np.sum(p * v) / total)


def twap(prices: object) -> float:
    """Time-weighted average price (mean over equally spaced samples)."""
    p = as_float_array(prices, "prices")
    require_min_length(p, 1, "twap")
    return float(np.mean(p))


def implementation_shortfall(
    arrival_price: float, fill_prices: object, fill_sizes: object, side: int = 1
) -> float:
    """Implementation shortfall versus an arrival (decision) price.

    Positive numbers are a cost. ``side`` is ``+1`` for a buy and ``-1`` for a
    sell, so paying above arrival on a buy (or selling below it) is a loss.
    """
    fp = as_float_array(fill_prices, "fill_prices")
    fs = as_float_array(fill_sizes, "fill_sizes")
    if fp.size != fs.size:
        raise ValueError("fill_prices and fill_sizes must be equal length")
    require_min_length(fp, 1, "implementation_shortfall")
    filled = float(np.sum(fs))
    if filled <= 0:
        raise ValueError("total filled size must be positive")
    avg = float(np.sum(fp * fs) / filled)
    return float(side) * (avg - arrival_price)
