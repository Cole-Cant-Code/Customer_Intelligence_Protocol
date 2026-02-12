.PHONY: install test lint format run validate-profiles

PYTHON ?= python3

install:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests scripts

format:
	ruff check --fix src tests scripts

run:
	$(PYTHON) -m cip_core.server.main

validate-profiles:
	$(PYTHON) scripts/validate_profiles.py profiles
