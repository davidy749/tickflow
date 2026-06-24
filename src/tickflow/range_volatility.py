"""Range-based volatility estimators that use OHLC bars.

When only OHLC bars are available (not the full tick path), range estimators are
far more efficient than close-to-close volatility because they use the high and
low, which carry information about the intraday path.
"""

from __future__ import annotations

import numpy as np

from ._validation import as_float_array


def parkinson(high: object, low: object) -> float:
    """Parkinson (1980) volatility from high/low ranges.

    Assumes a driftless geometric Brownian motion; biased low when there are
    jumps or an opening gap, since it ignores open/close.
    """
    h = as_float_array(high, "high")
    low_ = as_float_array(low, "low")
    if h.size != low_.size:
        raise ValueError("high and low must be equal length")
    if np.any(h <= 0) or np.any(low_ <= 0):
        raise ValueError("prices must be positive")
    log_hl = np.log(h / low_)
    return float(np.sqrt(np.mean(log_hl**2) / (4.0 * np.log(2.0))))


def garman_klass(open_: object, high: object, low: object, close: object) -> float:
    """Garman-Klass (1980) volatility from full OHLC bars.

    More efficient than Parkinson by also using the open-to-close move.
    """
    o = as_float_array(open_, "open")
    h = as_float_array(high, "high")
    low_ = as_float_array(low, "low")
    c = as_float_array(close, "close")
    if not (o.size == h.size == low_.size == c.size):
        raise ValueError("open, high, low, close must be equal length")
    hl = np.log(h / low_)
    co = np.log(c / o)
    var = 0.5 * hl**2 - (2.0 * np.log(2.0) - 1.0) * co**2
    return float(np.sqrt(np.mean(var)))
