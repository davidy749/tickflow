# Examples

Each script is self-contained and generates its own synthetic data, so you can
run them without downloading anything.

| Script | What it shows |
| --- | --- |
| `01_realized_volatility.py` | Realized variance, annualised vol, and a noise-robust kernel estimate |
| `02_information_bars.py` | Calendar-time vs. volume-driven bar sampling |
| `03_microstructure.py` | Recovering the bid-ask spread with the Roll model |
| `04_jump_detection.py` | Flagging an injected jump with the Lee-Mykland test |

```bash
python examples/01_realized_volatility.py
```
