import numpy as np
import pandas as pd
import pytest

from tickflow.cli import main


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "tickflow" in capsys.readouterr().out


def test_cli_rv(tmp_path, capsys):
    prices = 100 * np.exp(np.cumsum(np.full(20, 0.001)))
    path = tmp_path / "p.csv"
    pd.DataFrame({"price": prices}).to_csv(path, index=False)
    rc = main(["rv", str(path), "--annualize", "252"])
    out = capsys.readouterr().out.strip()
    assert rc == 0
    assert float(out) > 0


def test_cli_bars(tmp_path, capsys, trades):
    path = tmp_path / "t.csv"
    trades.to_csv(path, index=False)
    rc = main(["bars", str(path), "--freq", "1min"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "open" in out and "close" in out
