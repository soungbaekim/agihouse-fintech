"""
Sample financial profiles for demonstration purposes
Each profile represents a different financial situation
"""

import datetime
import random
from typing import List, Dict, Any
from data.sample_data import generate_sample_transactions

def get_profile_names() -> List[str]:
    """
    Get a list of available financial profile names
    
    Returns:
        List of profile names
    """
    return [
        "young_professional",
        "family_budget",
        "student_finances",
        "retirement_planning",
        "high_income",
        "debt_reduction"
    ]

def get_profile_descriptions() -> Dict[str, str]:
    """
    Get descriptions for each financial profile
    
    Returns:
        Dictionary mapping profile names to descriptions
    """
    return {
        "young_professional": "A young professional with steady income, moderate expenses, and focus on building savings and investments.",
        "family_budget": "A family with multiple income sources, higher expenses including childcare and education, and focus on budgeting.",
        "student_finances": "A student with limited income, education expenses, and student loans, focusing on managing a tight budget.",
        "retirement_planning": "An older individual with stable income, lower expenses, and focus on retirement planning and investments.",
        "high_income": "A high-income individual with significant discretionary spending, investments, and tax planning needs.",
        "debt_reduction": "An individual focusing on paying down significant debt while managing necessary expenses."
    }

def generate_young_professional_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a young professional
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for young professional
    category_frequencies = {
        'Income': 0.06,
        'Housing': 0.04,
        'Dining': 0.20,
        'Entertainment': 0.12,
        'Shopping': 0.15,
        'Transportation': 0.10,
        'Utilities': 0.04,
        'Groceries': 0.10,
        'Fitness': 0.06,
        'Subscriptions': 0.08,
        'Travel': 0.05
    }
    
    # Generate transactions with young professional profile
    transactions = generate_sample_transactions(
        num_transactions=300,
        income_range=(4000, 6000),
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.15
    )
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_family_budget_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a family budget
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for family budget
    category_frequencies = {
        'Income': 0.06,
        'Housing': 0.06,
        'Dining': 0.12,
        'Entertainment': 0.08,
        'Shopping': 0.12,
        'Transportation': 0.10,
        'Utilities': 0.06,
        'Groceries': 0.18,
        'Healthcare': 0.08,
        'Education': 0.08,
        'Fitness': 0.03,
        'Subscriptions': 0.03
    }
    
    # Generate transactions with family budget profile
    transactions = generate_sample_transactions(
        num_transactions=350,
        income_range=(7000, 9000),
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.10
    )
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_student_finances_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for student finances
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for student finances
    category_frequencies = {
        'Income': 0.05,
        'Housing': 0.05,
        'Dining': 0.20,
        'Entertainment': 0.15,
        'Shopping': 0.10,
        'Transportation': 0.08,
        'Utilities': 0.04,
        'Groceries': 0.12,
        'Education': 0.15,
        'Subscriptions': 0.06
    }
    
    # Generate transactions with student finances profile
    transactions = generate_sample_transactions(
        num_transactions=250,
        income_range=(1500, 2500),
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.05
    )
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_retirement_planning_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for retirement planning
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for retirement planning
    category_frequencies = {
        'Income': 0.06,
        'Housing': 0.04,
        'Dining': 0.10,
        'Entertainment': 0.08,
        'Shopping': 0.08,
        'Transportation': 0.08,
        'Utilities': 0.05,
        'Groceries': 0.12,
        'Healthcare': 0.10,
        'Travel': 0.10,
        'Fitness': 0.04,
        'Subscriptions': 0.03,
        'Investments': 0.12
    }
    
    # Generate transactions with retirement planning profile
    transactions = generate_sample_transactions(
        num_transactions=300,
        income_range=(6000, 8000),
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.25
    )
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_high_income_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a high-income individual
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for high income
    category_frequencies = {
        'Income': 0.05,
        'Housing': 0.05,
        'Dining': 0.15,
        'Entertainment': 0.10,
        'Shopping': 0.15,
        'Transportation': 0.08,
        'Utilities': 0.03,
        'Groceries': 0.08,
        'Travel': 0.12,
        'Fitness': 0.05,
        'Subscriptions': 0.04,
        'Investments': 0.10
    }
    
    # Generate transactions with high income profile
    transactions = generate_sample_transactions(
        num_transactions=400,
        income_range=(12000, 18000),
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.30
    )
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_debt_reduction_profile() -> Dict[str, Any]:
    """
    Generate a financial profile focused on debt reduction
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for debt reduction
    category_frequencies = {
        'Income': 0.06,
        'Housing': 0.05,
        'Dining': 0.08,
        'Entertainment': 0.05,
        'Shopping': 0.06,
        'Transportation': 0.08,
        'Utilities': 0.05,
        'Groceries': 0.12,
        'Healthcare': 0.05,
        'Debt Payments': 0.30,
        'Subscriptions': 0.02,
        'Education': 0.08
    }
    
    # Generate transactions with debt reduction profile
    transactions = generate_sample_transactions(
        num_transactions=300,
        income_range=(4500, 6500),
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.08
    )
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def prepare_sample_data(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate metrics and prepare sample data from transactions
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Sample data dictionary with transactions, analysis, and recommendations
    """
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
    
    # Generate savings recommendations based on spending
    savings_recommendations = generate_savings_recommendations(spending_by_category)
    
    # Generate investment recommendations based on income and expenses
    investment_recommendations = generate_investment_recommendations(income, expenses)
    
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

def generate_savings_recommendations(category_spending: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Generate savings recommendations based on category spending
    
    Args:
        category_spending: Dictionary mapping categories to spending amounts
        
    Returns:
        List of savings recommendation dictionaries
    """
    savings_recommendations = []
    
    # Dining recommendation
    if 'Dining' in category_spending and category_spending['Dining'] > 300:
        dining_savings = round(category_spending['Dining'] * 0.25, 2)  # 25% potential savings
        savings_recommendations.append({
            'category': 'dining',
            'description': f'You spent ${round(category_spending["Dining"], 2)} on dining out. Consider cooking more meals at home.',
            'potential_savings': dining_savings
        })
    
    # Entertainment recommendation
    if 'Entertainment' in category_spending and category_spending['Entertainment'] > 100:
        entertainment_savings = round(category_spending['Entertainment'] * 0.3, 2)  # 30% potential savings
        savings_recommendations.append({
            'category': 'entertainment',
            'description': f'You have multiple streaming subscriptions totaling ${round(category_spending["Entertainment"], 2)}. Consider consolidating services.',
            'potential_savings': entertainment_savings
        })
    
    # Shopping recommendation
    if 'Shopping' in category_spending and category_spending['Shopping'] > 200:
        shopping_savings = round(category_spending['Shopping'] * 0.2, 2)  # 20% potential savings
        savings_recommendations.append({
            'category': 'shopping',
            'description': f'Your shopping expenses of ${round(category_spending["Shopping"], 2)} could be reduced with a 24-hour rule for purchases.',
            'potential_savings': shopping_savings
        })
    
    # Transportation recommendation
    if 'Transportation' in category_spending and category_spending['Transportation'] > 150:
        transportation_savings = round(category_spending['Transportation'] * 0.15, 2)  # 15% potential savings
        savings_recommendations.append({
            'category': 'transportation',
            'description': f'You spent ${round(category_spending["Transportation"], 2)} on transportation. Consider carpooling or public transit.',
            'potential_savings': transportation_savings
        })
    
    # Groceries recommendation
    if 'Groceries' in category_spending and category_spending['Groceries'] > 400:
        groceries_savings = round(category_spending['Groceries'] * 0.12, 2)  # 12% potential savings
        savings_recommendations.append({
            'category': 'groceries',
            'description': f'Your grocery spending of ${round(category_spending["Groceries"], 2)} could be reduced with store brands and sales.',
            'potential_savings': groceries_savings
        })
    
    # Subscriptions recommendation
    if 'Subscriptions' in category_spending and category_spending['Subscriptions'] > 50:
        subscriptions_savings = round(category_spending['Subscriptions'] * 0.4, 2)  # 40% potential savings
        savings_recommendations.append({
            'category': 'subscriptions',
            'description': f'You spent ${round(category_spending["Subscriptions"], 2)} on subscriptions. Review and cancel unused services.',
            'potential_savings': subscriptions_savings
        })
    
    # Utilities recommendation
    if 'Utilities' in category_spending and category_spending['Utilities'] > 300:
        utilities_savings = round(category_spending['Utilities'] * 0.1, 2)  # 10% potential savings
        savings_recommendations.append({
            'category': 'utilities',
            'description': f'Your utility bills total ${round(category_spending["Utilities"], 2)}. Consider energy-efficient appliances.',
            'potential_savings': utilities_savings
        })
    
    # Ensure we have at least 3 recommendations
    if len(savings_recommendations) < 3:
        # Add generic recommendations to reach 3
        generic_recommendations = [
            {
                'category': 'dining',
                'description': 'Reducing dining out by cooking more meals at home could save you significant money each month.',
                'potential_savings': 85.00
            },
            {
                'category': 'entertainment',
                'description': 'Consider consolidating streaming services instead of subscribing to multiple platforms simultaneously.',
                'potential_savings': 25.00
            },
            {
                'category': 'shopping',
                'description': 'Implementing a 24-hour rule before making non-essential purchases can reduce impulse buying.',
                'potential_savings': 120.00
            }
        ]
        
        # Add generic recommendations until we have at least 3
        for rec in generic_recommendations:
            if len(savings_recommendations) >= 3:
                break
            if not any(r['category'] == rec['category'] for r in savings_recommendations):
                savings_recommendations.append(rec)
    
    return savings_recommendations

def generate_investment_recommendations(income: float, expenses: float) -> List[Dict[str, Any]]:
    """
    Generate investment recommendations based on income and expenses
    
    Args:
        income: Total income
        expenses: Total expenses
        
    Returns:
        List of investment recommendation dictionaries
    """
    monthly_savings = (income - expenses) / 12  # Approximate monthly savings
    
    investment_recommendations = [
        {
            'title': 'Emergency Fund',
            'description': f'Build an emergency fund covering 3-6 months of expenses (${round(expenses/12*3, 2)} to ${round(expenses/12*6, 2)}).',
            'priority': 'High',
            'risk_level': 'Very Low',
            'potential_return': '3-4% APY'
        }
    ]
    
    # Add retirement recommendation if income is substantial
    if income > 30000:
        investment_recommendations.append({
            'title': 'Retirement Contributions',
            'description': f'Increase your 401(k) contributions to at least capture the full employer match (${round(income * 0.15 / 12, 2)} monthly).',
            'priority': 'High',
            'risk_level': 'Medium',
            'potential_return': '7-10% annually (long-term)'
        })
    
    # Add index fund recommendation if there's potential for investing
    if monthly_savings > 200:
        investment_recommendations.append({
            'title': 'Index Fund Investing',
            'description': f'Consider investing ${round(monthly_savings * 0.4, 2)} monthly in low-cost index funds for long-term growth.',
            'priority': 'Medium',
            'risk_level': 'Medium',
            'potential_return': '7-10% annually (long-term)'
        })
    
    # Add debt reduction recommendation
    investment_recommendations.append({
        'title': 'Debt Reduction',
        'description': 'Pay down high-interest debt before focusing on additional investments.',
        'priority': 'High',
        'risk_level': 'Low',
        'potential_return': 'Equivalent to your interest rate'
    })
    
    return investment_recommendations

def get_sample_profile(profile_name: str) -> Dict[str, Any]:
    """
    Get sample data for a specific financial profile
    
    Args:
        profile_name: Name of the financial profile
        
    Returns:
        Sample data dictionary for the specified profile
    """
    profile_generators = {
        "young_professional": generate_young_professional_profile,
        "family_budget": generate_family_budget_profile,
        "student_finances": generate_student_finances_profile,
        "retirement_planning": generate_retirement_planning_profile,
        "high_income": generate_high_income_profile,
        "debt_reduction": generate_debt_reduction_profile
    }
    
    if profile_name in profile_generators:
        return profile_generators[profile_name]()
    else:
        # Default to young professional if profile not found
        return generate_young_professional_profile()
