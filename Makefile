# Finance Analyzer Makefile
# This file contains recipes for common tasks

# Variables
PYTHON = python
VENV = venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip
SAMPLE_DATA = data/sample_statement.csv
CUSTOM_CATEGORIES = data/category_mapping.json
OUTPUT_REPORT = finance_report.html

# Default target
.PHONY: help
help:
	@echo "Finance Analyzer Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  setup           - Create virtual environment and install dependencies"
	@echo "  run-sample      - Run with sample data"
	@echo "  run-interactive - Run in interactive mode"
	@echo "  run-custom      - Run with custom statement file (set STATEMENT=path/to/file)"
	@echo "  run-categories  - Run with custom categories (set STATEMENT=path/to/file)"
	@echo "  clean           - Remove generated files and __pycache__ directories"
	@echo "  clean-all       - Remove generated files, __pycache__ directories, and virtual environment"
	@echo ""
	@echo "Examples:"
	@echo "  make run-custom STATEMENT=my_bank_statement.csv"
	@echo "  make run-categories STATEMENT=my_bank_statement.csv"

# Setup virtual environment and install dependencies
.PHONY: setup
setup:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(VENV_PIP) install --upgrade pip setuptools wheel
	$(VENV_PIP) install -r requirements.txt
	@echo "Setup complete! Use 'make run-sample' to test the application."

# Run with sample data
.PHONY: run-sample
run-sample:
	@echo "Running Finance Analyzer with sample data..."
	$(VENV_PYTHON) main.py --statement $(SAMPLE_DATA)
	@echo "Report generated: $(OUTPUT_REPORT)"

# Run in interactive mode
.PHONY: run-interactive
run-interactive:
	@echo "Running Finance Analyzer in interactive mode..."
	$(VENV_PYTHON) main.py --interactive

# Run with custom statement file
.PHONY: run-custom
run-custom:
	@if [ -z "$(STATEMENT)" ]; then \
		echo "Error: STATEMENT variable is required."; \
		echo "Usage: make run-custom STATEMENT=path/to/your/statement.csv"; \
		exit 1; \
	fi
	@echo "Running Finance Analyzer with custom statement: $(STATEMENT)"
	$(VENV_PYTHON) main.py --statement $(STATEMENT)
	@echo "Report generated: $(OUTPUT_REPORT)"

# Run with custom statement file and custom categories
.PHONY: run-categories
run-categories:
	@if [ -z "$(STATEMENT)" ]; then \
		echo "Error: STATEMENT variable is required."; \
		echo "Usage: make run-categories STATEMENT=path/to/your/statement.csv"; \
		exit 1; \
	fi
	@echo "Running Finance Analyzer with custom statement and categories..."
	$(VENV_PYTHON) main.py --statement $(STATEMENT) --categories $(CUSTOM_CATEGORIES)
	@echo "Report generated: $(OUTPUT_REPORT)"

# Open the generated report
.PHONY: open-report
open-report:
	@if [ ! -f "$(OUTPUT_REPORT)" ]; then \
		echo "Error: Report file not found: $(OUTPUT_REPORT)"; \
		echo "Run 'make run-sample' first to generate a report."; \
		exit 1; \
	fi
	@echo "Opening report: $(OUTPUT_REPORT)"
	open $(OUTPUT_REPORT)

# Clean generated files and __pycache__ directories
.PHONY: clean
clean:
	@echo "Cleaning generated files and __pycache__ directories..."
	rm -f $(OUTPUT_REPORT)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "Clean complete!"

# Clean all (including virtual environment)
.PHONY: clean-all
clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "Clean all complete!"
