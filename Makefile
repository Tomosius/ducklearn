ENV_NAME = ducklearn

install:
	@echo ">>> Creating or updating conda environment..."
	conda env update -f environment.yml --prune

	@echo ">>> Activating environment and installing project..."
	conda run -n $(ENV_NAME) pip install -e .

	@echo ">>> Installing development tools..."
	conda run -n $(ENV_NAME) pre-commit install
	@echo ">>> Setup complete!"

sync:
	@echo ">>> Exporting environment to environment.yml..."
	conda env export --from-history > environment.yml
	@echo ">>> Sync complete!"