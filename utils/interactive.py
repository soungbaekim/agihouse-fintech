"""
Interactive Session - Interactive command-line interface for the Finance Analyzer
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from parsers.parser_factory import ParserFactory
from analysis.spending_analyzer import SpendingAnalyzer
from recommendations.savings_recommender import SavingsRecommender
from recommendations.investment_recommender import InvestmentRecommender
from utils.visualizer import Visualizer


class InteractiveSession:
    """Interactive command-line interface for the Finance Analyzer"""
    
    def __init__(self):
        """Initialize the interactive session"""
        self.transactions = []
        self.spending_analysis = None
        self.savings_recommendations = None
        self.investment_recommendations = None
        
        # Initialize components
        self.parser_factory = ParserFactory()
        self.analyzer = SpendingAnalyzer()
        self.savings_recommender = SavingsRecommender()
        self.investment_recommender = InvestmentRecommender()
        self.visualizer = Visualizer()
    
    def start(self):
        """Start the interactive session"""
        print("\n" + "=" * 60)
        print("Welcome to Finance Analyzer Interactive Mode")
        print("=" * 60)
        
        while True:
            print("\nWhat would you like to do?")
            print("1. Load a bank statement")
            print("2. View transaction summary")
            print("3. Analyze spending")
            print("4. Get savings recommendations")
            print("5. Get investment recommendations")
            print("6. Generate full report")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ")
            
            if choice == '1':
                self._load_statement()
            elif choice == '2':
                self._view_transaction_summary()
            elif choice == '3':
                self._analyze_spending()
            elif choice == '4':
                self._get_savings_recommendations()
            elif choice == '5':
                self._get_investment_recommendations()
            elif choice == '6':
                self._generate_report()
            elif choice == '7':
                print("\nThank you for using Finance Analyzer. Goodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")
    
    def _load_statement(self):
        """Load a bank statement file"""
        print("\n--- Load Bank Statement ---")
        
        # Get file path
        file_path = input("Enter the path to your bank statement file: ").strip()
        
        if not file_path:
            print("No file path provided. Returning to main menu.")
            return
        
        # Convert to Path object
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            print(f"Error: File not found: {file_path}")
            return
        
        try:
            # Get appropriate parser
            parser = self.parser_factory.get_parser(path)
            
            print(f"Parsing {path.name}...")
            self.transactions = parser.parse(path)
            
            print(f"Successfully parsed {len(self.transactions)} transactions.")
            
            # Reset analysis results
            self.spending_analysis = None
            self.savings_recommendations = None
            self.investment_recommendations = None
            
        except Exception as e:
            print(f"Error parsing file: {e}")
    
    def _view_transaction_summary(self):
        """View a summary of loaded transactions"""
        if not self.transactions:
            print("\nNo transactions loaded. Please load a bank statement first.")
            return
        
        print("\n--- Transaction Summary ---")
        print(f"Total transactions: {len(self.transactions)}")
        
        # Get date range
        dates = [t['date'] for t in self.transactions if 'date' in t]
        if dates:
            min_date = min(dates)
            max_date = max(dates)
            print(f"Date range: {min_date} to {max_date}")
        
        # Calculate total income and expenses
        income = sum(t['amount'] for t in self.transactions if t['amount'] > 0)
        expenses = sum(t['amount'] for t in self.transactions if t['amount'] < 0)
        
        print(f"Total income: ${income:.2f}")
        print(f"Total expenses: ${abs(expenses):.2f}")
        print(f"Net cash flow: ${income + expenses:.2f}")
        
        # Show sample transactions
        print("\nSample transactions:")
        for i, transaction in enumerate(sorted(self.transactions, key=lambda t: t['date'], reverse=True)[:5]):
            date = transaction['date']
            description = transaction['description']
            amount = transaction['amount']
            
            print(f"{i+1}. {date} - {description}: ${amount:.2f}")
        
        # Ask if user wants to see more transactions
        more = input("\nDo you want to see more transactions? (y/n): ").lower()
        if more == 'y':
            self._display_all_transactions()
    
    def _display_all_transactions(self):
        """Display all transactions in a paginated format"""
        sorted_transactions = sorted(self.transactions, key=lambda t: t['date'], reverse=True)
        page_size = 10
        total_pages = (len(sorted_transactions) + page_size - 1) // page_size
        current_page = 1
        
        while True:
            print(f"\n--- Transactions (Page {current_page}/{total_pages}) ---")
            
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, len(sorted_transactions))
            
            for i, transaction in enumerate(sorted_transactions[start_idx:end_idx], start=start_idx+1):
                date = transaction['date']
                description = transaction['description']
                amount = transaction['amount']
                category = transaction.get('category', 'Uncategorized')
                
                print(f"{i}. {date} - {description} (${amount:.2f}) - {category}")
            
            if total_pages <= 1:
                break
            
            print("\nNavigation: [n]ext page, [p]revious page, [q]uit")
            nav = input("Enter choice: ").lower()
            
            if nav == 'n' and current_page < total_pages:
                current_page += 1
            elif nav == 'p' and current_page > 1:
                current_page -= 1
            elif nav == 'q':
                break
            else:
                print("Invalid choice.")
    
    def _analyze_spending(self):
        """Analyze spending patterns"""
        if not self.transactions:
            print("\nNo transactions loaded. Please load a bank statement first.")
            return
        
        print("\n--- Analyzing Spending Patterns ---")
        
        try:
            # Perform analysis
            self.spending_analysis = self.analyzer.analyze(self.transactions)
            
            # Display summary
            print("\nSpending Analysis Results:")
            
            # Top spending categories
            print("\nTop Spending Categories:")
            for i, category in enumerate(self.spending_analysis['top_spending_categories'], start=1):
                name = category['category'].title()
                amount = category['amount']
                print(f"{i}. {name}: ${amount:.2f}")
            
            # Monthly spending trends
            print("\nMonthly Spending:")
            for month, categories in sorted(self.spending_analysis['monthly_spending'].items()):
                total = sum(categories.values())
                print(f"{month}: ${total:.2f}")
            
            # Recurring expenses
            if self.spending_analysis['recurring_expenses']:
                print("\nRecurring Expenses:")
                for i, expense in enumerate(self.spending_analysis['recurring_expenses'], start=1):
                    desc = expense['description']
                    amount = expense['average_amount']
                    freq = expense['frequency']
                    print(f"{i}. {desc} - ${amount:.2f} ({freq})")
            
            # Unusual spending
            if self.spending_analysis['unusual_spending']:
                print("\nUnusual Spending:")
                for month_data in self.spending_analysis['unusual_spending']:
                    month = month_data['month']
                    print(f"\nMonth: {month}")
                    
                    for category in month_data['unusual_categories']:
                        name = category['category'].title()
                        amount = category['amount']
                        avg = category['average']
                        pct = category['percent_increase']
                        print(f"  {name}: ${amount:.2f} (${avg:.2f} avg, {pct:.1f}% increase)")
            
            print("\nAnalysis complete!")
            
        except Exception as e:
            print(f"Error analyzing spending: {e}")
    
    def _get_savings_recommendations(self):
        """Get savings recommendations"""
        if not self.spending_analysis:
            if not self.transactions:
                print("\nNo transactions loaded. Please load a bank statement first.")
                return
            
            print("\nNo spending analysis available. Analyzing spending patterns first...")
            self.spending_analysis = self.analyzer.analyze(self.transactions)
        
        print("\n--- Savings Recommendations ---")
        
        try:
            # Generate recommendations
            self.savings_recommendations = self.savings_recommender.recommend(self.spending_analysis)
            
            # Display recommendations
            recommendations = self.savings_recommendations['recommendations']
            total_savings = self.savings_recommendations['total_potential_savings']
            
            print(f"\nTotal potential monthly savings: ${total_savings:.2f}")
            
            if recommendations:
                for i, rec in enumerate(recommendations, start=1):
                    category = rec['category'].title()
                    description = rec['description']
                    savings = rec['potential_savings']
                    
                    print(f"\n{i}. {category} - ${savings:.2f}")
                    print(f"   {description}")
            else:
                print("\nNo specific savings recommendations found.")
            
        except Exception as e:
            print(f"Error generating savings recommendations: {e}")
    
    def _get_investment_recommendations(self):
        """Get investment recommendations"""
        if not self.savings_recommendations:
            if not self.spending_analysis:
                if not self.transactions:
                    print("\nNo transactions loaded. Please load a bank statement first.")
                    return
                
                print("\nNo spending analysis available. Analyzing spending patterns first...")
                self.spending_analysis = self.analyzer.analyze(self.transactions)
            
            print("\nNo savings recommendations available. Generating savings recommendations first...")
            self.savings_recommendations = self.savings_recommender.recommend(self.spending_analysis)
        
        print("\n--- Investment Recommendations ---")
        
        try:
            # Generate recommendations
            self.investment_recommendations = self.investment_recommender.recommend(
                self.spending_analysis, self.savings_recommendations
            )
            
            # Display recommendations
            recommendations = self.investment_recommendations['recommendations']
            
            if recommendations:
                for i, rec in enumerate(recommendations, start=1):
                    title = rec['title']
                    description = rec['description']
                    potential_return = rec.get('potential_return', '')
                    
                    print(f"\n{i}. {title}")
                    print(f"   {description}")
                    if potential_return:
                        print(f"   Potential return: {potential_return}")
            else:
                print("\nNo specific investment recommendations found.")
            
        except Exception as e:
            print(f"Error generating investment recommendations: {e}")
    
    def _generate_report(self):
        """Generate a comprehensive financial report"""
        if not self.transactions:
            print("\nNo transactions loaded. Please load a bank statement first.")
            return
        
        print("\n--- Generating Financial Report ---")
        
        # Ensure we have all necessary analyses
        if not self.spending_analysis:
            print("Analyzing spending patterns...")
            self.spending_analysis = self.analyzer.analyze(self.transactions)
        
        if not self.savings_recommendations:
            print("Generating savings recommendations...")
            self.savings_recommendations = self.savings_recommender.recommend(self.spending_analysis)
        
        if not self.investment_recommendations:
            print("Generating investment recommendations...")
            self.investment_recommendations = self.investment_recommender.recommend(
                self.spending_analysis, self.savings_recommendations
            )
        
        # Get output path
        default_path = "finance_report.html"
        output_path = input(f"\nEnter output path for the report [{default_path}]: ").strip()
        
        if not output_path:
            output_path = default_path
        
        try:
            # Generate report
            print(f"\nGenerating report to {output_path}...")
            
            self.visualizer.generate_report(
                transactions=self.transactions,
                spending_analysis=self.spending_analysis,
                savings_recommendations=self.savings_recommendations,
                investment_recommendations=self.investment_recommendations,
                output_path=output_path
            )
            
            print(f"\nReport successfully generated to {os.path.abspath(output_path)}")
            
            # Ask if user wants to open the report
            open_report = input("\nDo you want to open the report now? (y/n): ").lower()
            if open_report == 'y':
                self._open_report(output_path)
            
        except Exception as e:
            print(f"Error generating report: {e}")
    
    def _open_report(self, report_path: str):
        """Open the generated report in the default browser"""
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
        except Exception as e:
            print(f"Error opening report: {e}")
            print(f"Please open the report manually at: {os.path.abspath(report_path)}")
