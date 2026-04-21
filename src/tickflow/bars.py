"""Bar sampling schemes for tick data.

Sampling in *calendar time* oversamples quiet periods and undersamples busy
ones. Information-driven bars (tick / volume / dollar) sample once a fixed
amount of activity has accumulated, which tends to produce returns closer to
i.i.d. normal — see Lopez de Prado, *Advances in Financial Machine Learning*.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ._validation import require_columns
from .types import PRICE, SIZE, TIME


def _aggregate(frame: pd.DataFrame, group: pd.Series) -> pd.DataFrame:
    """Aggregate trades into OHLCV bars given a group label per row."""
    bars = frame.groupby(group).agg(
        open=(PRICE, "first"),
        high=(PRICE, "max"),
        low=(PRICE, "min"),
        close=(PRICE, "last"),
        volume=(SIZE, "sum"),
        n_trades=(PRICE, "size"),
        end_time=(TIME, "last"),
    )
    return bars.reset_index(drop=True)


def time_bars(trades: pd.DataFrame, freq: str = "1min") -> pd.DataFrame:
    """Resample trades into fixed calendar-time OHLCV bars.

    Parameters
    ----------
    trades:
        Frame with ``timestamp``, ``price`` and ``size`` columns.
    freq:
        Any pandas offset alias, e.g. ``"1min"``, ``"5s"``, ``"1h"``.
    """
    require_columns(trades, (TIME, PRICE, SIZE))
    idx = pd.to_datetime(trades[TIME])
    # Sort by time so the open/close of each bar reflect chronological order
    # even when the caller passes unsorted trades.
    order = idx.argsort(kind="stable")
    trades = trades.iloc[order]
    buckets = idx.iloc[order].dt.floor(freq)
    return _aggregate(trades, buckets)


def _threshold_groups(cumulative: np.ndarray, threshold: float) -> np.ndarray:
    """Assign a bar id to each row, closing a bar once ``cumulative`` crosses a
    multiple of ``threshold``.

    The running total resets at each close so bars hold roughly ``threshold``
    units of the driving quantity (ticks, volume, or dollars).
    """
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    groups = np.empty(cumulative.size, dtype=np.int64)
    bar = 0
    running = 0.0
    for i, value in enumerate(cumulative):
        running += value
        groups[i] = bar
        if running >= threshold:
            bar += 1
            running = 0.0
    return groups


def tick_bars(trades: pd.DataFrame, n_ticks: int) -> pd.DataFrame:
    """Sample a new bar every ``n_ticks`` trades."""
    require_columns(trades, (TIME, PRICE, SIZE))
    groups = _threshold_groups(np.ones(len(trades)), float(n_ticks))
    return _aggregate(trades, pd.Series(groups, index=trades.index))


def volume_bars(trades: pd.DataFrame, volume: float) -> pd.DataFrame:
    """Sample a new bar once cumulative traded ``size`` reaches ``volume``."""
    require_columns(trades, (TIME, PRICE, SIZE))
    groups = _threshold_groups(trades[SIZE].to_numpy(dtype=float), float(volume))
    return _aggregate(trades, pd.Series(groups, index=trades.index))


def dollar_bars(trades: pd.DataFrame, dollars: float) -> pd.DataFrame:
    """Sample a new bar once cumulative ``price * size`` reaches ``dollars``."""
    require_columns(trades, (TIME, PRICE, SIZE))
    notional = (trades[PRICE] * trades[SIZE]).to_numpy(dtype=float)
    groups = _threshold_groups(notional, float(dollars))
    return _aggregate(trades, pd.Series(groups, index=trades.index))
