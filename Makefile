SHELL := /bin/bash

BACKEND_DIR := backend
FRONTEND_DIR := frontend
COMPOSE := docker compose

# Host/port for local uvicorn run
API_HOST ?= 127.0.0.1
API_PORT ?= 8000
BASE_URL := http://$(API_HOST):$(API_PORT)

.PHONY: help db-up db-down migrate api-run api-up api-stop fe-dev fe-build fe-up fe-stop demo test backend-venv

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | sort | awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

db-up: ## Start PostgreSQL via Docker Compose
	cd $(BACKEND_DIR) && $(COMPOSE) up -d postgres

db-down: ## Stop PostgreSQL service
	cd $(BACKEND_DIR) && $(COMPOSE) stop postgres

migrate: ## Apply Alembic migrations
	cd $(BACKEND_DIR) && alembic upgrade head

api-run: ## Run FastAPI locally with uvicorn (reload)
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload --host $(API_HOST) --port $(API_PORT)

api-up: ## Start API in Docker (profile=api)
	cd $(BACKEND_DIR) && $(COMPOSE) --profile api up -d app

api-stop: ## Stop API container
	cd $(BACKEND_DIR) && $(COMPOSE) stop app

fe-dev: ## Start frontend dev server locally (Vite)
	cd $(FRONTEND_DIR) && npm install && npm run dev

fe-build: ## Build frontend (Vite production build)
	cd $(FRONTEND_DIR) && npm install && npm run build

fe-up: ## Start frontend in Docker (profile=web)
	cd $(BACKEND_DIR) && $(COMPOSE) --profile web up -d frontend

fe-stop: ## Stop frontend container
	cd $(BACKEND_DIR) && $(COMPOSE) stop frontend

demo: ## Run demo auth script against BASE_URL (register -> login -> me)
	cd $(BACKEND_DIR) && BASE_URL=$(BASE_URL) ./scripts/demo_auth.sh

test: ## Run backend tests
	cd $(BACKEND_DIR) && if [ -x .venv/bin/pytest ]; then .venv/bin/pytest -q; else pytest -q; fi

backend-venv: ## Create venv and install backend deps
	cd $(BACKEND_DIR) \
	&& python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& python -m pip install -U pip \
	&& python -m pip install -r requirements.txt
