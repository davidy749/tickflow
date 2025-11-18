"""Shared fixtures: small deterministic synthetic tick datasets."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(42)


@pytest.fixture
def trades(rng: np.random.Generator) -> pd.DataFrame:
    n = 500
    start = pd.Timestamp("2025-01-02 09:30:00", tz="UTC")
    ts = start + pd.to_timedelta(np.cumsum(rng.exponential(0.5, n)), unit="s")
    price = 100.0 + np.cumsum(rng.normal(0, 0.01, n))
    size = rng.integers(1, 50, n)
    return pd.DataFrame({"timestamp": ts, "price": price, "size": size})


@pytest.fixture
def quotes(rng: np.random.Generator) -> pd.DataFrame:
    n = 200
    start = pd.Timestamp("2025-01-02 09:30:00", tz="UTC")
    ts = start + pd.to_timedelta(np.arange(n), unit="s")
    mid = 100.0 + np.cumsum(rng.normal(0, 0.01, n))
    half = 0.01
    return pd.DataFrame(
        {
            "timestamp": ts,
            "bid": mid - half,
            "ask": mid + half,
            "bid_size": rng.integers(1, 100, n),
            "ask_size": rng.integers(1, 100, n),
        }
    )
