"""Recover the bid-ask spread from a noisy price series with the Roll model."""

from __future__ import annotations

import numpy as np

import tickflow as tf


def main() -> None:
    rng = np.random.default_rng(11)
    n = 10_000
    true_spread = 0.02
    efficient = np.cumsum(rng.normal(0, 0.01, n))
    bounce = (true_spread / 2) * rng.choice([-1, 1], n)
    observed = 25 + efficient + bounce

    est = tf.roll_spread(observed)
    print(f"true spread:      {true_spread:.4f}")
    print(f"Roll estimate:    {est.value:.4f}  (n={est.n_obs})")


if __name__ == "__main__":
    main()
