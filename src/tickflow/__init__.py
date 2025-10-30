"""tickflow: tools for analysing high-frequency financial time series."""

from __future__ import annotations

from .bars import dollar_bars, tick_bars, time_bars, volume_bars
from .exceptions import InsufficientDataError, SchemaError, TickflowError
from .io import read_quotes, read_trades
from .volatility import (
    bipower_variation,
    jump_variation,
    realized_variance,
    realized_volatility,
)

__version__ = "0.0.0"

__all__ = [
    "__version__",
    # errors
    "TickflowError",
    "SchemaError",
    "InsufficientDataError",
    # io
    "read_trades",
    "read_quotes",
    # bars
    "time_bars",
    "tick_bars",
    "volume_bars",
    "dollar_bars",
    # volatility
    "realized_variance",
    "realized_volatility",
    "bipower_variation",
    "jump_variation",
]
