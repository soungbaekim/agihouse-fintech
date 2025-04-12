# Comprehensive Guide to the Finance Analyzer Makefile

This guide provides detailed instructions on using the Makefile to run the Finance Analyzer application. The Makefile simplifies common tasks by providing easy-to-remember commands that handle the underlying complexity.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Basic Commands](#basic-commands)
4. [Working with Custom Data](#working-with-custom-data)
5. [Viewing Reports](#viewing-reports)
6. [Maintenance Commands](#maintenance-commands)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

## Prerequisites

Before using the Makefile commands, ensure you have the following installed:

- **Make**: The build automation tool (usually pre-installed on macOS and Linux)
- **Python 3.8+**: The programming language runtime
- **Tesseract OCR**: Required for PDF parsing with images (optional, only needed for PDF statements)

To check if Make is installed:
```bash
make --version
```

## Getting Started

### Viewing Available Commands

To see all available commands in the Makefile:

```bash
make help
```

This will display a list of all targets with descriptions and usage examples.

### Setting Up the Environment

The first step is to set up the Python virtual environment and install all dependencies:

```bash
make setup
```

This command:
1. Creates a virtual environment in the `venv` directory
2. Upgrades pip, setuptools, and wheel
3. Installs all required dependencies from `requirements.txt`

Wait for the setup to complete before running other commands. This may take a few minutes depending on your internet connection.

## Basic Commands

### Running with Sample Data

To test the application with the included sample data:

```bash
make run-sample
```

This command:
1. Uses the sample statement file (`data/sample_statement.csv`)
2. Analyzes the transactions and generates spending patterns
3. Creates savings and investment recommendations
4. Generates an HTML report (`finance_report.html`)

### Running in Interactive Mode

To use the interactive command-line interface:

```bash
make run-interactive
```

This launches a menu-driven interface where you can:
- Load bank statements
- View transaction summaries
- Analyze spending patterns
- Get savings recommendations
- Get investment recommendations
- Generate reports

Navigate the menu by entering the number corresponding to your choice.

## Working with Custom Data

### Analyzing Your Own Statement

To analyze your own bank statement:

```bash
make run-custom STATEMENT=path/to/your/statement.csv
```

Replace `path/to/your/statement.csv` with the actual path to your statement file. The application supports CSV, Excel (.xlsx, .xls), and PDF files.

### Using Custom Category Mappings

To use your own statement with the included category mapping:

```bash
make run-categories STATEMENT=path/to/your/statement.csv
```

This command uses the custom category mapping file (`data/category_mapping.json`) to categorize your transactions.

## Viewing Reports

### Opening the Generated Report

After running an analysis, open the generated report in your default browser:

```bash
make open-report
```

This command will open `finance_report.html` in your default web browser.

## Maintenance Commands

### Cleaning Generated Files

To remove generated files and Python cache directories:

```bash
make clean
```

This removes:
- Generated reports
- `__pycache__` directories
- Compiled Python files (.pyc, .pyo, .pyd)
- Other temporary files

### Complete Cleanup

To perform a complete cleanup including the virtual environment:

```bash
make clean-all
```

This removes everything that `make clean` does, plus the virtual environment directory. Use this when you want to start fresh or before updating the application.

## Troubleshooting

### Common Issues and Solutions

1. **Command not found: make**
   - Install make using your package manager:
     - macOS: `brew install make`
     - Ubuntu/Debian: `sudo apt install make`
     - Windows: Install Make through [Chocolatey](https://chocolatey.org/): `choco install make`

2. **Python version issues**
   - If you encounter compatibility problems, ensure you're using Python 3.8 or newer
   - You can specify a different Python interpreter by editing the `PYTHON` variable in the Makefile

3. **Dependency installation failures**
   - Try running: `make clean-all` followed by `make setup`
   - If specific packages fail, you may need to install system dependencies for them

4. **File not found errors**
   - Ensure you're providing the correct path to your statement file
   - Use absolute paths if relative paths aren't working

## Advanced Usage

### Modifying the Makefile

You can customize the Makefile for your specific needs:

1. **Changing default values**
   - Edit the variables at the top of the Makefile:
     ```make
     PYTHON = python3  # Change Python interpreter
     OUTPUT_REPORT = my_report.html  # Change default report name
     ```

2. **Adding new targets**
   - Add your own custom targets at the end of the file:
     ```make
     .PHONY: my-custom-target
     my-custom-target:
         @echo "Running my custom command..."
         $(VENV_PYTHON) my_script.py
     ```

### Running Multiple Commands

You can chain multiple make commands together:

```bash
make clean && make setup && make run-sample
```

This will clean the project, set up the environment, and run the analysis with sample data in sequence.

### Using Environment Variables

You can use environment variables with make commands:

```bash
OUTPUT=custom_report.html make run-sample
```

This will override the default output file name for this specific command.

---

This guide covers all aspects of using the Makefile for the Finance Analyzer application. For more information about the application itself, refer to the README.md file.
