# tickflow

Tools for analysing high-frequency financial time series in Python.

tickflow is a small, dependency-light toolkit of estimators for tick-level data:
bar sampling, realized-volatility estimators (including noise-robust ones),
microstructure and liquidity metrics, order-flow utilities, jump detection, and
execution benchmarks. Everything is a plain function over NumPy arrays or a
normalised pandas frame — no framework to learn, easy to drop into a notebook.

## Install

```bash
pip install tickflow
```

## Quick start

```python
import pandas as pd
import tickflow as tf

trades = tf.read_trades(pd.read_csv("trades.csv"))

# information-driven bars
bars = tf.volume_bars(trades, volume=10_000)
close = bars["close"].to_numpy()

# realized volatility, annualised
print(tf.realized_volatility(close, annualize=252))

# noise-robust estimate at high sampling frequency
print(tf.realized_kernel(close, bandwidth=5))

# implied bid-ask spread from price reversals
print(tf.roll_spread(close))
```

## What's inside

- **Bars** — time, tick, volume and dollar bars (`time_bars`, `tick_bars`, `volume_bars`, `dollar_bars`)
- **Volatility** — realized variance/vol, bipower variation, two-scale RV, realized kernel, HAR features
- **Microstructure** — Roll spread, Amihud illiquidity, effective spread, Kyle's lambda
- **Order book** — mid, weighted mid, microprice, order-flow imbalance, Lee-Ready classification
- **Jumps** — Lee-Mykland test
- **Execution** — VWAP, TWAP, implementation shortfall
- **CLI** — `tickflow rv` and `tickflow bars` for quick CSV work

## Documentation

- [Usage guide](docs/usage.md)
- [Architecture](docs/architecture.md)
- [API reference](docs/api-reference.md)
- [Design notes](docs/design-notes.md)
- Runnable [examples](examples/)

## License

MIT — see [LICENSE](LICENSE).
