import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from tickflow._validation import as_float_array, log_returns
from tickflow.exceptions import SchemaError


def test_as_float_array_rejects_2d():
    with pytest.raises(SchemaError):
        as_float_array([[1.0, 2.0], [3.0, 4.0]])


def test_log_returns_rejects_non_positive():
    with pytest.raises(SchemaError):
        log_returns(np.array([1.0, -1.0, 2.0]))


@given(
    st.lists(
        st.floats(min_value=1.0, max_value=1e4, allow_nan=False),
        min_size=2,
        max_size=50,
    )
)
def test_log_returns_length(prices):
    arr = np.array(prices)
    assert log_returns(arr).size == arr.size - 1
