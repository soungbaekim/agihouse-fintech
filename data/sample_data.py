"""
Sample financial data for demonstration purposes
"""

import datetime
import random
from typing import List, Dict, Any


def generate_sample_transactions(num_transactions: int = 150) -> List[Dict[str, Any]]:
    """
    Generate sample transaction data for demonstration purposes
    
    Args:
        num_transactions: Number of transactions to generate
        
    Returns:
        List of transaction dictionaries
    """
    # Categories with sample merchants and amount ranges
    categories = {
        'Groceries': {
            'merchants': ['Whole Foods', 'Trader Joe\'s', 'Safeway', 'Kroger', 'Costco', 'Aldi'],
            'amount_range': (15, 200)
        },
        'Dining': {
            'merchants': ['Starbucks', 'Chipotle', 'Subway', 'McDonald\'s', 'Local Restaurant', 'Pizza Hut'],
            'amount_range': (8, 75)
        },
        'Shopping': {
            'merchants': ['Amazon', 'Target', 'Walmart', 'Best Buy', 'Apple Store', 'Macy\'s'],
            'amount_range': (10, 300)
        },
        'Entertainment': {
            'merchants': ['Netflix', 'Spotify', 'Movie Theater', 'Steam', 'Disney+', 'Hulu'],
            'amount_range': (10, 50)
        },
        'Transportation': {
            'merchants': ['Uber', 'Lyft', 'Gas Station', 'Public Transit', 'Parking', 'Car Repair'],
            'amount_range': (5, 100)
        },
        'Utilities': {
            'merchants': ['Electric Company', 'Water Service', 'Internet Provider', 'Phone Bill', 'Gas Bill'],
            'amount_range': (40, 200)
        },
        'Housing': {
            'merchants': ['Rent Payment', 'Mortgage', 'Home Insurance', 'Property Tax', 'HOA Fees'],
            'amount_range': (800, 2500)
        },
        'Income': {
            'merchants': ['Employer Payroll', 'Direct Deposit', 'Freelance Payment', 'Consulting Fee'],
            'amount_range': (1000, 5000)
        }
    }
    
    # Generate random dates within the last 6 months
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=180)
    
    transactions = []
    
    for _ in range(num_transactions):
        # Random date
        days_offset = random.randint(0, (end_date - start_date).days)
        transaction_date = start_date + datetime.timedelta(days=days_offset)
        
        # Random category
        category = random.choice(list(categories.keys()))
        category_info = categories[category]
        
        # Random merchant
        merchant = random.choice(category_info['merchants'])
        
        # Random amount
        min_amount, max_amount = category_info['amount_range']
        amount = round(random.uniform(min_amount, max_amount), 2)
        
        # Income is positive, expenses are negative
        if category == 'Income':
            amount_with_sign = amount
        else:
            amount_with_sign = -amount
        
        # Create transaction
        transaction = {
            'date': transaction_date,
            'description': merchant,
            'amount': amount_with_sign,
            'category': category
        }
        
        transactions.append(transaction)
    
    # Sort by date
    transactions.sort(key=lambda x: x['date'])
    
    return transactions


def get_sample_data() -> Dict[str, Any]:
    """
    Get a complete sample dataset for the Finance Analyzer
    
    Returns:
        Dictionary with transactions and analysis data
    """
    transactions = generate_sample_transactions()
    
    # Calculate basic metrics
    income = sum(t['amount'] for t in transactions if t['amount'] > 0)
    expenses = abs(sum(t['amount'] for t in transactions if t['amount'] < 0))
    net_cash_flow = income - expenses
    savings_rate = (net_cash_flow / income) * 100 if income > 0 else 0
    
    # Calculate spending by category
    spending_by_category = {}
    for t in transactions:
        if t['amount'] < 0:  # Only expenses
            category = t['category']
            if category not in spending_by_category:
                spending_by_category[category] = 0
            spending_by_category[category] += abs(t['amount'])
    
    # Calculate top spending categories
    top_categories = sorted(
        [{'category': k, 'amount': v} for k, v in spending_by_category.items()],
        key=lambda x: x['amount'],
        reverse=True
    )[:5]
    
    # Calculate monthly spending
    monthly_spending = {}
    for t in transactions:
        if t['amount'] < 0:  # Only expenses
            month_key = t['date'].strftime('%Y-%m')
            if month_key not in monthly_spending:
                monthly_spending[month_key] = {}
            
            category = t['category']
            if category not in monthly_spending[month_key]:
                monthly_spending[month_key][category] = 0
            
            monthly_spending[month_key][category] += abs(t['amount'])
    
    # Calculate top merchants
    merchant_spending = {}
    for t in transactions:
        if t['amount'] < 0:  # Only expenses
            merchant = t['description']
            if merchant not in merchant_spending:
                merchant_spending[merchant] = 0
            merchant_spending[merchant] += abs(t['amount'])
    
    top_merchants = sorted(
        [{'merchant': k, 'amount': v} for k, v in merchant_spending.items()],
        key=lambda x: x['amount'],
        reverse=True
    )[:10]
    
    # Generate sample savings recommendations
    savings_recommendations = [
        {
            'category': 'dining',
            'description': 'You spent $345 on dining out this month, which is 28% higher than your average. Consider cooking more meals at home.',
            'potential_savings': 85.00
        },
        {
            'category': 'entertainment',
            'description': 'You have multiple streaming subscriptions. Consider consolidating or rotating services to reduce monthly costs.',
            'potential_savings': 25.00
        },
        {
            'category': 'shopping',
            'description': 'Your online shopping increased by 35% this month. Try implementing a 24-hour rule before making non-essential purchases.',
            'potential_savings': 120.00
        },
        {
            'category': 'transportation',
            'description': 'Consider using public transportation or carpooling to reduce your transportation expenses.',
            'potential_savings': 65.00
        },
        {
            'category': 'groceries',
            'description': 'Shopping at discount grocery stores and buying store brands could reduce your grocery bill.',
            'potential_savings': 50.00
        }
    ]
    
    # Generate sample investment recommendations
    investment_recommendations = [
        {
            'title': 'Emergency Fund',
            'description': 'Build an emergency fund covering 3-6 months of expenses in a high-yield savings account.',
            'priority': 'High',
            'risk_level': 'Very Low',
            'potential_return': '1-2% APY'
        },
        {
            'title': 'Retirement Contributions',
            'description': 'Increase your 401(k) contributions to at least capture the full employer match.',
            'priority': 'High',
            'risk_level': 'Medium',
            'potential_return': '7-10% annually (long-term)'
        },
        {
            'title': 'Index Fund Investing',
            'description': 'Consider investing in low-cost index funds for long-term growth.',
            'priority': 'Medium',
            'risk_level': 'Medium',
            'potential_return': '7-10% annually (long-term)'
        },
        {
            'title': 'Debt Reduction',
            'description': 'Pay down high-interest debt before focusing on additional investments.',
            'priority': 'High',
            'risk_level': 'Low',
            'potential_return': 'Equivalent to your interest rate'
        }
    ]
    
    # Combine all data
    sample_data = {
        'transactions': transactions,
        'analysis': {
            'income': income,
            'expenses': expenses,
            'net_cash_flow': net_cash_flow,
            'savings_rate': savings_rate,
            'spending_by_category': spending_by_category,
            'top_spending_categories': top_categories,
            'monthly_spending': monthly_spending,
            'top_merchants': top_merchants,
            'total_potential_savings': sum(r['potential_savings'] for r in savings_recommendations)
        },
        'recommendations': {
            'savings': savings_recommendations,
            'investment': investment_recommendations
        }
    }
    
    return sample_data
