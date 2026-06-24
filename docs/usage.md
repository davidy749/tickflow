# Usage

## Installation

```bash
pip install tickflow
```

## Loading data

Loaders normalise arbitrary column names into tickflow's canonical schema:

```python
import pandas as pd
import tickflow as tf

raw = pd.read_csv("trades.csv")
trades = tf.read_trades(raw, rename={"ts": "timestamp", "px": "price", "qty": "size"})
```

## Sampling bars

```python
minute = tf.time_bars(trades, "1min")
vbars = tf.volume_bars(trades, volume=10_000)
dbars = tf.dollar_bars(trades, dollars=1_000_000)
```

## Realized volatility

```python
prices = minute["close"].to_numpy()
tf.realized_variance(prices)
tf.realized_volatility(prices, annualize=252)   # annualised
tf.realized_kernel(prices, bandwidth=5)          # robust to noise
tf.two_scale_rv(prices, slow_step=5)
```

## Microstructure

```python
spread = tf.roll_spread(prices)        # SpreadEstimate(value=..., n_obs=...)
tf.amihud_illiquidity(prices, volumes)
```

## Command line

```bash
tickflow rv prices.csv --column close --annualize 252
tickflow bars trades.csv --freq 5min > bars.csv
```
