"""Compare calendar-time bars with volume bars on synthetic trades."""

from __future__ import annotations

import numpy as np
import pandas as pd

import tickflow as tf


def make_trades(n: int = 5_000) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    start = pd.Timestamp("2025-03-03 09:30:00", tz="UTC")
    ts = start + pd.to_timedelta(np.cumsum(rng.exponential(0.2, n)), unit="s")
    price = 50 + np.cumsum(rng.normal(0, 0.005, n))
    size = rng.integers(1, 100, n)
    return pd.DataFrame({"timestamp": ts, "price": price, "size": size})


def main() -> None:
    trades = make_trades()
    tbars = tf.time_bars(trades, "1min")
    vbars = tf.volume_bars(trades, volume=trades["size"].sum() / len(tbars))
    print(f"time bars:   {len(tbars):3d}")
    print(f"volume bars: {len(vbars):3d}")
    print("volume-bar return std is usually closer to constant across bars")


if __name__ == "__main__":
    main()
