"""Aligning irregularly spaced ticks onto a regular grid.

High-frequency series arrive at random times. Most estimators expect prices
sampled on a fixed grid, so we use *previous-tick* interpolation (the last
observed price at or before each grid point), which avoids look-ahead bias.
"""

from __future__ import annotations

import pandas as pd

from ._validation import require_columns
from .types import PRICE, TIME


def previous_tick(trades: pd.DataFrame, freq: str = "1s", price_col: str = PRICE) -> pd.Series:
    """Sample the last price at or before each point of a regular grid.

    Returns a price :class:`~pandas.Series` indexed by the regular grid. Grid
    points before the first trade are left as ``NaN``.
    """
    require_columns(trades, (TIME, price_col))
    s = pd.Series(
        trades[price_col].to_numpy(),
        index=pd.to_datetime(trades[TIME]),
    ).sort_index()
    grid = pd.date_range(s.index[0].floor(freq), s.index[-1].ceil(freq), freq=freq)
    return s.reindex(s.index.union(grid)).ffill().reindex(grid)


def align_prices(series: pd.Series, freq: str = "1s") -> pd.Series:
    """Forward-fill an already time-indexed price series onto a regular grid."""
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("series must have a DatetimeIndex")
    s = series.sort_index()
    grid = pd.date_range(s.index[0].floor(freq), s.index[-1].ceil(freq), freq=freq)
    return s.reindex(s.index.union(grid)).ffill().reindex(grid)
