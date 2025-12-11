"""Command-line interface for quick estimates from CSV files.

Examples
--------
Compute annualised realized volatility from a column of prices::

    tickflow rv prices.csv --column price --annualize 252

Resample a trades file into one-minute OHLCV bars::

    tickflow bars trades.csv --freq 1min
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

import pandas as pd

from . import __version__, bars, volatility


def _add_rv_parser(sub: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    p = sub.add_parser("rv", help="realized volatility from a price column")
    p.add_argument("path", help="CSV file with a price column")
    p.add_argument("--column", default="price", help="name of the price column")
    p.add_argument(
        "--annualize",
        type=float,
        default=None,
        help="periods per year to annualise by",
    )


def _add_bars_parser(sub: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    p = sub.add_parser("bars", help="resample a trades CSV into time bars")
    p.add_argument("path", help="CSV with timestamp, price, size columns")
    p.add_argument("--freq", default="1min", help="pandas offset alias")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tickflow", description=__doc__)
    parser.add_argument("--version", action="version", version=f"tickflow {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    _add_rv_parser(sub)
    _add_bars_parser(sub)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    df = pd.read_csv(args.path)

    if args.command == "rv":
        vol = volatility.realized_volatility(df[args.column], annualize=args.annualize)
        print(f"{vol:.8f}")
    elif args.command == "bars":
        out = bars.time_bars(df, freq=args.freq)
        out.to_csv(sys.stdout, index=False)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
