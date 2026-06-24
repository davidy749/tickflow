"""Internal input-validation helpers.

These are not part of the public API but are shared by every estimator so that
error messages stay consistent.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from .exceptions import InsufficientDataError, SchemaError


def require_columns(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    """Raise :class:`SchemaError` if ``frame`` is missing any of ``columns``."""
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise SchemaError(f"frame is missing required columns: {missing}")


def as_float_array(values: object, name: str = "values") -> np.ndarray:
    """Coerce ``values`` to a 1-D float64 array, raising on ragged input."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise SchemaError(f"{name} must be one-dimensional, got {arr.ndim} dims")
    return arr


def require_min_length(arr: np.ndarray, minimum: int, what: str) -> None:
    """Raise :class:`InsufficientDataError` if ``arr`` is shorter than ``minimum``."""
    if arr.size < minimum:
        raise InsufficientDataError(f"{what} needs at least {minimum} observations, got {arr.size}")


def log_returns(prices: np.ndarray) -> np.ndarray:
    """Return log differences of a strictly positive price array."""
    if np.any(prices <= 0):
        raise SchemaError("prices must be strictly positive to take log returns")
    return np.diff(np.log(prices))
