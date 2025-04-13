<div align="center">

# 🌊 VIBECODED 🌊

</div>

<div align="center">
<h1>✨ Finance Analyzer ✨</h1>
<h3>Elevate your financial intelligence</h3>

![Vibecoded Badge](https://img.shields.io/badge/VIBECODED-✓-blueviolet?style=for-the-badge)
![Built With Love](https://img.shields.io/badge/Built_With-❤️-red?style=for-the-badge)
![Financial Freedom](https://img.shields.io/badge/Financial-Freedom-success?style=for-the-badge)

A smart banking statement parser and financial advisor that helps you analyze your spending habits, categorize transactions, and receive personalized savings recommendations.
</div>

## 📱 Screenshots

<div align="center">

### Homepage
![Homepage](/screenshots/homepage.png)
*The main entry point of the application*

### Dashboard Views
![Dashboard Overview](/screenshots/dashboard_1.png)
*The main dashboard provides a comprehensive view of your financial health*
![Spending Analysis](/screenshots/dashboard_2.png)
*A detailed breakdown of your spending patterns*
![Transaction Summary](/screenshots/dashboard_3.png)
*A summary of your recent transactions*

### Recommendations
![Savings Recommendations](/screenshots/recommendation_1.png)
*Personalized suggestions to reduce expenses and increase savings*
![AI-Powered Recommendations & Chat](/screenshots/recommendation_2.png)
*The recommendation page with AI chat interface for personalized financial advice*
![Recommendation Popup](/screenshots/recommendation_popup.png)
*Detailed view of a specific financial recommendation with actionable insights*

### Transactions
![Transaction Details](/screenshots/transaction.png)
*Detailed view of transaction history with filtering and categorization options*

</div>

## ✨ Features

- **Statement Parsing**: Support for various bank statement formats (PDF, CSV, Excel)
- **Spending Analysis**: Categorize and visualize your spending patterns
- **Savings Recommendations**: Get personalized suggestions to reduce expenses
- **Investment Ideas**: Receive basic investment recommendations based on your savings potential
- **AI-Powered Chat**: Get personalized financial advice through natural language

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
# Set up the environment
make setup

# Run with sample data
make run-sample

# Run in interactive mode
make run-interactive

# Run with your own statement file
make run-custom STATEMENT=path/to/your/statement.csv

# Start the web application
make run-webapp

# Restart the web application (kills any running instance first)
make restart-webapp

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

# Run the web application
python app.py
```

#### 3. AI Chat Configuration

The Finance Analyzer includes an AI-powered chat assistant that can provide personalized financial insights and recommendations based on your data. The chat assistant appears as a widget on every page of the web application.

##### Setting Up AI Chat

To use the AI-powered chat feature, you need to set up environment variables for the AI provider:

```bash
# Create a .env file in the project root with the following variables

# AI Provider Selection (openai or claude)
AI_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o  # Optional, defaults to gpt-4o

# Claude Configuration (if using Claude)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# CLAUDE_MODEL=claude-3-opus-20240229  # Optional
```

You can obtain API keys from:
- OpenAI: https://platform.openai.com/account/api-keys
- Anthropic Claude: https://www.anthropic.com/product

##### Using the AI Chat Assistant

The AI chat assistant is context-aware and provides different suggestions based on the page you're viewing:

1. **On the Transactions page**: Get insights about spending patterns, unusual transactions, and categorization suggestions
2. **On the Recommendations page**: Receive detailed explanations about savings recommendations and investment advice
3. **On Category Details pages**: Get specific insights about a particular spending category and optimization strategies

The chat widget can be minimized when not in use by clicking the minimize button in the top-right corner of the widget.

##### Restarting the Web Application

If you make changes to the AI configuration or encounter issues with the chat feature, you can restart the web application using:

```bash
make restart-webapp
```

This command will automatically kill any running instances of the application and start a fresh instance.

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