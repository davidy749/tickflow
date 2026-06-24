.PHONY: install lint type test cov all

install:
	pip install -e ".[dev]"

lint:
	ruff check .
	ruff format --check .

type:
	mypy src

test:
	pytest -q

cov:
	pytest --cov=tickflow --cov-report=term-missing

all: lint type cov
