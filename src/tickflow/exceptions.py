"""Exception types raised across tickflow."""

from __future__ import annotations


class TickflowError(Exception):
    """Base class for all tickflow errors."""


class SchemaError(TickflowError):
    """Raised when an input frame is missing required columns or has wrong dtypes."""


class InsufficientDataError(TickflowError):
    """Raised when an estimator does not have enough observations to compute a result."""
