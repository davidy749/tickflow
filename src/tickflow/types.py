"""Shared column names and lightweight result containers."""

from __future__ import annotations

from dataclasses import dataclass

# Canonical column names used throughout the library. Loaders normalise incoming
# data to these names so estimators never have to guess.
TIME = "timestamp"
PRICE = "price"
SIZE = "size"
BID = "bid"
ASK = "ask"
BID_SIZE = "bid_size"
ASK_SIZE = "ask_size"

#: Columns a trades frame must expose after loading.
TRADE_COLUMNS = (TIME, PRICE, SIZE)
#: Columns a quotes frame must expose after loading.
QUOTE_COLUMNS = (TIME, BID, ASK, BID_SIZE, ASK_SIZE)


@dataclass(frozen=True)
class JumpTestResult:
    """Outcome of a jump-detection test at a single sampling point."""

    statistic: float
    threshold: float
    is_jump: bool


@dataclass(frozen=True)
class SpreadEstimate:
    """A spread estimate together with the number of observations behind it."""

    value: float
    n_obs: int
