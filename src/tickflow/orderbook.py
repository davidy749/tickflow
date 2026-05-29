"""Top-of-book quote utilities: mids, microprice and order-flow imbalance."""

from __future__ import annotations

from typing import cast

import numpy as np

from ._validation import as_float_array


def mid_price(bid: object, ask: object) -> np.ndarray:
    """Simple arithmetic mid, ``(bid + ask) / 2``."""
    b = as_float_array(bid, "bid")
    a = as_float_array(ask, "ask")
    return cast(np.ndarray, (b + a) / 2.0)


def weighted_mid(bid: object, ask: object, bid_size: object, ask_size: object) -> np.ndarray:
    """Size-weighted mid that leans toward the side with more depth.

    Imbalance ``I = bid_size / (bid_size + ask_size)`` weights the *ask* price,
    so a heavy bid (large ``I``) pulls the quote up toward the ask.
    """
    b = as_float_array(bid, "bid")
    a = as_float_array(ask, "ask")
    bs = as_float_array(bid_size, "bid_size")
    as_ = as_float_array(ask_size, "ask_size")
    depth = bs + as_
    with np.errstate(divide="ignore", invalid="ignore"):
        imbalance = np.where(depth > 0, bs / depth, 0.5)
    return cast(np.ndarray, imbalance * a + (1.0 - imbalance) * b)


def order_flow_imbalance(bid_size: object, ask_size: object) -> np.ndarray:
    """Normalised depth imbalance in ``[-1, 1]``.

    ``(bid_size - ask_size) / (bid_size + ask_size)``; positive means more size
    resting on the bid than the ask.
    """
    bs = as_float_array(bid_size, "bid_size")
    as_ = as_float_array(ask_size, "ask_size")
    depth = bs + as_
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(depth > 0, (bs - as_) / depth, 0.0)


def microprice(bid: object, ask: object, bid_size: object, ask_size: object) -> np.ndarray:
    """Stoikov microprice.

    A single-step approximation of the microprice, this returns the size-
    weighted mid. It is exposed separately because it is the natural fair-value
    anchor for execution models, even though it coincides with
    :func:`weighted_mid` at the top of book.
    """
    return weighted_mid(bid, ask, bid_size, ask_size)


def classify_trades(price: object, bid: object, ask: object) -> np.ndarray:
    """Lee-Ready trade-sign classification.

    Returns ``+1`` for buyer-initiated and ``-1`` for seller-initiated trades by
    comparing each trade price to the prevailing mid; trades exactly at the mid
    fall back to the tick test on the price series.
    """
    p = as_float_array(price, "price")
    mid = mid_price(bid, ask)
    if p.size != mid.size:
        raise ValueError("price and quotes must be equal length")
    sign = np.sign(p - mid)
    # Tick test for trades sitting exactly on the mid.
    tick = np.sign(np.diff(p, prepend=p[0]))
    for i in range(sign.size):
        if sign[i] == 0:
            sign[i] = tick[i] if tick[i] != 0 else (sign[i - 1] if i else 1.0)
    return cast(np.ndarray, sign.astype(float))
