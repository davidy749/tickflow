# Design notes

A running log of decisions and the trade-offs behind them.

## Canonical schema in one place

Every loader funnels data into the names defined in `tickflow.types`. Estimators
never accept a `column=` argument for the core fields, which keeps their
signatures small. The cost is an explicit `read_trades(..., rename=...)` step up
front — worth it to avoid threading column names through every function.

## Information-driven bars are computed with a Python loop

`_threshold_groups` walks trades one at a time. A vectorised `cumsum`-and-modulo
trick is faster but subtly wrong: it cannot reset the running total exactly at a
bar close, so bar boundaries drift. Correctness wins here; the loop is still
fast enough for a trading day, and the hot path can be moved to numba later if a
profile says so.

## Noise correction is opt-in

Plain `realized_variance` is intentionally the naive sum of squared returns. It
is biased under microstructure noise, but it is also the textbook definition and
the right default for already-cleaned bar data. Users who sample very finely
reach for `realized_kernel` or `two_scale_rv` deliberately.

## Dataclasses for multi-field results

`roll_spread` returns a `SpreadEstimate` rather than a bare float so the number
of observations travels with the estimate. Jump tests return a `JumpTestResult`
per point for the same reason — the statistic and threshold are useful context.
