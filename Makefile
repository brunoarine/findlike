.PHONY: build test

build:
	@echo "Building Python package..."
	python build
	@echo "Uploading to PyPI..."
	python -m twine upload dist/*

test:
	@echo "Running tests..."
	pytest