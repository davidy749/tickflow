import pandas as pd
import pytest

from tickflow import read_quotes, read_trades
from tickflow.exceptions import SchemaError


def test_read_trades_renames_and_sorts():
    raw = pd.DataFrame(
        {
            "ts": ["2025-01-02T09:30:01Z", "2025-01-02T09:30:00Z"],
            "px": [100.0, 99.5],
            "qty": [10, 5],
        }
    )
    out = read_trades(raw, rename={"ts": "timestamp", "px": "price", "qty": "size"})
    assert list(out.columns) == ["timestamp", "price", "size"]
    # rows should come out sorted by time
    assert out["price"].tolist() == [99.5, 100.0]


def test_read_trades_missing_column_raises():
    raw = pd.DataFrame({"timestamp": ["2025-01-02T09:30:00Z"], "price": [1.0]})
    with pytest.raises(SchemaError):
        read_trades(raw)


def test_read_quotes_schema(quotes):
    out = read_quotes(quotes)
    assert list(out.columns) == ["timestamp", "bid", "ask", "bid_size", "ask_size"]
    assert out["timestamp"].is_monotonic_increasing
