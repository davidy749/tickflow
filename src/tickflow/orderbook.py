"""Top-of-book quote utilities: mids, microprice and order-flow imbalance."""

from __future__ import annotations

import numpy as np

from ._validation import as_float_array


def mid_price(bid: object, ask: object) -> np.ndarray:
    """Simple arithmetic mid, ``(bid + ask) / 2``."""
    b = as_float_array(bid, "bid")
    a = as_float_array(ask, "ask")
    return (b + a) / 2.0


def weighted_mid(
    bid: object, ask: object, bid_size: object, ask_size: object
) -> np.ndarray:
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
    return imbalance * a + (1.0 - imbalance) * b


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
