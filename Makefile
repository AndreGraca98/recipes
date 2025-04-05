.PHONY: env up down lint test clean deep-clean help
.DEFAULT_GOAL := help
.SILENT:

env: ## Create the environment file
	test -f .env || cp .env.template .env

up: env ## Start the container
	@echo "Starting the container..."
	docker compose up -d --build --remove-orphans

down: env ## Stop the container
	@echo "Stopping the container..."
	docker compose down --remove-orphans

lint: ## Lint the code
	@echo "Linting the code..."
	pdm run lint

test: ## Run the tests
	@echo "Running the tests..."
	pdm run test

clean: ## Clean the project
	@echo "Cleaning the project..."
	rm -rf .pytest_cache
	rm -rf .cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

deep-clean: clean ## Deep clean the project
	rm -rf .venv
	rm -rf docker-storage
	rm -f .env

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
