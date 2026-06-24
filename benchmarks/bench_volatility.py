"""Micro-benchmark for the realized-volatility estimators.

Not a pytest test — run directly::

    python benchmarks/bench_volatility.py
"""

from __future__ import annotations

import time

import numpy as np

import tickflow as tf


def _timeit(fn, prices, repeat: int = 50) -> float:
    start = time.perf_counter()
    for _ in range(repeat):
        fn(prices)
    return (time.perf_counter() - start) / repeat * 1e3  # ms per call


def main() -> None:
    rng = np.random.default_rng(0)
    prices = 100 * np.exp(np.cumsum(rng.normal(0, 0.0002, 23_400)))

    cases = {
        "realized_variance": tf.realized_variance,
        "bipower_variation": tf.bipower_variation,
        "two_scale_rv": lambda p: tf.two_scale_rv(p, slow_step=5),
        "realized_kernel": lambda p: tf.realized_kernel(p, bandwidth=5),
    }
    print(f"{'estimator':<20} {'ms/call':>10}")
    for name, fn in cases.items():
        print(f"{name:<20} {_timeit(fn, prices):>10.4f}")


if __name__ == "__main__":
    main()
