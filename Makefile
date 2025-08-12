.PHONY: build test lint format

build:
	@echo "Building Python package..."
	python -m build
	@echo "Uploading to PyPI..."
	python -m twine upload dist/*

test:
	@echo "Running tests..."
	python -m pytest

lint:
	@echo "Running lint checks..."
	ruff check --fix src tests

format:
	@echo "Formatting code..."
	ruff format src tests
