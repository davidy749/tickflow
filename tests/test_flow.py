import numpy as np
import pytest

from tickflow import vpin
from tickflow.exceptions import InsufficientDataError


def test_vpin_balanced_flow_is_low():
    buy = np.full(100, 50.0)
    sell = np.full(100, 50.0)
    out = vpin(buy, sell, window=10)
    assert np.allclose(out, 0.0)


def test_vpin_one_sided_flow_is_high():
    buy = np.full(100, 100.0)
    sell = np.zeros(100)
    out = vpin(buy, sell, window=10)
    assert np.allclose(out, 1.0)


def test_vpin_output_length():
    buy = np.arange(1, 21, dtype=float)
    sell = np.arange(20, 0, -1, dtype=float)
    out = vpin(buy, sell, window=5)
    assert out.size == 20 - 5 + 1


def test_vpin_requires_window():
    with pytest.raises(InsufficientDataError):
        vpin([1.0, 2.0], [1.0, 2.0], window=10)
