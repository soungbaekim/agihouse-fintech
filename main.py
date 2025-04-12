#!/usr/bin/env python3
"""
Finance Analyzer - Main Entry Point
A tool to parse banking statements, analyze spending, and provide savings recommendations.
"""

import argparse
import os
import sys
from pathlib import Path

# Import core modules
from parsers.parser_factory import ParserFactory
from analysis.spending_analyzer import SpendingAnalyzer
from recommendations.savings_recommender import SavingsRecommender
from recommendations.investment_recommender import InvestmentRecommender
from utils.interactive import InteractiveSession
from utils.visualizer import Visualizer

def main():
    """Main entry point for the Finance Analyzer application."""
    parser = argparse.ArgumentParser(
        description="Finance Analyzer - Parse bank statements and get financial insights"
    )
    
    # Define command-line arguments
    parser.add_argument(
        "--statement", 
        type=str, 
        help="Path to your bank statement file (CSV, PDF, XLSX)"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Start in interactive mode"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="finance_report.html",
        help="Output file for the financial report (default: finance_report.html)"
    )
    parser.add_argument(
        "--categories", 
        type=str, 
        help="Path to custom category mapping file"
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        session = InteractiveSession()
        session.start()
        return
    
    # Check if statement file was provided
    if not args.statement:
        print("Error: Please provide a bank statement file or use interactive mode.")
        parser.print_help()
        sys.exit(1)
    
    # Check if file exists
    statement_path = Path(args.statement)
    if not statement_path.exists():
        print(f"Error: File not found: {args.statement}")
        sys.exit(1)
    
    # Process the statement
    try:
        # 1. Parse the statement
        parser_factory = ParserFactory()
        statement_parser = parser_factory.get_parser(statement_path)
        transactions = statement_parser.parse(statement_path)
        
        print(f"Successfully parsed {len(transactions)} transactions.")
        
        # 2. Analyze spending
        analyzer = SpendingAnalyzer(custom_categories_path=args.categories)
        spending_analysis = analyzer.analyze(transactions)
        
        # 3. Generate recommendations
        savings_recommender = SavingsRecommender()
        savings_recommendations = savings_recommender.recommend(spending_analysis)
        
        investment_recommender = InvestmentRecommender()
        investment_recommendations = investment_recommender.recommend(
            spending_analysis, savings_recommendations
        )
        
        # 4. Visualize results
        visualizer = Visualizer()
        visualizer.generate_report(
            transactions=transactions,
            spending_analysis=spending_analysis,
            savings_recommendations=savings_recommendations,
            investment_recommendations=investment_recommendations,
            output_path=args.output
        )
        
        print(f"Financial analysis complete! Report saved to {args.output}")
        
    except Exception as e:
        print(f"Error processing statement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
