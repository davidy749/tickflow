"""Loaders that normalise raw trade and quote data into tickflow's schema.

Real-world tick files use wildly different column names (``ts``, ``Time``,
``px``, ``qty`` ...). These helpers accept a renaming map and hand back a frame
that uses the canonical names defined in :mod:`tickflow.types`, with a sorted
``DatetimeIndex``-friendly timestamp column.
"""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd

from ._validation import require_columns
from .types import QUOTE_COLUMNS, TIME, TRADE_COLUMNS


def _normalise(
    frame: pd.DataFrame,
    rename: Mapping[str, str] | None,
    required: tuple[str, ...],
) -> pd.DataFrame:
    out = frame.rename(columns=dict(rename)) if rename else frame.copy()
    require_columns(out, required)
    out[TIME] = pd.to_datetime(out[TIME], utc=True)
    out = out.sort_values(TIME, kind="stable").reset_index(drop=True)
    return out


def read_trades(frame: pd.DataFrame, rename: Mapping[str, str] | None = None) -> pd.DataFrame:
    """Normalise a trades frame to ``(timestamp, price, size)``.

    Parameters
    ----------
    frame:
        Raw trades data.
    rename:
        Optional mapping from the source column names to canonical names.
    """
    out = _normalise(frame, rename, TRADE_COLUMNS)
    return out.loc[:, list(TRADE_COLUMNS)]


def read_quotes(frame: pd.DataFrame, rename: Mapping[str, str] | None = None) -> pd.DataFrame:
    """Normalise a quotes frame to ``(timestamp, bid, ask, bid_size, ask_size)``."""
    out = _normalise(frame, rename, QUOTE_COLUMNS)
    return out.loc[:, list(QUOTE_COLUMNS)]
