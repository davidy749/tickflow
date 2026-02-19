"""Numerical constants shared by several estimators."""

from __future__ import annotations

import numpy as np

#: ``E[|Z|]`` for a standard normal. Appears in bipower variation and in the
#: local-volatility scaling of the Lee-Mykland jump statistic.
MU1: float = float(np.sqrt(2.0 / np.pi))
