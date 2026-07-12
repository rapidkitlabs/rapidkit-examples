
# ==============================================
# RapidKit Project Automation
# ==============================================
.DEFAULT_GOAL := help
.RECIPEPREFIX := >

COMPOSE_BASE ?= deploy/compose/base.yml
COMPOSE_LOCAL ?= deploy/compose/local.yml
COMPOSE_PRODUCTION ?= deploy/compose/production.yml

POETRY ?= poetry
PYTHON ?= python3

.PHONY: help install setup dev start lint format test coverage typecheck build docker-build docker-up docker-down docker-logs docker-up-prod docker-down-prod docker-logs-prod ci

help: ## Show available commands
> @echo "RapidKit project commands:"
> @echo ""
> @grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
> awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
> @echo "[install] Installing dependencies"

> $(POETRY) install


setup: ## Install dependencies and prepare tooling
> @$(MAKE) install

> $(POETRY) run pre-commit install --install-hooks || true


dev: ## Run the application in development mode
> @echo "[dev] Starting development server"

> $(POETRY) run uvicorn src.main:app --reload --host 0.0.0.0 --port 8003


start: ## Run the application with production settings
> @echo "[start] Starting production server"

> $(POETRY) run uvicorn src.main:app --host 0.0.0.0 --port 8003


lint: ## Run static analysis checks

> $(POETRY) run ruff check src tests
> $(POETRY) run black --check src tests


format: ## Auto-format the codebase

> $(POETRY) run ruff check src tests --fix
> $(POETRY) run black src tests


test: ## Run unit tests

> $(POETRY) run pytest -q


coverage: ## Run tests with coverage reporting

> $(POETRY) run pytest --cov=src --cov-report=term-missing


typecheck: ## Run static type checks

> $(POETRY) run mypy src


build: ## Build distributable artifacts

> $(POETRY) run build


ci: ## Run the CI pipeline locally
> @echo "[ci] Running CI pipeline"
> $(MAKE) lint
> $(MAKE) typecheck
> $(MAKE) test

# ==============================================
# Docker helpers
# ==============================================

docker-build: ## Build all Docker images
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) build

docker-up: ## Start local Docker services
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) --profile local up --remove-orphans

docker-up-prod: ## Start production-like Docker services
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_PRODUCTION) --profile production up -d --remove-orphans

docker-down: ## Stop local Docker services
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) --profile local down

docker-down-prod: ## Stop production-like Docker services
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_PRODUCTION) --profile production down

docker-logs: ## Tail logs from local services
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_LOCAL) --profile local logs -f

docker-logs-prod: ## Tail logs from production-like services
> docker compose -f $(COMPOSE_BASE) -f $(COMPOSE_PRODUCTION) --profile production logs -f
