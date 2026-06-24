"""tickflow: tools for analysing high-frequency financial time series."""

from __future__ import annotations

from .bars import dollar_bars, tick_bars, time_bars, volume_bars
from .exceptions import InsufficientDataError, SchemaError, TickflowError
from .execution import implementation_shortfall, twap, vwap
from .io import read_quotes, read_trades
from .jumps import lee_mykland_jumps
from .microstructure import (
    amihud_illiquidity,
    effective_spread,
    kyle_lambda,
    roll_spread,
)
from .orderbook import (
    classify_trades,
    microprice,
    mid_price,
    order_flow_imbalance,
    weighted_mid,
)
from .range_vol import garman_klass, parkinson
from .resample import align_prices, previous_tick
from .volatility import (
    bipower_variation,
    har_features,
    jump_variation,
    realized_kernel,
    realized_semivariance,
    realized_variance,
    realized_volatility,
    two_scale_rv,
)

__version__ = "0.2.0"

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
    # resample
    "previous_tick",
    "align_prices",
    # volatility
    "realized_variance",
    "realized_volatility",
    "bipower_variation",
    "jump_variation",
    "two_scale_rv",
    "realized_kernel",
    "realized_semivariance",
    "har_features",
    # range-based volatility
    "parkinson",
    "garman_klass",
    # microstructure
    "roll_spread",
    "amihud_illiquidity",
    "effective_spread",
    "kyle_lambda",
    # orderbook
    "mid_price",
    "weighted_mid",
    "microprice",
    "order_flow_imbalance",
    "classify_trades",
    # jumps
    "lee_mykland_jumps",
    # execution
    "vwap",
    "twap",
    "implementation_shortfall",
]
