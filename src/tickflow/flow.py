"""Order-flow toxicity metrics."""

from __future__ import annotations

import numpy as np

from ._validation import as_float_array, require_min_length
from .types import FloatArray


def vpin(buy_volume: object, sell_volume: object, window: int = 50) -> FloatArray:
    """Volume-synchronised probability of informed trading (Easley et al., 2012).

    Given per-bucket buy and sell volumes (use equal-volume buckets), VPIN is the
    rolling mean of the volume imbalance ``|buy - sell| / (buy + sell)`` over
    ``window`` buckets. Higher values flag more toxic, one-sided flow.

    Returns one value per bucket from index ``window - 1`` onward.
    """
    buy = as_float_array(buy_volume, "buy_volume")
    sell = as_float_array(sell_volume, "sell_volume")
    if buy.size != sell.size:
        raise ValueError("buy_volume and sell_volume must be equal length")
    require_min_length(buy, window, "vpin")

    total = buy + sell
    with np.errstate(divide="ignore", invalid="ignore"):
        imbalance = np.where(total > 0, np.abs(buy - sell) / total, 0.0)
    csum = np.cumsum(imbalance)
    windowed = np.concatenate(([csum[window - 1]], csum[window:] - csum[:-window]))
    return np.asarray(windowed / window, dtype=np.float64)
