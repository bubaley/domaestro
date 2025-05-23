ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif

# ----------- SHORT COMMANDS -----------

r: run ## short run runserver

# ----------- BASE COMMANDS -----------

run: ## run runserver
	uvicorn app.main:app --reload

lint: ## run lint
	pre-commit run --all-files

help:
	@echo "Usage: make <target>"
	@awk 'BEGIN {FS = ":.*##"} /^[0-9a-zA-Z_-]+:.*?## / { printf "  * %-20s -%s\n", $$1, $$2 }' $(MAKEFILE_LIST)
