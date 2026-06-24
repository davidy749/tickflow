import numpy as np

from tickflow import (
    classify_trades,
    microprice,
    mid_price,
    order_flow_imbalance,
    weighted_mid,
)


def test_mid_price():
    assert mid_price([100.0], [102.0]).tolist() == [101.0]


def test_weighted_mid_leans_to_heavier_side():
    # heavy bid -> quote above the simple mid
    wm = weighted_mid([100.0], [102.0], [90.0], [10.0])
    assert wm[0] > 101.0


def test_microprice_matches_weighted_mid():
    args = ([100.0], [102.0], [30.0], [70.0])
    assert microprice(*args)[0] == weighted_mid(*args)[0]


def test_order_flow_imbalance_bounds():
    ofi = order_flow_imbalance([80.0, 0.0], [20.0, 100.0])
    assert ofi.tolist() == [0.6, -1.0]


def test_classify_trades_sign():
    price = np.array([101.5, 100.5])
    bid = np.array([100.0, 100.0])
    ask = np.array([101.0, 101.0])
    signs = classify_trades(price, bid, ask)
    assert signs.tolist() == [1.0, -1.0]
