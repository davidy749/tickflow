"""Estimate daily realized volatility from intraday prices.

Run with::

    python examples/01_realized_volatility.py
"""

from __future__ import annotations

import numpy as np

import tickflow as tf


def main() -> None:
    rng = np.random.default_rng(0)
    # one trading day of 1-second log prices
    log_prices = np.cumsum(rng.normal(0, 0.0002, 23_400))
    prices = 100 * np.exp(log_prices)

    rv = tf.realized_variance(prices)
    vol = tf.realized_volatility(prices, annualize=252)
    print(f"realized variance (day): {rv:.6e}")
    print(f"annualised volatility:   {vol:.2%}")
    print(f"noise-robust (kernel):   {tf.realized_kernel(prices, bandwidth=5):.6e}")


if __name__ == "__main__":
    main()
