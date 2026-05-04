from tickflow import dollar_bars, tick_bars, time_bars, volume_bars


def test_time_bars_have_ohlcv(trades):
    bars = time_bars(trades, "1min")
    assert {"open", "high", "low", "close", "volume", "n_trades"} <= set(bars.columns)
    assert (bars["high"] >= bars["low"]).all()
    assert (bars["volume"] > 0).all()


def test_tick_bars_count(trades):
    bars = tick_bars(trades, n_ticks=100)
    # 500 trades / 100 per bar -> 5 full bars (the last partial bar is kept)
    assert bars["n_trades"].iloc[:-1].eq(100).all()
    assert bars["n_trades"].sum() == len(trades)


def test_volume_bars_respect_threshold(trades):
    bars = volume_bars(trades, volume=500)
    # every completed bar should carry at least the threshold volume
    assert (bars["volume"].iloc[:-1] >= 500).all()


def test_dollar_bars_total_preserved(trades):
    bars = dollar_bars(trades, dollars=1_000_000)
    assert bars["n_trades"].sum() == len(trades)


def test_time_bars_handle_unsorted_input(trades):
    shuffled = trades.sample(frac=1.0, random_state=1).reset_index(drop=True)
    a = time_bars(trades, "1min").reset_index(drop=True)
    b = time_bars(shuffled, "1min").reset_index(drop=True)
    # open/close must match the chronological result regardless of input order
    assert a["open"].tolist() == b["open"].tolist()
    assert a["close"].tolist() == b["close"].tolist()
