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

_OHLCV = {
    "open": (PRICE, "first"),
    "high": (PRICE, "max"),
    "low": (PRICE, "min"),
    "close": (PRICE, "last"),
    "volume": (SIZE, "sum"),
}


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
    buckets = idx.dt.floor(freq)
    return _aggregate(trades, buckets)
