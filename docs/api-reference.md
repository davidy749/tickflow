# API reference

All names below are importable directly from `tickflow`.

## io

| Function | Returns | Notes |
| --- | --- | --- |
| `read_trades(frame, rename=None)` | `DataFrame` | normalises to `timestamp, price, size` |
| `read_quotes(frame, rename=None)` | `DataFrame` | normalises to `timestamp, bid, ask, bid_size, ask_size` |

## bars

| Function | Returns | Notes |
| --- | --- | --- |
| `time_bars(trades, freq="1min")` | `DataFrame` | calendar-time OHLCV |
| `tick_bars(trades, n_ticks)` | `DataFrame` | one bar per N trades |
| `volume_bars(trades, volume)` | `DataFrame` | one bar per volume threshold |
| `dollar_bars(trades, dollars)` | `DataFrame` | one bar per notional threshold |

## volatility

| Function | Returns | Notes |
| --- | --- | --- |
| `realized_variance(prices)` | `float` | sum of squared log returns |
| `realized_volatility(prices, annualize=None)` | `float` | sqrt of RV |
| `bipower_variation(prices)` | `float` | jump-robust |
| `jump_variation(prices)` | `float` | `max(RV - BV, 0)` |
| `two_scale_rv(prices, slow_step=5)` | `float` | noise-corrected |
| `realized_kernel(prices, bandwidth=1)` | `float` | Bartlett kernel |
| `har_features(daily_rv, weekly=5, monthly=22)` | `DataFrame` | HAR regressors |

## microstructure

| Function | Returns |
| --- | --- |
| `roll_spread(prices)` | `SpreadEstimate` |
| `amihud_illiquidity(prices, volumes)` | `float` |
| `effective_spread(trade_price, mid_price, side)` | `float` |
| `kyle_lambda(signed_volume, price_change)` | `float` |

## orderbook

| Function | Returns |
| --- | --- |
| `mid_price(bid, ask)` | `ndarray` |
| `weighted_mid(bid, ask, bid_size, ask_size)` | `ndarray` |
| `microprice(bid, ask, bid_size, ask_size)` | `ndarray` |
| `order_flow_imbalance(bid_size, ask_size)` | `ndarray` |
| `classify_trades(price, bid, ask)` | `ndarray` |

## jumps / execution

| Function | Returns |
| --- | --- |
| `lee_mykland_jumps(prices, window=270, alpha=0.01)` | `list[JumpTestResult]` |
| `vwap(prices, volumes)` | `float` |
| `twap(prices)` | `float` |
| `implementation_shortfall(arrival_price, fill_prices, fill_sizes, side=1)` | `float` |
