################################################################################
# Project Makefile — FAST, CLEAN, COLORED OUTPUT (uv)
################################################################################

UV  := uv
RUN := $(UV) run

# Supported Python minors (must match requires-python in pyproject.toml).
PY_VERSIONS := 3.12 3.13

GREEN  = \033[1;32m
RED    = \033[1;31m
YELLOW = \033[1;33m
BLUE   = \033[1;34m
RESET  = \033[0m

################################################################################
# INSTALLATION / ENV
################################################################################

install:
	@echo "$(BLUE)>>> Installing runtime environment...$(RESET)"
	$(UV) sync
	@echo "$(GREEN)>>> Installation complete!$(RESET)"

dev:
	@echo "$(BLUE)>>> Installing dev environment (all groups)...$(RESET)"
	$(UV) sync --all-groups
	@echo "$(BLUE)>>> Installing pre-commit hooks...$(RESET)"
	$(RUN) pre-commit install
	@echo "$(GREEN)>>> Dev setup complete!$(RESET)"

################################################################################
# PRE-COMMIT GATE
################################################################################

# Run the exact same checks as a commit would run, but on the whole repo.
check:
	@echo "$(BLUE)>>> Running pre-commit on all files...$(RESET)"
	$(RUN) pre-commit run --all-files --show-diff-on-failure
	@echo "$(GREEN)---------------------------------------------------$(RESET)"
	@echo "$(GREEN)   CHECK COMPLETE (matches commit hooks)$(RESET)"
	@echo "$(GREEN)---------------------------------------------------$(RESET)"

# Faster local iteration: run on staged files only.
check-fast:
	@echo "$(BLUE)>>> Running pre-commit on staged files...$(RESET)"
	$(RUN) pre-commit run --show-diff-on-failure

# Convenience: attempt auto-fixes (ruff/doc tools), then you run `make check`.
fix:
	@echo "$(BLUE)>>> Running pre-commit (auto-fix hooks may apply changes)...$(RESET)"
	$(RUN) pre-commit run --all-files --show-diff-on-failure || true
	@echo "$(YELLOW)>>> If changes were applied, re-run: make check$(RESET)"

################################################################################
# TESTING
################################################################################

test:
	@echo "$(BLUE)>>> Running tests...$(RESET)"
	$(RUN) pytest

test-cov:
	@echo "$(BLUE)>>> Running tests with coverage...$(RESET)"
	$(RUN) pytest --cov=ducklearn --cov-report=term-missing .
	@echo "$(GREEN)>>> Coverage report generated.$(RESET)"

################################################################################
# DOCUMENTATION
################################################################################

docs-serve:
	@echo "$(BLUE)>>> Serving documentation...$(RESET)"
	$(RUN) mkdocs serve

docs-build:
	@echo "$(BLUE)>>> Building documentation...$(RESET)"
	$(RUN) mkdocs build
	@echo "$(GREEN)>>> Build complete.$(RESET)"

docs-deploy:
	@echo "$(BLUE)>>> Deploying documentation...$(RESET)"
	$(RUN) mkdocs gh-deploy --force
	@echo "$(GREEN)>>> Deployment complete.$(RESET)"

################################################################################
# PRE-RELEASE / MATRIX (PER-PYTHON ENV, DOES NOT TOUCH MAIN .venv)
################################################################################

define RUN_IN_PY_ENV
	@echo "$(BLUE)>>> [py$(1)] Syncing env (.venv-py$(1))...$(RESET)"
	@UV_PROJECT_ENVIRONMENT=.venv-py$(1) $(UV) sync --all-groups --python $(1) --frozen

	@echo "$(BLUE)>>> [py$(1)] Running checks (ruff + mypy + pyright + docs + tests)...$(RESET)"
	@UV_PROJECT_ENVIRONMENT=.venv-py$(1) $(RUN) --python $(1) pre-commit run --all-files --show-diff-on-failure
	@UV_PROJECT_ENVIRONMENT=.venv-py$(1) $(RUN) --python $(1) pytest

	@echo "$(GREEN)>>> [py$(1)] Matrix checks OK.$(RESET)"
endef

prerelease:
	@echo "$(GREEN)===================================================$(RESET)"
	@echo "$(GREEN)   PRE-RELEASE MATRIX: $(PY_VERSIONS)$(RESET)"
	@echo "$(GREEN)===================================================$(RESET)"
	$(foreach v,$(PY_VERSIONS),$(call RUN_IN_PY_ENV,$(v)))
	@echo "$(GREEN)===================================================$(RESET)"
	@echo "$(GREEN)   ALL PRE-RELEASE CHECKS PASSED$(RESET)"
	@echo "$(GREEN)===================================================$(RESET)"

################################################################################
.PHONY: install dev check check-fast fix test test-cov docs-serve docs-build \
        docs-deploy prerelease
