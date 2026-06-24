"""Flag intraday jumps with the Lee-Mykland test."""

from __future__ import annotations

import numpy as np

import tickflow as tf


def main() -> None:
    rng = np.random.default_rng(3)
    returns = rng.normal(0, 0.0004, 2_000)
    returns[1_500] += 0.04  # inject a jump
    prices = 100 * np.exp(np.cumsum(returns))

    results = tf.lee_mykland_jumps(prices, window=270, alpha=0.01)
    jumps = [i for i, r in enumerate(results) if r.is_jump]
    print(f"tested points: {len(results)}")
    print(f"jumps flagged: {jumps}")


if __name__ == "__main__":
    main()
