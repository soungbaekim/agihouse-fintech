"""
Visualizer - Generate visualizations and reports for financial data
"""

import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
import numpy as np


class Visualizer:
    """Generate visualizations and reports for financial data"""
    
    def __init__(self):
        """Initialize the visualizer"""
        # Set up styling
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12
        
        # Create color palette
        self.colors = sns.color_palette("viridis", 20)
    
    def generate_report(
        self,
        transactions: List[Dict[str, Any]],
        spending_analysis: Dict[str, Any],
        savings_recommendations: Dict[str, Any],
        investment_recommendations: Dict[str, Any],
        output_path: str = "finance_report.html"
    ) -> None:
        """
        Generate a comprehensive financial report
        
        Args:
            transactions: List of transaction dictionaries
            spending_analysis: Spending analysis results
            savings_recommendations: Savings recommendations
            investment_recommendations: Investment recommendations
            output_path: Path to save the report
        """
        # Create report directory
        report_dir = os.path.dirname(output_path)
        if report_dir and not os.path.exists(report_dir):
            os.makedirs(report_dir)
        
        # Generate visualizations
        charts = {}
        
        # 1. Spending by category pie chart
        charts['spending_by_category'] = self._create_spending_by_category_chart(
            spending_analysis['spending_by_category']
        )
        
        # 2. Monthly spending trend
        charts['monthly_spending'] = self._create_monthly_spending_chart(
            spending_analysis['monthly_spending']
        )
        
        # 3. Income vs. Expenses
        charts['income_vs_expenses'] = self._create_income_vs_expenses_chart(
            spending_analysis['income'],
            spending_analysis['expenses']
        )
        
        # 4. Top merchants bar chart
        charts['top_merchants'] = self._create_top_merchants_chart(
            spending_analysis['top_merchants']
        )
        
        # Generate HTML report
        html_content = self._generate_html_report(
            transactions=transactions,
            spending_analysis=spending_analysis,
            savings_recommendations=savings_recommendations,
            investment_recommendations=investment_recommendations,
            charts=charts
        )
        
        # Save the report
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    def _create_spending_by_category_chart(self, spending_by_category: Dict[str, float]) -> str:
        """Create a pie chart of spending by category"""
        # Create figure
        plt.figure(figsize=(10, 10))
        
        # Sort categories by amount
        sorted_categories = sorted(
            spending_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Separate small categories into "Other"
        threshold = sum(spending_by_category.values()) * 0.03  # 3% threshold
        main_categories = []
        other_amount = 0
        
        for category, amount in sorted_categories:
            if amount >= threshold:
                main_categories.append((category, amount))
            else:
                other_amount += amount
        
        if other_amount > 0:
            main_categories.append(('Other', other_amount))
        
        # Extract labels and values
        labels = [c[0].title() for c in main_categories]
        values = [c[1] for c in main_categories]
        
        # Create pie chart
        plt.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=self.colors[:len(labels)],
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        plt.axis('equal')
        plt.title('Spending by Category', fontsize=16, pad=20)
        
        # Save to temporary file
        chart_path = 'spending_by_category.png'
        plt.savefig(chart_path, bbox_inches='tight', dpi=100)
        plt.close()
        
        return chart_path
    
    def _create_monthly_spending_chart(self, monthly_spending: Dict[str, Dict[str, float]]) -> str:
        """Create a line chart of monthly spending trends"""
        # Convert to DataFrame for easier plotting
        months = sorted(monthly_spending.keys())
        
        if not months:
            # Return empty chart if no data
            plt.figure(figsize=(12, 8))
            plt.title('Monthly Spending Trends', fontsize=16)
            plt.xlabel('Month')
            plt.ylabel('Amount ($)')
            plt.text(0.5, 0.5, 'No monthly data available', 
                     horizontalalignment='center', verticalalignment='center',
                     transform=plt.gca().transAxes)
            
            chart_path = 'monthly_spending.png'
            plt.savefig(chart_path, bbox_inches='tight', dpi=100)
            plt.close()
            return chart_path
        
        # Get all unique categories
        all_categories = set()
        for month_data in monthly_spending.values():
            all_categories.update(month_data.keys())
        
        # Prepare data for plotting
        data = []
        for month in months:
            month_data = monthly_spending[month]
            row = {'month': month}
            
            for category in all_categories:
                row[category] = month_data.get(category, 0)
            
            data.append(row)
        
        df = pd.DataFrame(data)
        df = df.set_index('month')
        
        # Sort columns by total spending
        column_totals = df.sum().sort_values(ascending=False)
        top_categories = column_totals.head(8).index.tolist()  # Show top 8 categories
        
        # Sum the rest as "Other"
        if len(column_totals) > 8:
            df['Other'] = df[column_totals.iloc[8:].index].sum(axis=1)
            top_categories.append('Other')
        
        # Plot
        plt.figure(figsize=(14, 8))
        
        for i, category in enumerate(top_categories):
            plt.plot(
                df.index,
                df[category],
                marker='o',
                linewidth=2,
                label=category.title(),
                color=self.colors[i % len(self.colors)]
            )
        
        plt.title('Monthly Spending Trends', fontsize=16)
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Format x-axis labels
        plt.xticks(rotation=45)
        
        # Save to temporary file
        chart_path = 'monthly_spending.png'
        plt.savefig(chart_path, bbox_inches='tight', dpi=100)
        plt.close()
        
        return chart_path
    
    def _create_income_vs_expenses_chart(self, income: float, expenses: float) -> str:
        """Create a bar chart comparing income and expenses"""
        plt.figure(figsize=(10, 6))
        
        categories = ['Income', 'Expenses', 'Net']
        values = [income, expenses, income - expenses]
        colors = ['#2ecc71', '#e74c3c', '#3498db']  # Green, Red, Blue
        
        bars = plt.bar(categories, values, color=colors)
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'${height:,.2f}',
                ha='center',
                va='bottom',
                fontsize=12
            )
        
        plt.title('Income vs. Expenses', fontsize=16)
        plt.ylabel('Amount ($)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save to temporary file
        chart_path = 'income_vs_expenses.png'
        plt.savefig(chart_path, bbox_inches='tight', dpi=100)
        plt.close()
        
        return chart_path
    
    def _create_top_merchants_chart(self, top_merchants: List[Dict[str, Any]]) -> str:
        """Create a horizontal bar chart of top merchants by spending"""
        plt.figure(figsize=(12, 8))
        
        if not top_merchants:
            plt.title('Top Merchants by Spending', fontsize=16)
            plt.xlabel('Amount ($)')
            plt.text(0.5, 0.5, 'No merchant data available', 
                     horizontalalignment='center', verticalalignment='center',
                     transform=plt.gca().transAxes)
            
            chart_path = 'top_merchants.png'
            plt.savefig(chart_path, bbox_inches='tight', dpi=100)
            plt.close()
            return chart_path
        
        # Extract data
        merchants = [m['merchant'] for m in top_merchants]
        amounts = [m['amount'] for m in top_merchants]
        
        # Create horizontal bar chart
        bars = plt.barh(
            merchants,
            amounts,
            color=self.colors[:len(merchants)],
            height=0.6
        )
        
        # Add data labels
        for bar in bars:
            width = bar.get_width()
            plt.text(
                width + (width * 0.01),
                bar.get_y() + bar.get_height() / 2,
                f'${width:,.2f}',
                va='center',
                fontsize=12
            )
        
        plt.title('Top Merchants by Spending', fontsize=16)
        plt.xlabel('Amount ($)')
        plt.gca().invert_yaxis()  # Highest at the top
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save to temporary file
        chart_path = 'top_merchants.png'
        plt.savefig(chart_path, bbox_inches='tight', dpi=100)
        plt.close()
        
        return chart_path
    
    def _generate_html_report(
        self,
        transactions: List[Dict[str, Any]],
        spending_analysis: Dict[str, Any],
        savings_recommendations: Dict[str, Any],
        investment_recommendations: Dict[str, Any],
        charts: Dict[str, str]
    ) -> str:
        """Generate HTML report content"""
        # Get current date
        today = datetime.datetime.now().strftime('%B %d, %Y')
        
        # Calculate summary statistics
        total_transactions = len(transactions)
        date_range = self._get_date_range(transactions)
        
        # Format currency values
        income = spending_analysis['income']
        expenses = spending_analysis['expenses']
        net_cash_flow = spending_analysis['net_cash_flow']
        savings_rate = spending_analysis['savings_rate'] * 100  # Convert to percentage
        
        # Generate HTML
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Financial Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 1px solid #eee;
                }}
                .date {{
                    color: #7f8c8d;
                    font-size: 1.1em;
                }}
                .summary-box {{
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .summary-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                }}
                .summary-item {{
                    text-align: center;
                }}
                .summary-value {{
                    font-size: 1.8em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .summary-label {{
                    font-size: 0.9em;
                    color: #7f8c8d;
                }}
                .positive {{
                    color: #27ae60;
                }}
                .negative {{
                    color: #e74c3c;
                }}
                .chart-container {{
                    margin: 30px 0;
                    text-align: center;
                }}
                .chart {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .recommendations {{
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    padding: 20px;
                    margin: 30px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .recommendation-item {{
                    margin-bottom: 15px;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #eee;
                }}
                .recommendation-item:last-child {{
                    border-bottom: none;
                }}
                .savings-value {{
                    font-weight: bold;
                    color: #27ae60;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #7f8c8d;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Financial Analysis Report</h1>
                <p class="date">Generated on {today}</p>
                <p>Analysis period: {date_range}</p>
            </div>
            
            <div class="summary-box">
                <h2>Financial Summary</h2>
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-value">${income:,.2f}</div>
                        <div class="summary-label">Total Income</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${expenses:,.2f}</div>
                        <div class="summary-label">Total Expenses</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value {self._get_value_class(net_cash_flow)}">${net_cash_flow:,.2f}</div>
                        <div class="summary-label">Net Cash Flow</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value {self._get_value_class(savings_rate)}">{savings_rate:.1f}%</div>
                        <div class="summary-label">Savings Rate</div>
                    </div>
                </div>
            </div>
            
            <h2>Spending Analysis</h2>
            
            <div class="chart-container">
                <h3>Spending by Category</h3>
                <img src="{charts['spending_by_category']}" alt="Spending by Category" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>Monthly Spending Trends</h3>
                <img src="{charts['monthly_spending']}" alt="Monthly Spending Trends" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>Income vs. Expenses</h3>
                <img src="{charts['income_vs_expenses']}" alt="Income vs. Expenses" class="chart">
            </div>
            
            <div class="chart-container">
                <h3>Top Merchants by Spending</h3>
                <img src="{charts['top_merchants']}" alt="Top Merchants by Spending" class="chart">
            </div>
            
            <h2>Top Spending Categories</h2>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>% of Total Expenses</th>
                </tr>
                {self._generate_category_table_rows(spending_analysis['top_spending_categories'], expenses)}
            </table>
            
            <div class="recommendations">
                <h2>Savings Recommendations</h2>
                {self._generate_savings_recommendations_html(savings_recommendations)}
            </div>
            
            <div class="recommendations">
                <h2>Investment Recommendations</h2>
                {self._generate_investment_recommendations_html(investment_recommendations)}
            </div>
            
            <h2>Recurring Expenses</h2>
            {self._generate_recurring_expenses_html(spending_analysis.get('recurring_expenses', []))}
            
            <h2>Unusual Spending</h2>
            {self._generate_unusual_spending_html(spending_analysis.get('unusual_spending', []))}
            
            <div class="footer">
                <p>This report was generated by Finance Analyzer. The information provided is for informational purposes only and should not be considered financial advice.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _get_date_range(self, transactions: List[Dict[str, Any]]) -> str:
        """Get date range string from transactions"""
        if not transactions:
            return "No transactions"
        
        dates = [t['date'] for t in transactions if 'date' in t]
        if not dates:
            return "No date information"
        
        min_date = min(dates)
        max_date = max(dates)
        
        return f"{min_date.strftime('%B %d, %Y')} to {max_date.strftime('%B %d, %Y')}"
    
    def _get_value_class(self, value: float) -> str:
        """Get CSS class for value formatting"""
        if value > 0:
            return "positive"
        elif value < 0:
            return "negative"
        else:
            return ""
    
    def _generate_category_table_rows(self, top_categories: List[Dict[str, Any]], total_expenses: float) -> str:
        """Generate HTML table rows for top spending categories"""
        if not top_categories:
            return "<tr><td colspan='3'>No category data available</td></tr>"
        
        rows = ""
        for category in top_categories:
            category_name = category['category'].title()
            amount = category['amount']
            percentage = (amount / total_expenses) * 100 if total_expenses > 0 else 0
            
            rows += f"""
            <tr>
                <td>{category_name}</td>
                <td>${amount:,.2f}</td>
                <td>{percentage:.1f}%</td>
            </tr>
            """
        
        return rows
    
    def _generate_savings_recommendations_html(self, savings_recommendations: Dict[str, Any]) -> str:
        """Generate HTML for savings recommendations"""
        if not savings_recommendations or not savings_recommendations.get('recommendations'):
            return "<p>No savings recommendations available.</p>"
        
        recommendations = savings_recommendations['recommendations']
        total_potential_savings = savings_recommendations.get('total_potential_savings', 0)
        
        html = f"<p>Total potential monthly savings: <span class='savings-value'>${total_potential_savings:,.2f}</span></p>"
        
        for rec in recommendations:
            category = rec.get('category', 'Unknown').title()
            description = rec.get('description', '')
            potential_savings = rec.get('potential_savings', 0)
            
            html += f"""
            <div class="recommendation-item">
                <h3>{category}</h3>
                <p>{description}</p>
                <p>Potential savings: <span class="savings-value">${potential_savings:,.2f}</span></p>
            </div>
            """
        
        return html
    
    def _generate_investment_recommendations_html(self, investment_recommendations: Dict[str, Any]) -> str:
        """Generate HTML for investment recommendations"""
        if not investment_recommendations or not investment_recommendations.get('recommendations'):
            return "<p>No investment recommendations available.</p>"
        
        recommendations = investment_recommendations['recommendations']
        
        html = ""
        for rec in recommendations:
            title = rec.get('title', 'Investment Opportunity')
            description = rec.get('description', '')
            potential_return = rec.get('potential_return', '')
            
            html += f"""
            <div class="recommendation-item">
                <h3>{title}</h3>
                <p>{description}</p>
                {f'<p>Potential return: {potential_return}</p>' if potential_return else ''}
            </div>
            """
        
        return html
    
    def _generate_recurring_expenses_html(self, recurring_expenses: List[Dict[str, Any]]) -> str:
        """Generate HTML for recurring expenses"""
        if not recurring_expenses:
            return "<p>No recurring expenses identified.</p>"
        
        html = "<table>"
        html += """
        <tr>
            <th>Description</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Frequency</th>
        </tr>
        """
        
        for expense in recurring_expenses:
            description = expense.get('description', 'Unknown')
            category = expense.get('category', 'Unknown').title()
            amount = expense.get('average_amount', 0)
            frequency = expense.get('frequency', 'Unknown').title()
            
            html += f"""
            <tr>
                <td>{description}</td>
                <td>{category}</td>
                <td>${amount:,.2f}</td>
                <td>{frequency}</td>
            </tr>
            """
        
        html += "</table>"
        return html
    
    def _generate_unusual_spending_html(self, unusual_spending: List[Dict[str, Any]]) -> str:
        """Generate HTML for unusual spending"""
        if not unusual_spending:
            return "<p>No unusual spending patterns detected.</p>"
        
        html = ""
        for month_data in unusual_spending:
            month = month_data.get('month', 'Unknown')
            unusual_categories = month_data.get('unusual_categories', [])
            
            html += f"<h3>Month: {month}</h3>"
            html += "<table>"
            html += """
            <tr>
                <th>Category</th>
                <th>Amount</th>
                <th>Average</th>
                <th>Increase</th>
            </tr>
            """
            
            for category in unusual_categories:
                category_name = category.get('category', 'Unknown').title()
                amount = category.get('amount', 0)
                average = category.get('average', 0)
                percent_increase = category.get('percent_increase', 0)
                
                html += f"""
                <tr>
                    <td>{category_name}</td>
                    <td>${amount:,.2f}</td>
                    <td>${average:,.2f}</td>
                    <td>{percent_increase:.1f}%</td>
                </tr>
                """
            
            html += "</table>"
        
        return html
