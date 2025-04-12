# Finance Analyzer

A smart banking statement parser and financial advisor that helps you analyze your spending habits, categorize transactions, and receive personalized savings recommendations.

## Features

- **Statement Parsing**: Support for various bank statement formats (PDF, CSV, Excel)
- **Spending Analysis**: Categorize and visualize your spending patterns
- **Savings Recommendations**: Get personalized suggestions to reduce expenses
- **Investment Ideas**: Receive basic investment recommendations based on your savings potential

## Getting Started

### Prerequisites

- Python 3.8+
- Tesseract OCR (for PDF parsing with images)

### Setting Up Python Environment

It's recommended to use a virtual environment to manage dependencies for this project. Here's how to set it up:

#### Using venv (Python's built-in virtual environment)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Your terminal prompt should change to indicate the active environment
# (venv) $
```

#### Using conda (Alternative approach)

```bash
# Create a conda environment
conda create -n finance-analyzer python=3.8

# Activate the conda environment
conda activate finance-analyzer
```

#### Deactivating the Environment

When you're done working on the project, you can deactivate the virtual environment:

```bash
# For venv
deactivate

# For conda
# conda deactivate
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/finance-analyzer.git
cd finance-analyzer

# Activate your virtual environment (see above)

# Install dependencies
pip install -r requirements.txt
```

## Running the Finance Analyzer

This section provides a comprehensive guide on how to set up and run the Finance Analyzer application.

### Quick Start with Make

The project includes a Makefile that simplifies common tasks. Here are the most useful commands:

```bash
# Set up the environment and install dependencies
make setup

# Run with sample data
make run-sample

# Run in interactive mode
make run-interactive

# Run with your own statement file
make run-custom STATEMENT=path/to/your/statement.csv

# Open the generated report
make open-report
```

Run `make help` to see all available commands.

### Manual Setup and Usage

If you prefer not to use Make, you can run the commands directly:

#### 1. Setting Up the Environment

```bash
# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 2. Running the Application

```bash
# Run with a specific statement file
python main.py --statement path/to/your/statement.csv

# Use the included sample data
python main.py --statement data/sample_statement.csv

# Use interactive mode
python main.py --interactive

# Use custom category mapping
python main.py --statement path/to/your/statement.csv --categories data/category_mapping.json
```

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `--statement` | Path to your bank statement file (CSV, PDF, XLSX) |
| `--interactive` | Start in interactive mode |
| `--output` | Output file for the financial report (default: finance_report.html) |
| `--categories` | Path to custom category mapping file |

### Interactive Mode

Interactive mode provides a menu-driven interface for analyzing your financial data:

1. **Load a bank statement** - Import your financial data
2. **View transaction summary** - See a summary of your transactions
3. **Analyze spending** - Categorize and analyze your spending patterns
4. **Get savings recommendations** - Receive personalized savings suggestions
5. **Get investment recommendations** - Get investment advice based on your financial situation
6. **Generate full report** - Create a comprehensive HTML report

### Sample Data

The project includes sample data to help you test the application without using your personal financial information:

- `data/sample_statement.csv`: A sample bank statement with common transaction types
- `data/category_mapping.json`: A comprehensive category mapping file that can be customized

### Supported File Formats

The Finance Analyzer supports the following bank statement formats:

- **CSV files** (.csv) - Most banks offer statements in CSV format
- **Excel files** (.xlsx, .xls) - Spreadsheet format often used by financial institutions
- **PDF files** (.pdf) - The application can extract transaction data from PDF statements

### Customizing Categories

You can customize transaction categories by editing the `data/category_mapping.json` file or creating your own mapping file. The format is a JSON object where:
- Keys are category names
- Values are arrays of keywords that identify transactions belonging to that category

### Generated Reports

After analyzing your financial data, the application generates an HTML report (`finance_report.html` by default) that includes:

- Financial summary (income, expenses, net cash flow, savings rate)
- Spending analysis with visualizations
- Top spending categories and merchants
- Recurring expenses
- Unusual spending patterns
- Savings recommendations
- Investment suggestions

Open the report in any web browser to view your financial insights.

## Project Structure

- `main.py`: Entry point for the application
- `parsers/`: Statement parsing modules for different formats
- `analysis/`: Spending analysis and categorization logic
- `recommendations/`: Savings and investment recommendation engines
- `utils/`: Utility functions and helpers
- `config/`: Configuration files
- `data/`: Sample data and category mappings