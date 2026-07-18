# Marketing Commander developer commands.
# Requires: pdm (Python package manager), Docker (from Phase 3).

.PHONY: help setup lint format test bootstrap-check build run clean

help:
	@echo "Marketing Commander"
	@echo ""
	@echo "  make setup            Install development dependencies (pdm)"
	@echo "  make lint             Run ruff checks on scripts and tests"
	@echo "  make format           Apply ruff formatting"
	@echo "  make test             Run the test suite (documentation validation)"
	@echo "  make bootstrap-check  Verify the local environment bootstrap"
	@echo "  make build            Build service containers (available from Phase 3)"
	@echo "  make run              Start the local stack (available from Phase 3)"
	@echo "  make clean            Remove caches and build output"

setup:
	pdm install

lint:
	pdm run ruff check scripts tests
	pdm run ruff format --check scripts tests

format:
	pdm run ruff format scripts tests
	pdm run ruff check --fix scripts tests

test:
	pdm run pytest

bootstrap-check:
	pdm run python scripts/bootstrap_check.py

build:
	@if [ -f docker-compose.yml ]; then \
		docker compose build; \
	else \
		echo "ERROR: docker-compose.yml does not exist yet."; \
		echo "Service containers are delivered in Phase 3 (plan/plan.md)."; \
		exit 1; \
	fi

run:
	@if [ -f docker-compose.yml ]; then \
		docker compose up --build; \
	else \
		echo "ERROR: docker-compose.yml does not exist yet."; \
		echo "The runnable stack is delivered in Phase 3 (plan/plan.md)."; \
		exit 1; \
	fi

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -not -path './.git/*' -exec rm -rf {} +
