# Marketing Commander developer commands.
# Requires: pdm (Python package manager), Docker (from Phase 3).

.PHONY: help setup lint format test check bootstrap-check build run clean migrate seed db-reset

help:
	@echo "Marketing Commander"
	@echo ""
	@echo "  make setup            Install development dependencies (pdm)"
	@echo "  make lint             Run ruff checks on scripts and tests"
	@echo "  make format           Apply ruff formatting"
	@echo "  make test             Run the test suite (documentation and repo validation)"
	@echo "  make check            Full local quality gate (what CI runs)"
	@echo "  make bootstrap-check  Verify the local environment bootstrap"
	@echo "  make migrate          Apply database migrations (alembic upgrade head)"
	@echo "  make build            Build service containers"
	@echo "  make run              Start the local stack (docker compose up --build)"
	@echo "  make clean            Remove caches and build output"

setup:
	pdm install
	cd apps/api && pdm install -G:all

lint:
	pdm run ruff check scripts tests apps services
	pdm run ruff format --check scripts tests apps services

format:
	pdm run ruff format scripts tests apps services
	pdm run ruff check --fix scripts tests apps services

test:
	pdm run pytest
	cd apps/api && pdm run pytest

check: lint test bootstrap-check
	@echo "All checks passed."

bootstrap-check:
	pdm run python scripts/bootstrap_check.py

migrate:
	cd apps/api && pdm run alembic upgrade head

build:
	docker compose build

run:
	docker compose up --build

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -not -path './.git/*' -exec rm -rf {} +

seed:
	cd apps/api && pdm run python -m app.seed

db-reset:
	cd apps/api && pdm run alembic downgrade base && pdm run alembic upgrade head
