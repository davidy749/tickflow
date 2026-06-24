import numpy as np
import pytest

from tickflow import garman_klass, parkinson


def test_parkinson_positive(rng):
    base = 100 + np.cumsum(rng.normal(0, 0.1, 100))
    high = base + np.abs(rng.normal(0, 0.2, 100))
    low = base - np.abs(rng.normal(0, 0.2, 100))
    assert parkinson(high, low) > 0


def test_parkinson_zero_for_flat_bars():
    high = np.full(10, 100.0)
    low = np.full(10, 100.0)
    assert parkinson(high, low) == pytest.approx(0.0)


def test_garman_klass_runs(rng):
    o = 100 + rng.normal(0, 0.1, 50)
    c = o + rng.normal(0, 0.1, 50)
    high = np.maximum(o, c) + 0.05
    low = np.minimum(o, c) - 0.05
    assert garman_klass(o, high, low, c) >= 0


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        parkinson([1.0, 2.0], [1.0])
