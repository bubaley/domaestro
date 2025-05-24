ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif

# ----------- SHORT COMMANDS -----------

r: run ## short run runserver
t: test ## short run tests

# ----------- BASE COMMANDS -----------

run: ## run runserver
	uvicorn app.main:app --reload

lint: ## run lint
	pre-commit run --all-files --show-diff-on-failure

test: ## run tests
	pytest

help:
	@echo "Usage: make <target>"
	@awk 'BEGIN {FS = ":.*##"} /^[0-9a-zA-Z_-]+:.*?## / { printf "  * %-20s -%s\n", $$1, $$2 }' $(MAKEFILE_LIST)
