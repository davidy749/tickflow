# Architecture

tickflow is a flat collection of pure functions grouped by concern. There is no
global state and no central object you have to construct — every estimator takes
arrays (or a normalised frame) and returns a number, array, or small dataclass.

```
                +-------------+
   raw CSV/df ->|    io       |  normalise columns -> canonical schema
                +------+------+
                       |
        +--------------+------------------------------+
        |              |              |               |
   +----v----+   +-----v-----+  +-----v------+  +-----v------+
   |  bars   |   | resample  |  | orderbook  |  | execution  |
   +----+----+   +-----+-----+  +-----+------+  +-----+------+
        |              |              |               |
        +------+-------+------+-------+               |
               |              |                       |
         +-----v-----+  +-----v-------+               |
         | volatility|  |microstructure|              |
         +-----+-----+  +-------------+               |
               |                                      |
         +-----v-----+                                |
         |   jumps    |  <-- shares bipower scaling   |
         +------------+                               |
```

## Layers

- **io** — the only place that knows about messy external column names. Everything
  downstream assumes the canonical names in `tickflow.types`.
- **bars / resample** — turn irregular ticks into something estimators can consume
  (OHLCV bars or a regular price grid).
- **volatility / microstructure / orderbook / execution / jumps** — leaf modules
  of pure estimators. They depend only on `_validation` and `types`.

## Why pure functions

High-frequency research is exploratory: people compose estimators in notebooks in
ways the author never anticipated. Free functions over plain arrays compose more
cleanly than a class hierarchy and are trivial to test in isolation.
