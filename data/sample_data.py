"""
Sample financial data for demonstration purposes
"""

import datetime
import random
from typing import List, Dict, Any


def generate_sample_transactions(num_transactions: int = 350) -> List[Dict[str, Any]]:
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
            'merchants': ['Whole Foods', 'Trader Joe\'s', 'Safeway', 'Kroger', 'Costco', 'Aldi', 'Publix', 'Wegmans', 
                         'Sprouts', 'H-E-B', 'Food Lion', 'Save-A-Lot', 'Albertsons', 'ShopRite', 'Meijer'],
            'amount_range': (15, 200),
            'frequency': 0.15  # Percentage of transactions in this category
        },
        'Dining': {
            'merchants': ['Starbucks', 'Chipotle', 'Subway', 'McDonald\'s', 'Local Restaurant', 'Pizza Hut', 'Olive Garden', 
                         'Panera Bread', 'Taco Bell', 'Burger King', 'Chick-fil-A', 'Dunkin\' Donuts', 'Wendy\'s', 
                         'Applebee\'s', 'Domino\'s Pizza', 'KFC', 'Panda Express', 'Five Guys', 'In-N-Out Burger'],
            'amount_range': (8, 75),
            'frequency': 0.18
        },
        'Shopping': {
            'merchants': ['Amazon', 'Target', 'Walmart', 'Best Buy', 'Apple Store', 'Macy\'s', 'Nordstrom', 'Kohl\'s', 
                         'Home Depot', 'Lowe\'s', 'IKEA', 'TJ Maxx', 'Marshalls', 'Gap', 'Old Navy', 'Sephora', 'Ulta Beauty', 
                         'Bed Bath & Beyond', 'Wayfair', 'Etsy', 'eBay', 'Newegg', 'Michaels', 'Hobby Lobby'],
            'amount_range': (10, 300),
            'frequency': 0.12
        },
        'Entertainment': {
            'merchants': ['Netflix', 'Spotify', 'Movie Theater', 'Steam', 'Disney+', 'Hulu', 'HBO Max', 'Amazon Prime', 
                         'Apple TV+', 'Paramount+', 'YouTube Premium', 'Peacock', 'Tidal', 'Apple Music', 'AMC Theaters', 
                         'Regal Cinemas', 'Dave & Buster\'s', 'Bowling Alley', 'Concert Tickets', 'Live Nation', 'Ticketmaster'],
            'amount_range': (10, 150),
            'frequency': 0.08
        },
        'Transportation': {
            'merchants': ['Uber', 'Lyft', 'Gas Station', 'Public Transit', 'Parking', 'Car Repair', 'Car Wash', 'Toll Roads', 
                         'Chevron', 'Shell', 'BP', 'Exxon', 'Jiffy Lube', 'Midas', 'Pep Boys', 'AutoZone', 'Enterprise Rent-A-Car', 
                         'Hertz', 'Avis', 'Amtrak', 'Airline Tickets', 'Taxi Service'],
            'amount_range': (5, 250),
            'frequency': 0.10
        },
        'Utilities': {
            'merchants': ['Electric Company', 'Water Service', 'Internet Provider', 'Phone Bill', 'Gas Bill', 'Waste Management', 
                         'Comcast', 'AT&T', 'Verizon', 'T-Mobile', 'Spectrum', 'Cox Communications', 'PG&E', 'ConEd', 
                         'Duke Energy', 'Xfinity', 'Dish Network', 'DirecTV', 'Solar City'],
            'amount_range': (40, 300),
            'frequency': 0.05
        },
        'Housing': {
            'merchants': ['Rent Payment', 'Mortgage', 'Home Insurance', 'Property Tax', 'HOA Fees', 'Apartment Management', 
                         'Rental Insurance', 'Security Deposit', 'Moving Service', 'Storage Unit', 'Furniture Rental', 
                         'Home Warranty', 'Lawn Service', 'Cleaning Service', 'Pest Control'],
            'amount_range': (800, 3500),
            'frequency': 0.04
        },
        'Healthcare': {
            'merchants': ['Doctor\'s Office', 'Hospital', 'Pharmacy', 'Dental Care', 'Vision Care', 'Health Insurance', 
                         'CVS', 'Walgreens', 'Rite Aid', 'Kaiser Permanente', 'UnitedHealthcare', 'Blue Cross', 'Aetna', 
                         'Cigna', 'Urgent Care', 'Laboratory Services', 'Mental Health Services', 'Physical Therapy'],
            'amount_range': (20, 500),
            'frequency': 0.06
        },
        'Education': {
            'merchants': ['Tuition Payment', 'Student Loans', 'Textbooks', 'School Supplies', 'Online Courses', 
                         'Tutoring Services', 'Educational Software', 'College Board', 'Pearson', 'McGraw-Hill', 
                         'Coursera', 'Udemy', 'edX', 'Chegg', 'Khan Academy', 'Skillshare', 'MasterClass'],
            'amount_range': (50, 1000),
            'frequency': 0.03
        },
        'Fitness': {
            'merchants': ['Gym Membership', 'Fitness Equipment', 'Workout Classes', 'Peloton', 'Planet Fitness', 
                         'LA Fitness', 'Equinox', 'Nike', 'Adidas', 'Under Armour', 'Lululemon', 'Athleta', 
                         'Supplement Store', 'Sports League Fees', 'Personal Trainer'],
            'amount_range': (15, 200),
            'frequency': 0.04
        },
        'Subscriptions': {
            'merchants': ['Amazon Prime', 'Microsoft 365', 'Adobe Creative Cloud', 'iCloud Storage', 'Google One', 
                         'Dropbox', 'LastPass', 'NordVPN', 'Grammarly', 'New York Times', 'Wall Street Journal', 
                         'Medium', 'Patreon', 'Substack', 'Audible', 'Kindle Unlimited', 'PlayStation Plus', 'Xbox Game Pass'],
            'amount_range': (5, 50),
            'frequency': 0.05
        },
        'Travel': {
            'merchants': ['Airbnb', 'Hotels.com', 'Expedia', 'Booking.com', 'Marriott', 'Hilton', 'Delta Airlines', 
                         'United Airlines', 'American Airlines', 'Southwest Airlines', 'Cruise Line', 'Travel Insurance', 
                         'Vacation Rental', 'Resort Fees', 'Travel Agency', 'VRBO', 'Travelocity', 'Kayak'],
            'amount_range': (100, 2000),
            'frequency': 0.04
        },
        'Income': {
            'merchants': ['Employer Payroll', 'Direct Deposit', 'Freelance Payment', 'Consulting Fee', 'Client Payment', 
                         'Investment Dividend', 'Tax Refund', 'Rental Income', 'Side Gig', 'Bonus Payment', 'Commission', 
                         'Royalty Payment', 'Profit Share', 'Rebate', 'Cash Back', 'Gift'],
            'amount_range': (1000, 8000),
            'frequency': 0.06
        }
    }
    
    # Generate random dates within the last 12 months
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=365)
    
    transactions = []
    
    # Calculate number of transactions per category based on frequency
    category_counts = {}
    remaining_transactions = num_transactions
    
    for category, info in categories.items():
        if category == 'Income':
            # Handle income separately to ensure regular income entries
            # Assume bi-weekly income (26 payments per year)
            category_counts[category] = min(26, int(num_transactions * info['frequency']))
        else:
            count = int(num_transactions * info['frequency'])
            category_counts[category] = count
        remaining_transactions -= category_counts[category]
    
    # Distribute any remaining transactions proportionally
    if remaining_transactions > 0:
        for category in sorted(categories.keys(), 
                              key=lambda k: categories[k]['frequency'], 
                              reverse=True):
            if remaining_transactions <= 0:
                break
            category_counts[category] += 1
            remaining_transactions -= 1
    
    # Generate transactions for each category
    for category, count in category_counts.items():
        category_info = categories[category]
        
        if category == 'Income':
            # Create regular income transactions (bi-weekly)
            payment_interval = 14  # days
            current_date = start_date
            
            while current_date <= end_date and len(transactions) < category_counts[category]:
                # Random merchant from income category
                merchant = random.choice(category_info['merchants'])
                
                # Random amount with slight variations
                base_amount = random.uniform(category_info['amount_range'][0], category_info['amount_range'][1])
                variation = random.uniform(0.95, 1.05)  # 5% variation
                amount = round(base_amount * variation, 2)
                
                # Create transaction
                transaction = {
                    'date': current_date,
                    'description': merchant,
                    'amount': amount,  # Income is positive
                    'category': category
                }
                
                transactions.append(transaction)
                
                # Move to next payment date
                current_date += datetime.timedelta(days=payment_interval)
                # Add a little randomness to the next payment date
                current_date += datetime.timedelta(days=random.randint(-1, 1))
        else:
            # Create expense transactions with realistic patterns
            for _ in range(count):
                # Random date
                days_offset = random.randint(0, (end_date - start_date).days)
                transaction_date = start_date + datetime.timedelta(days=days_offset)
                
                # Random merchant
                merchant = random.choice(category_info['merchants'])
                
                # Random amount
                min_amount, max_amount = category_info['amount_range']
                amount = round(random.uniform(min_amount, max_amount), 2)
                
                # Create recurring patterns for some categories
                if category in ['Utilities', 'Housing', 'Subscriptions']:
                    # Find similar transactions in the same month
                    same_month_same_merchant = [t for t in transactions 
                                              if t['category'] == category 
                                              and t['description'] == merchant
                                              and t['date'].month == transaction_date.month]
                    
                    if same_month_same_merchant:
                        # Skip duplicate monthly bills
                        continue
                
                # Create transaction
                transaction = {
                    'date': transaction_date,
                    'description': merchant,
                    'amount': -amount,  # Expenses are negative
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
    
    # Calculate category spending for recommendations
    category_spending = {}
    for t in transactions:
        if t['amount'] < 0:  # Only expenses
            category = t['category']
            if category not in category_spending:
                category_spending[category] = 0
            category_spending[category] += abs(t['amount'])
    
    # Generate sample savings recommendations based on actual spending
    savings_recommendations = []
    
    # Dining recommendation
    if 'Dining' in category_spending and category_spending['Dining'] > 300:
        dining_savings = round(category_spending['Dining'] * 0.25, 2)  # 25% potential savings
        savings_recommendations.append({
            'category': 'dining',
            'description': f'You spent ${round(category_spending["Dining"], 2)} on dining out, which is {round(category_spending["Dining"]/sum(category_spending.values())*100, 1)}% of your expenses. Consider cooking more meals at home.',
            'potential_savings': dining_savings
        })
    
    # Entertainment recommendation
    if 'Entertainment' in category_spending and category_spending['Entertainment'] > 100:
        entertainment_savings = round(category_spending['Entertainment'] * 0.3, 2)  # 30% potential savings
        savings_recommendations.append({
            'category': 'entertainment',
            'description': f'You have multiple streaming subscriptions totaling ${round(category_spending["Entertainment"], 2)}. Consider consolidating or rotating services to reduce monthly costs.',
            'potential_savings': entertainment_savings
        })
    
    # Shopping recommendation
    if 'Shopping' in category_spending and category_spending['Shopping'] > 200:
        shopping_savings = round(category_spending['Shopping'] * 0.2, 2)  # 20% potential savings
        savings_recommendations.append({
            'category': 'shopping',
            'description': f'Your shopping expenses of ${round(category_spending["Shopping"], 2)} could be reduced by implementing a 24-hour rule before making non-essential purchases.',
            'potential_savings': shopping_savings
        })
    
    # Transportation recommendation
    if 'Transportation' in category_spending and category_spending['Transportation'] > 150:
        transportation_savings = round(category_spending['Transportation'] * 0.15, 2)  # 15% potential savings
        savings_recommendations.append({
            'category': 'transportation',
            'description': f'You spent ${round(category_spending["Transportation"], 2)} on transportation. Consider using public transportation or carpooling to reduce these expenses.',
            'potential_savings': transportation_savings
        })
    
    # Groceries recommendation
    if 'Groceries' in category_spending and category_spending['Groceries'] > 400:
        groceries_savings = round(category_spending['Groceries'] * 0.12, 2)  # 12% potential savings
        savings_recommendations.append({
            'category': 'groceries',
            'description': f'Your grocery spending of ${round(category_spending["Groceries"], 2)} could be reduced by shopping at discount stores and buying store brands.',
            'potential_savings': groceries_savings
        })
    
    # Subscriptions recommendation
    if 'Subscriptions' in category_spending and category_spending['Subscriptions'] > 50:
        subscriptions_savings = round(category_spending['Subscriptions'] * 0.4, 2)  # 40% potential savings
        savings_recommendations.append({
            'category': 'subscriptions',
            'description': f'You spent ${round(category_spending["Subscriptions"], 2)} on various subscriptions. Review and cancel unused or underutilized services.',
            'potential_savings': subscriptions_savings
        })
    
    # Utilities recommendation
    if 'Utilities' in category_spending and category_spending['Utilities'] > 300:
        utilities_savings = round(category_spending['Utilities'] * 0.1, 2)  # 10% potential savings
        savings_recommendations.append({
            'category': 'utilities',
            'description': f'Your utility bills total ${round(category_spending["Utilities"], 2)}. Consider energy-efficient appliances and usage habits to reduce these costs.',
            'potential_savings': utilities_savings
        })
    
    # Fitness recommendation
    if 'Fitness' in category_spending and category_spending['Fitness'] > 100:
        fitness_savings = round(category_spending['Fitness'] * 0.25, 2)  # 25% potential savings
        savings_recommendations.append({
            'category': 'fitness',
            'description': f'You spent ${round(category_spending["Fitness"], 2)} on fitness. Consider home workouts or more affordable gym memberships.',
            'potential_savings': fitness_savings
        })
    
    # Ensure we have at least 5 recommendations
    if len(savings_recommendations) < 5:
        # Add generic recommendations to reach 5
        generic_recommendations = [
            {
                'category': 'dining',
                'description': 'Reducing dining out by cooking more meals at home could save you significant money each month.',
                'potential_savings': 85.00
            },
            {
                'category': 'entertainment',
                'description': 'Consider consolidating or rotating streaming services instead of subscribing to multiple platforms simultaneously.',
                'potential_savings': 25.00
            },
            {
                'category': 'shopping',
                'description': 'Implementing a 24-hour rule before making non-essential purchases can reduce impulse buying.',
                'potential_savings': 120.00
            },
            {
                'category': 'transportation',
                'description': 'Using public transportation or carpooling could significantly reduce your transportation costs.',
                'potential_savings': 65.00
            },
            {
                'category': 'groceries',
                'description': 'Shopping at discount grocery stores and buying store brands could reduce your grocery expenses.',
                'potential_savings': 50.00
            }
        ]
        
        # Add generic recommendations until we have at least 5
        for rec in generic_recommendations:
            if len(savings_recommendations) >= 5:
                break
            if not any(r['category'] == rec['category'] for r in savings_recommendations):
                savings_recommendations.append(rec)
    
    # Generate sample investment recommendations based on income and expenses
    total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
    total_expenses = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
    monthly_savings = (total_income - total_expenses) / 12  # Approximate monthly savings
    
    investment_recommendations = [
        {
            'title': 'Emergency Fund',
            'description': f'Build an emergency fund covering 3-6 months of expenses (${round(total_expenses/12*3, 2)} to ${round(total_expenses/12*6, 2)}) in a high-yield savings account.',
            'priority': 'High',
            'risk_level': 'Very Low',
            'potential_return': '3-4% APY'
        }
    ]
    
    # Add retirement recommendation if income is substantial
    if total_income > 30000:
        investment_recommendations.append({
            'title': 'Retirement Contributions',
            'description': f'Increase your 401(k) contributions to at least capture the full employer match. Consider contributing ${round(total_income * 0.15 / 12, 2)} monthly.',
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
        'description': 'Pay down high-interest debt before focusing on additional investments. This provides a guaranteed return equal to your interest rate.',
        'priority': 'High',
        'risk_level': 'Low',
        'potential_return': 'Equivalent to your interest rate'
    })
    
    # Add real estate recommendation for higher incomes
    if total_income > 60000:
        investment_recommendations.append({
            'title': 'Real Estate Investment',
            'description': 'Consider investing in real estate through REITs or rental properties for income and appreciation.',
            'priority': 'Medium',
            'risk_level': 'Medium to High',
            'potential_return': '5-12% annually'
        })
    
    # Add tax-advantaged accounts recommendation
    investment_recommendations.append({
        'title': 'Tax-Advantaged Accounts',
        'description': 'Maximize contributions to tax-advantaged accounts like IRAs, HSAs, or 529 plans depending on your goals.',
        'priority': 'Medium',
        'risk_level': 'Varies',
        'potential_return': 'Tax savings + investment returns'
    })
    
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
