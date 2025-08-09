.PHONY: build test

build:
	@echo "Building Python package..."
	python -m build
	@echo "Uploading to PyPI..."
	python -m twine upload dist/*

test:
	@echo "Running tests..."
	python -m pytest