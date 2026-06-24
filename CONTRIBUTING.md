# Contributing

Thanks for your interest in tickflow! Contributions of estimators, bug fixes,
and documentation are all welcome.

## Development setup

```bash
git clone https://github.com/davidy749/tickflow
cd tickflow
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Before opening a PR

```bash
ruff check .
mypy src
pytest --cov=tickflow
```

All three must pass — CI runs the same checks across Python 3.10–3.12.

## Adding an estimator

1. Put pure computation in the relevant module (`volatility.py`, `microstructure.py`, ...).
2. Validate inputs through the helpers in `_validation.py` so error messages stay consistent.
3. Add at least one test that checks the result against a known closed-form case.
4. Export it from `tickflow/__init__.py` and add a row to `docs/api-reference.md`.
5. Cite the source paper in the docstring.

## Style

- Type hints on all public functions; `mypy --strict` must pass.
- Keep functions free of global state.
- Docstrings explain *what* and *why*, not line-by-line *how*.
