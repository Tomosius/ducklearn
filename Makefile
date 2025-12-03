################################################################################
# Project Makefile
#
# Code Quality + Environment Sync + Editable Install + Testing
################################################################################

ENV_NAME = ducklearn

# Run tools inside conda environment
PYTHON        = conda run -n $(ENV_NAME) python
RUFF          = conda run -n $(ENV_NAME) ruff
PYLINT        = conda run -n $(ENV_NAME) pylint
PYDOCSTYLE    = conda run -n $(ENV_NAME) pydocstyle
VULTURE       = conda run -n $(ENV_NAME) vulture
DOCFORMATTER  = conda run -n $(ENV_NAME) docformatter
INTERROGATE   = conda run -n $(ENV_NAME) interrogate
PYROMA        = conda run -n $(ENV_NAME) pyroma
PYTEST        = conda run -n $(ENV_NAME) pytest
MUTMUT        = conda run -n $(ENV_NAME) mutmut


################################################################################
# INSTALLATION
################################################################################

install:
	@echo ">>> Creating / updating conda environment..."
	conda env update -f environment.yml --prune

	@echo ">>> Installing project (-e)..."
	conda run -n $(ENV_NAME) pip install -e .

	@echo ">>> Installing pre-commit hooks..."
	conda run -n $(ENV_NAME) pre-commit install

	@echo ">>> Installation complete!"


################################################################################
# SYNC
################################################################################

sync:
	@echo ">>> Exporting clean environment.yml..."
	conda env export --from-history > environment.yml

	@echo ">>> Extracting Python version from environment.yml..."
	@PY_VERSION=$$(grep -E 'python=([0-9]+\.[0-9]+)' environment.yml | sed 's/.*python=//'); \
	echo ">>> Python version detected: $$PY_VERSION"; \
	python scripts/sync_python_version.py $$PY_VERSION

	@echo ">>> Sync complete!"


################################################################################
# CODE QUALITY — Ruff
################################################################################

format:
	@echo ">>> Running ruff format..."
	$(RUFF) format .
	@echo ">>> Done."

lint:
	@echo ">>> Running ruff lint..."
	$(RUFF) check .
	@echo ">>> Done."

fix:
	@echo ">>> Running ruff fix..."
	$(RUFF) check --fix .
	@echo ">>> Done."


################################################################################
# CODE QUALITY — Deep tools
################################################################################

pylint:
	@echo ">>> Running pylint..."
	$(PYLINT) ducklearn || true

pydocstyle:
	@echo ">>> Checking docstring style..."
	$(PYDOCSTYLE) ducklearn || true

docfmt:
	@echo ">>> Formatting docstrings..."
	$(DOCFORMATTER) -r -i ducklearn
	@echo ">>> Docstrings formatted."

vulture:
	@echo ">>> Detecting dead code..."
	$(VULTURE) ducklearn || true

interrogate:
	@echo ">>> Checking docstring coverage..."
	$(INTERROGATE) -c pyproject.toml ducklearn || true

pyroma:
	@echo ">>> Checking project metadata quality..."
	$(PYROMA) . || true


################################################################################
# FULL QUALITY PASS (CI-like)
################################################################################

quality: format lint pylint pydocstyle vulture interrogate pyroma
	@echo "==================================================="
	@echo "   ALL QUALITY CHECKS COMPLETE"
	@echo "==================================================="

check: quality


###############################################################################
# TESTING
#
# test        - fast run: failed + new tests (quick feedback)
# test-cov    - full suite with coverage
# test-full   - full suite + coverage + mutation testing
###############################################################################

## make test
## Quick tests: only failed + newly added tests


test:
	@echo ">>> Cleaning leftover mutation artifacts..."
	@if [ -d "mutants" ]; then rm -rf mutants; fi
	@echo ">>> Running quick tests (failures + new tests)..."
	$(PYTEST) --lf --new-first || true
	@echo ">>> Quick test cycle complete."

## make test-cov
## Full test suite with coverage
test-cov:
	@echo ">>> Cleaning leftover mutation artifacts..."
	@if [ -d "mutants" ]; then rm -rf mutants; fi
	@echo ">>> Running full test suite with coverage..."
	$(PYTEST) --cov=ducklearn --cov-report=term-missing .
	@echo ">>> Coverage run complete."

## make test-full
## Full tests + coverage + mutation testing
test-full: test-cov
	@echo ">>> Starting mutation testing with mutmut..."
	$(MUTMUT) run || true
	@echo ">>> Mutation testing results:"
	$(MUTMUT) results || true
	@echo ">>> Full test suite complete."