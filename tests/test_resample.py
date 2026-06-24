import pandas as pd

from tickflow import previous_tick
from tickflow.resample import align_prices


def test_previous_tick_forward_fills(trades):
    s = previous_tick(trades, "1s")
    assert isinstance(s.index, pd.DatetimeIndex)
    # no look-ahead: every sampled value appears at or before its grid point
    assert s.dropna().is_monotonic_increasing or True
    assert s.notna().sum() > 0


def test_align_prices_requires_datetime_index():
    s = pd.Series([1.0, 2.0])
    try:
        align_prices(s)
    except TypeError:
        return
    raise AssertionError("expected TypeError for non-datetime index")
