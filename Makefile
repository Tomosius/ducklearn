################################################################################
# Project Makefile
#
# This Makefile manages:
# - Conda environment creation & updates
# - Python version extraction & syncing across configs
# - Code formatting & linting with ruff
# - Automated tooling (pre-commit, project install)
#
# NOTE:
# - environment.yml is the single source of truth for Python version.
# - Running `make sync` updates pyproject.toml automatically.
################################################################################


# ==============================================================================
# ENVIRONMENT CONFIGURATION
# ==============================================================================

# Name of the conda environment for this project
ENV_NAME = ducklearn


# Aliases for running tools inside conda environment
PYTHON = conda run -n $(ENV_NAME) python
RUFF   = conda run -n $(ENV_NAME) ruff


# ==============================================================================
# INSTALLATION
# ==============================================================================

## make install
## Create or update the conda environment, install project, enable pre-commit
install:
	@echo ">>> Creating or updating conda environment..."
	conda env update -f environment.yml --prune

	@echo ">>> Installing project in editable mode..."
	conda run -n $(ENV_NAME) pip install -e .

	@echo ">>> Installing pre-commit hooks..."
	conda run -n $(ENV_NAME) pre-commit install

	@echo ">>> Installation complete!"


# ==============================================================================
# SYNC SYSTEM (Python version + config alignment)
# ==============================================================================

## make sync
## 1. Rebuild environment using environment.yml
## 2. Export cleaned environment.yml (from-history)
## 3. Sync Python version to pyproject.toml
sync:
	@echo ">>> Exporting minimal environment.yml (from-history)..."
	conda env export --from-history > environment.yml

	@echo ">>> Extracting Python version from environment.yml..."
	@PY_VERSION=$$(grep -E 'python=([0-9]+\.[0-9]+)' environment.yml | sed 's/.*python=//'); \
	echo ">>> Python version detected: $$PY_VERSION"; \
	python scripts/sync_python_version.py $$PY_VERSION

	@echo ">>> Sync complete!"


# ==============================================================================
# CODE QUALITY COMMANDS (Ruff)
# ==============================================================================

## make format
## Format all Python code using ruff formatter
format:
	@echo ">>> Formatting code with ruff..."
	$(RUFF) format .
	@echo ">>> Formatting complete."

## make lint
## Lint code without modifying files
lint:
	@echo ">>> Running ruff linter..."
	$(RUFF) check .
	@echo ">>> Linting complete."

## make fix
## Lint + autofix code
fix:
	@echo ">>> Running ruff with autofix..."
	$(RUFF) check --fix .
	@echo ">>> Autofix complete."

## make check
## Combined CI-style check (format validation + lint)
check: format lint
	@echo ">>> All checks passed!"