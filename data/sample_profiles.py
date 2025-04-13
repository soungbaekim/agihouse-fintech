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
        # Individual profiles
        "young_professional",
        "family_budget",
        "student_finances",
        "retirement_planning",
        "high_income",
        "debt_reduction",
        "freelancer",
        "travel_enthusiast",
        # Business/company profiles
        "small_business",
        "tech_startup",
        "restaurant_business",
        "retail_store"
    ]

def get_profile_descriptions() -> Dict[str, str]:
    """
    Get descriptions for each financial profile
    
    Returns:
        Dictionary mapping profile names to descriptions
    """
    return {
        # Individual profiles
        "young_professional": "A young professional with steady income, moderate expenses, and focus on building savings and investments.",
        "family_budget": "A family with multiple income sources, higher expenses including childcare and education, and focus on budgeting.",
        "student_finances": "A student with limited income, education expenses, and student loans, focusing on managing a tight budget.",
        "retirement_planning": "An older individual with stable income, lower expenses, and focus on retirement planning and investments.",
        "high_income": "A high-income individual with significant discretionary spending, investments, and tax planning needs.",
        "debt_reduction": "An individual focusing on paying down significant debt while managing necessary expenses.",
        "freelancer": "A freelance professional with irregular income patterns, business expenses, and need for tax planning and savings buffers.",
        "travel_enthusiast": "An individual who prioritizes travel experiences with significant spending on flights, accommodations, and international transactions.",
        
        # Business/company profiles
        "small_business": "A small business with regular revenue, operating expenses, inventory purchases, and business-related services.",
        "tech_startup": "A technology startup with venture funding, high development costs, subscription revenue, and rapid growth expenses.",
        "restaurant_business": "A restaurant with daily cash and card transactions, food and beverage inventory purchases, staffing costs, and equipment expenses.",
        "retail_store": "A retail business with seasonal sales patterns, inventory purchases, employee payroll, and commercial rent expenses."
    }

def generate_young_professional_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a young professional
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for young professional
    category_frequencies = {
        'Income': 0.15,  # Increased income frequency for better representation
        'Housing': 0.04,
        'Dining': 0.16,
        'Entertainment': 0.10,
        'Shopping': 0.12,
        'Transportation': 0.08,
        'Utilities': 0.04,
        'Groceries': 0.10,
        'Fitness': 0.06,
        'Subscriptions': 0.07,
        'Travel': 0.05,
        'Healthcare': 0.03
    }
    
    # Generate transactions with young professional profile - more transactions for better variety
    transactions = generate_sample_transactions(
        num_transactions=500,  # Increased transaction count
        income_range=(5500, 7500),  # Higher income range
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.18  # Slightly higher savings rate
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
        'Income': 0.15,  # Increased income frequency for better representation
        'Housing': 0.06,
        'Dining': 0.10,
        'Entertainment': 0.08,
        'Shopping': 0.10,
        'Transportation': 0.09,
        'Utilities': 0.06,
        'Groceries': 0.16,
        'Healthcare': 0.08,
        'Education': 0.08,
        'Fitness': 0.02,
        'Subscriptions': 0.02,
        'Travel': 0.03,
        'Childcare': 0.07  # Added childcare for family
    }
    
    # Generate transactions with family budget profile
    transactions = generate_sample_transactions(
        num_transactions=650,  # More transactions for a family
        income_range=(8000, 12000),  # Higher family income (dual income household)
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.08  # Lower savings rate due to family expenses
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
        'Income': 0.12,  # More income transactions to represent part-time work
        'Housing': 0.05,
        'Dining': 0.18,  # Students eat out frequently
        'Entertainment': 0.13,
        'Shopping': 0.08,
        'Transportation': 0.07,
        'Utilities': 0.04,
        'Groceries': 0.10,
        'Education': 0.14,  # Textbooks, supplies, fees
        'Subscriptions': 0.05,
        'Healthcare': 0.02,
        'Travel': 0.02  # Occasional trips home
    }
    
    # Generate transactions with student finances profile
    transactions = generate_sample_transactions(
        num_transactions=400,  # More comprehensive transaction history
        income_range=(800, 2200),  # Varied income from part-time jobs, financial aid
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.03  # Students typically have lower savings rates
    )
    
    # Add student loan disbursements and payments
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add student loan disbursement (start of semester - Aug and Jan)
    for month in [1, 8]:  # January and August
        loan_date = datetime.date(start_date.year, month, 15)
        if start_date <= loan_date <= end_date:
            transactions.append({
                'date': loan_date,
                'description': 'Student Loan Disbursement',
                'amount': 5000,
                'category': 'Income'
            })
    
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
        'Income': 0.12,  # Various income sources instead of salary
        'Housing': 0.04,
        'Dining': 0.08,
        'Entertainment': 0.06,
        'Shopping': 0.07,
        'Transportation': 0.05,
        'Utilities': 0.05,
        'Groceries': 0.10,
        'Healthcare': 0.15,  # Higher healthcare costs in retirement
        'Travel': 0.12,  # More travel in retirement
        'Fitness': 0.04,
        'Subscriptions': 0.03,
        'Investments': 0.09
    }
    
    # Generate transactions with retirement planning profile
    transactions = generate_sample_transactions(
        num_transactions=450,  # More transaction variety
        income_range=(4500, 6500),  # Retirement income range
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.18  # Typical retirement savings rate
    )
    
    # Add recurring retirement-specific income sources
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add monthly Social Security payments
    current_date = start_date
    while current_date <= end_date:
        if current_date.day == 3:  # Social Security typically deposits on the 3rd
            transactions.append({
                'date': current_date,
                'description': 'Social Security Payment',
                'amount': 1850,
                'category': 'Income'
            })
        current_date += datetime.timedelta(days=1)
    
    # Add quarterly dividend payments
    for month in [1, 4, 7, 10]:  # January, April, July, October
        dividend_date = datetime.date(start_date.year, month, 15)
        if start_date <= dividend_date <= end_date:
            transactions.append({
                'date': dividend_date,
                'description': 'Dividend Payment - Vanguard',
                'amount': 1200,
                'category': 'Income'
            })
    
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
        'Income': 0.10,  # Multiple income sources
        'Housing': 0.04,  # Higher-end housing
        'Dining': 0.14,  # Luxury dining
        'Entertainment': 0.09,  # Premium entertainment
        'Shopping': 0.14,  # High-end shopping
        'Transportation': 0.06,  # Luxury vehicles, ride services
        'Utilities': 0.02,  # Less significant percentage
        'Groceries': 0.06,  # Specialty grocers
        'Travel': 0.15,  # Luxury travel
        'Fitness': 0.05,  # Premium fitness
        'Subscriptions': 0.03,  # Premium services
        'Investments': 0.12   # Higher investment activity
    }
    
    # Generate transactions with high income profile - larger amounts and more transactions
    transactions = generate_sample_transactions(
        num_transactions=700,  # More varied transaction history
        income_range=(20000, 30000),  # Higher monthly income
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.25  # High but realistic savings rate
    )
    
    # Add specialty high-income transactions
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add quarterly stock sales
    for month in [3, 6, 9, 12]:
        stock_date = datetime.date(start_date.year, month, random.randint(10, 20))
        if start_date <= stock_date <= end_date:
            transactions.append({
                'date': stock_date,
                'description': f'Stock Sale - {random.choice(["Apple", "Google", "Amazon", "Microsoft"])}',
                'amount': random.randint(15000, 25000),
                'category': 'Income'
            })
    
    # Add annual bonus
    bonus_date = datetime.date(start_date.year, 12, 15)  # December bonus
    if start_date <= bonus_date <= end_date:
        transactions.append({
            'date': bonus_date,
            'description': 'Annual Performance Bonus',
            'amount': random.randint(50000, 100000),
            'category': 'Income'
        })
    
    # Add some luxury purchases
    luxury_purchases = [
        {'description': 'Fine Dining - Michelin Star Restaurant', 'amount': -random.randint(400, 800), 'category': 'Dining'},
        {'description': 'Designer Apparel Purchase', 'amount': -random.randint(1500, 3000), 'category': 'Shopping'},
        {'description': 'Luxury Watch Purchase', 'amount': -random.randint(5000, 12000), 'category': 'Shopping'},
        {'description': 'First Class Airfare', 'amount': -random.randint(3000, 7000), 'category': 'Travel'},
        {'description': 'Luxury Hotel Stay', 'amount': -random.randint(1500, 4000), 'category': 'Travel'},
        {'description': 'Private Golf Club Membership', 'amount': -random.randint(2000, 5000), 'category': 'Entertainment'}
    ]
    
    # Add these luxury purchases at random dates
    for purchase in luxury_purchases:
        random_days = random.randint(10, 350)
        purchase_date = start_date + datetime.timedelta(days=random_days)
        purchase_copy = purchase.copy()
        purchase_copy['date'] = purchase_date
        transactions.append(purchase_copy)
    
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
        'Income': 0.14,  # Regular income transactions
        'Housing': 0.05,
        'Dining': 0.07,  # Reduced dining out
        'Entertainment': 0.04,  # Reduced entertainment
        'Shopping': 0.05,  # Minimized shopping
        'Transportation': 0.08,
        'Utilities': 0.05,
        'Groceries': 0.12,
        'Healthcare': 0.05,
        'Debt Payments': 0.30,  # High proportion of debt payments
        'Subscriptions': 0.01,  # Minimal subscriptions
        'Education': 0.04
    }
    
    # Generate transactions with debt reduction profile
    transactions = generate_sample_transactions(
        num_transactions=450,  # More transaction history
        income_range=(4800, 6200),  # Moderate income
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.05  # Low savings rate due to debt payments
    )
    
    # Add specific recurring debt payments
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Define debt payment schedule
    debt_payments = [
        {'name': 'Credit Card Payment - Chase', 'amount': -650, 'day': 5},
        {'name': 'Credit Card Payment - Citi', 'amount': -450, 'day': 12},
        {'name': 'Personal Loan Payment', 'amount': -350, 'day': 15},
        {'name': 'Student Loan Payment', 'amount': -280, 'day': 21},
        {'name': 'Auto Loan Payment', 'amount': -420, 'day': 28}
    ]
    
    # Add monthly debt payments
    current_date = start_date
    while current_date <= end_date:
        for payment in debt_payments:
            if current_date.day == payment['day']:
                transactions.append({
                    'date': current_date,
                    'description': payment['name'],
                    'amount': payment['amount'],
                    'category': 'Debt Payments'
                })
        current_date += datetime.timedelta(days=1)
    
    # Add initial debt consolidation activity
    consolidation_date = start_date + datetime.timedelta(days=45)
    if start_date <= consolidation_date <= end_date:
        transactions.append({
            'date': consolidation_date,
            'description': 'Debt Consolidation Loan',
            'amount': 12000,  # Loan received
            'category': 'Income'
        })
        
        # Payment of other debts using consolidation
        transactions.append({
            'date': consolidation_date + datetime.timedelta(days=2),
            'description': 'Credit Card Payoff - Bank of America',
            'amount': -8500,
            'category': 'Debt Payments'
        })
        
        transactions.append({
            'date': consolidation_date + datetime.timedelta(days=2),
            'description': 'Credit Card Payoff - Discover',
            'amount': -3200,
            'category': 'Debt Payments'
        })
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_freelancer_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a freelance professional
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for freelancer
    category_frequencies = {
        'Income': 0.15,  # Irregular income sources
        'Housing': 0.05,
        'Dining': 0.10,
        'Entertainment': 0.07,
        'Shopping': 0.08,
        'Transportation': 0.06,
        'Utilities': 0.04,
        'Groceries': 0.10,
        'Healthcare': 0.08,  # Higher healthcare (self-insured)
        'Business Expenses': 0.12,  # Professional expenses
        'Subscriptions': 0.05,  # Software and services
        'Education': 0.06,  # Professional development
        'Travel': 0.04
    }
    
    # Generate transactions with freelancer profile
    transactions = generate_sample_transactions(
        num_transactions=500,
        income_range=(3000, 9000),  # Highly variable income
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.12  # Variable savings
    )
    
    # Add irregular client payments
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # List of potential clients and project types
    clients = [
        "DesignCorp", "TechSolutions", "MediaGroup", "StartupX", "LocalBusiness",
        "CreativeAgency", "ConsultingFirm", "SmallBizNetwork", "InnovationLabs", "WebServices"
    ]
    
    project_types = [
        "Website Development", "Graphic Design", "Content Creation", "Consulting", 
        "Marketing Campaign", "App Development", "Brand Strategy", "Video Production",
        "Social Media Management", "UX/UI Design"
    ]
    
    # Generate random client payments with irregular patterns
    num_payments = random.randint(15, 25)  # Number of client payments over the year
    payment_dates = []
    
    for _ in range(num_payments):
        random_days = random.randint(10, 355)
        payment_date = start_date + datetime.timedelta(days=random_days)
        if payment_date not in payment_dates and start_date <= payment_date <= end_date:
            payment_dates.append(payment_date)
            
            # Random client and project
            client = random.choice(clients)
            project = random.choice(project_types)
            
            # Random payment amount based on project
            if "Development" in project or "Production" in project:
                amount = random.randint(2000, 8000)  # Larger projects
            elif "Consulting" in project or "Strategy" in project:
                amount = random.randint(1500, 4000)  # Medium projects
            else:
                amount = random.randint(500, 2000)  # Smaller projects
                
            transactions.append({
                'date': payment_date,
                'description': f'Client Payment - {client} - {project}',
                'amount': amount,
                'category': 'Income'
            })
    
    # Add business expense transactions
    business_expenses = [
        {'description': 'Software Subscription - Adobe Creative Cloud', 'amount': -52.99, 'category': 'Business Expenses', 'monthly': True},
        {'description': 'Software Subscription - Microsoft 365', 'amount': -12.99, 'category': 'Business Expenses', 'monthly': True},
        {'description': 'Website Hosting', 'amount': -25, 'category': 'Business Expenses', 'monthly': True},
        {'description': 'Professional Association Membership', 'amount': -200, 'category': 'Business Expenses', 'monthly': False},
        {'description': 'Business Insurance', 'amount': -150, 'category': 'Business Expenses', 'monthly': False},
        {'description': 'Coworking Space Membership', 'amount': -299, 'category': 'Business Expenses', 'monthly': True},
        {'description': 'Office Supplies', 'amount': -random.randint(50, 200), 'category': 'Business Expenses', 'monthly': False},
        {'description': 'Professional Development Course', 'amount': -random.randint(300, 1200), 'category': 'Education', 'monthly': False},
        {'description': 'Networking Event', 'amount': -random.randint(20, 100), 'category': 'Business Expenses', 'monthly': False},
        {'description': 'Equipment Purchase', 'amount': -random.randint(500, 3000), 'category': 'Business Expenses', 'monthly': False}
    ]
    
    # Add monthly recurring business expenses
    current_date = start_date
    month_count = 0
    
    while current_date <= end_date:
        if current_date.day == 1:  # First of the month for recurring expenses
            for expense in business_expenses:
                if expense['monthly'] or (month_count % 3 == 0 and not expense['monthly']):
                    expense_copy = expense.copy()
                    expense_copy['date'] = current_date
                    if not expense['monthly']:
                        # Vary the non-monthly expenses slightly
                        expense_copy['amount'] = expense['amount'] * random.uniform(0.8, 1.2)
                    transactions.append(expense_copy)
            month_count += 1
        current_date += datetime.timedelta(days=1)
        
    # Add quarterly tax payments (self-employed)
    for month in [4, 6, 9, 1]:  # April, June, September, January (for previous year Q4)
        tax_date = datetime.date(start_date.year if month != 1 else start_date.year + 1, month, 15)
        if start_date <= tax_date <= end_date:
            transactions.append({
                'date': tax_date,
                'description': 'Quarterly Estimated Tax Payment',
                'amount': -random.randint(2000, 4000),
                'category': 'Business Expenses'
            })
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_travel_enthusiast_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a travel enthusiast
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for travel enthusiast
    category_frequencies = {
        'Income': 0.12,  # Regular income
        'Housing': 0.05,
        'Dining': 0.12,  # Dining out frequently including while traveling
        'Entertainment': 0.08,
        'Shopping': 0.10,
        'Transportation': 0.08,
        'Utilities': 0.03,
        'Groceries': 0.07,
        'Travel': 0.25,  # Major focus on travel
        'Subscriptions': 0.04,
        'Healthcare': 0.03,
        'Education': 0.03
    }
    
    # Generate transactions with travel enthusiast profile
    transactions = generate_sample_transactions(
        num_transactions=600,
        income_range=(6000, 8500),  # Good income to support travel
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.10
    )
    
    # Add specific travel-related transactions
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Create major travel events (3-5 major trips per year)
    num_trips = random.randint(3, 5)
    trip_destinations = [
        "Paris, France", "Tokyo, Japan", "Rome, Italy", "Bali, Indonesia", 
        "New York, USA", "Sydney, Australia", "London, UK", "Barcelona, Spain",
        "Costa Rica", "Thailand", "Amsterdam, Netherlands", "Marrakech, Morocco"
    ]
    
    for _ in range(num_trips):
        # Random trip start date
        trip_start_day = random.randint(30, 330)
        trip_start = start_date + datetime.timedelta(days=trip_start_day)
        trip_length = random.randint(5, 14)  # 5-14 day trips
        
        # Skip if outside our time range
        if trip_start > end_date:
            continue
            
        # Select random destination
        destination = random.choice(trip_destinations)
        trip_destinations.remove(destination)  # No repeat destinations
        
        # Flight booking (typically 1-3 months before trip)
        booking_date = trip_start - datetime.timedelta(days=random.randint(30, 90))
        if booking_date >= start_date:
            transactions.append({
                'date': booking_date,
                'description': f'Airfare to {destination}',
                'amount': -random.randint(600, 2000),
                'category': 'Travel'
            })
        
        # Hotel or accommodations (booked around same time)
        if booking_date >= start_date:
            transactions.append({
                'date': booking_date + datetime.timedelta(days=random.randint(0, 5)),
                'description': f'Accommodation in {destination}',
                'amount': -random.randint(500, 2500),
                'category': 'Travel'
            })
        
        # During trip expenses (if trip is within our date range)
        trip_end = trip_start + datetime.timedelta(days=trip_length)
        current_date = max(trip_start, start_date)
        end_trip_date = min(trip_end, end_date)
        
        while current_date <= end_trip_date:
            # Daily vacation expenses
            if random.random() < 0.8:  # 80% chance of restaurant charges each day
                transactions.append({
                    'date': current_date,
                    'description': f'Restaurant in {destination}',
                    'amount': -random.randint(50, 200),
                    'category': 'Dining'
                })
                
            if random.random() < 0.7:  # 70% chance of activity/entertainment charges
                transactions.append({
                    'date': current_date,
                    'description': f'Activity/Tour in {destination}',
                    'amount': -random.randint(100, 300),
                    'category': 'Travel'
                })
                
            if random.random() < 0.5:  # 50% chance of shopping
                transactions.append({
                    'date': current_date,
                    'description': f'Shopping in {destination}',
                    'amount': -random.randint(50, 250),
                    'category': 'Shopping'
                })
                
            if random.random() < 0.4:  # 40% chance of transportation
                transactions.append({
                    'date': current_date,
                    'description': f'Local Transportation in {destination}',
                    'amount': -random.randint(20, 100),
                    'category': 'Transportation'
                })
                
            current_date += datetime.timedelta(days=1)
    
    # Add travel-related subscriptions
    travel_subscriptions = [
        {'description': 'Priority Pass Membership', 'amount': -429, 'annual': True},
        {'description': 'Travel Insurance Annual Plan', 'amount': -250, 'annual': True},
        {'description': 'Language Learning App', 'amount': -12.99, 'annual': False},
        {'description': 'Travel Credit Card Annual Fee', 'amount': -95, 'annual': True}
    ]
    
    # Add these subscriptions
    for sub in travel_subscriptions:
        if sub['annual']:
            # One-time annual charge
            charge_day = random.randint(30, 330)
            charge_date = start_date + datetime.timedelta(days=charge_day)
            if start_date <= charge_date <= end_date:
                transactions.append({
                    'date': charge_date,
                    'description': sub['description'],
                    'amount': sub['amount'],
                    'category': 'Subscriptions'
                })
        else:
            # Monthly charge
            current_date = start_date
            while current_date <= end_date:
                if current_date.day == 15:  # Middle of month charge
                    transactions.append({
                        'date': current_date,
                        'description': sub['description'],
                        'amount': sub['amount'],
                        'category': 'Subscriptions'
                    })
                current_date += datetime.timedelta(days=1)
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_small_business_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a small business
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for small business
    category_frequencies = {
        'Income': 0.20,  # Business revenue (using Income category for consistency)
        'Rent': 0.04,     # Business rent
        'Utilities': 0.04,
        'Supplies': 0.10,
        'Inventory': 0.18,
        'Services': 0.06,
        'Marketing': 0.05,
        'Payroll': 0.15,
        'Insurance': 0.03,
        'Equipment': 0.04,
        'Taxes': 0.05,
        'Miscellaneous': 0.06
    }
    
    # Generate business transactions
    transactions = generate_sample_transactions(
        num_transactions=700,
        income_range=(20000, 35000),  # Business revenue
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.12  # Business profit margin
    )
    
    # Keep 'Income' category for proper income tracking
    # No longer converting Income to Revenue for consistency
    
    # Add specific business transactions
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add regular payroll (bi-weekly)
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 4 and current_date.day in [15, 30] or current_date.day == 28:  # Fridays near 15th and 30th
            transactions.append({
                'date': current_date,
                'description': 'Employee Payroll',
                'amount': -random.randint(8000, 12000),
                'category': 'Payroll'
            })
        current_date += datetime.timedelta(days=1)
    
    # Add quarterly tax payments
    for month in [4, 7, 10, 1]:  # April, July, October, January
        if month == 1:
            tax_date = datetime.date(start_date.year + 1, month, 15)
        else:
            tax_date = datetime.date(start_date.year, month, 15)
            
        if start_date <= tax_date <= end_date:
            transactions.append({
                'date': tax_date,
                'description': 'Quarterly Business Tax Payment',
                'amount': -random.randint(4000, 7000),
                'category': 'Taxes'
            })
    
    # Add monthly recurring expenses
    monthly_expenses = [
        {'description': 'Business Rent', 'amount': -random.randint(2000, 4000), 'category': 'Rent'},
        {'description': 'Business Insurance', 'amount': -random.randint(300, 600), 'category': 'Insurance'},
        {'description': 'Internet and Phone', 'amount': -random.randint(150, 300), 'category': 'Utilities'},
        {'description': 'Electricity', 'amount': -random.randint(200, 500), 'category': 'Utilities'},
        {'description': 'Accounting Services', 'amount': -random.randint(300, 700), 'category': 'Services'},
        {'description': 'Cleaning Service', 'amount': -random.randint(200, 400), 'category': 'Services'},
        {'description': 'Office Supplies', 'amount': -random.randint(100, 300), 'category': 'Supplies'},
        {'description': 'Marketing Services', 'amount': -random.randint(500, 1500), 'category': 'Marketing'}
    ]
    
    # Add these monthly expenses
    current_date = start_date
    while current_date <= end_date:
        if current_date.day == 1:  # First of month payment
            for expense in monthly_expenses:
                # Add some variability to monthly amounts
                expense_copy = expense.copy()
                base_amount = expense['amount']
                expense_copy['amount'] = int(base_amount * random.uniform(0.9, 1.1))
                expense_copy['date'] = current_date
                transactions.append(expense_copy)
        current_date += datetime.timedelta(days=1)
    
    # Add inventory purchases (variable frequency)
    inventory_suppliers = [
        "Wholesale Supplier A", "Manufacturer B", "Distributor C", 
        "Import Company D", "Local Producer E"
    ]
    
    # Generate 20-30 inventory purchases over the year
    for _ in range(random.randint(20, 30)):
        purchase_day = random.randint(10, 355)
        purchase_date = start_date + datetime.timedelta(days=purchase_day)
        
        if start_date <= purchase_date <= end_date:
            supplier = random.choice(inventory_suppliers)
            transactions.append({
                'date': purchase_date,
                'description': f'Inventory Purchase - {supplier}',
                'amount': -random.randint(1000, 5000),
                'category': 'Inventory'
            })
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_tech_startup_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a technology startup
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for tech startup
    category_frequencies = {
        'Income': 0.25,        # Combined revenue streams and funding (for proper income tracking)
        'Rent': 0.05,           # Office space
        'Utilities': 0.03,
        'Supplies': 0.05,
        'Software': 0.08,        # SaaS tools and services
        'Hardware': 0.06,        # Equipment and devices
        'Marketing': 0.08,       # Digital marketing
        'Payroll': 0.20,         # Tech talent is expensive
        'Insurance': 0.02,
        'Legal': 0.03,           # IP protection, contracts
        'Travel': 0.04,          # Conferences, investor meetings
        'Services': 0.06,        # Professional services
        'Miscellaneous': 0.05
    }
    
    # Generate tech startup transactions
    transactions = generate_sample_transactions(
        num_transactions=600,
        income_range=(15000, 40000),  # Variable revenue/funding
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.05  # Startups typically operate at a loss or slim margins
    )
    
    # Keep 'Income' category for proper income tracking
    # No longer converting Income to Revenue for consistency
    
    # Add specific startup transactions
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add funding round(s)
    funding_rounds = [
        {'name': 'Seed Funding', 'amount': random.randint(250000, 500000), 'month': random.randint(1, 6)},
        {'name': 'Angel Investment', 'amount': random.randint(100000, 200000), 'month': random.randint(7, 12)}
    ]
    
    for funding in funding_rounds:
        funding_date = datetime.date(start_date.year, funding['month'], random.randint(1, 28))
        if start_date <= funding_date <= end_date:
            transactions.append({
                'date': funding_date,
                'description': funding['name'],
                'amount': funding['amount'],
                'category': 'Funding'
            })
    
    # Add tech talent payroll (higher than typical small business)
    current_date = start_date
    while current_date <= end_date:
        if current_date.day == 15:  # Monthly payroll
            transactions.append({
                'date': current_date,
                'description': 'Tech Team Payroll',
                'amount': -random.randint(18000, 25000),
                'category': 'Payroll'
            })
        current_date += datetime.timedelta(days=1)
    
    # Add software subscriptions and services
    tech_expenses = [
        {'description': 'AWS Cloud Services', 'amount': -random.randint(1500, 4000), 'category': 'Software'},
        {'description': 'GitHub Enterprise', 'amount': -random.randint(200, 500), 'category': 'Software'},
        {'description': 'Atlassian Suite', 'amount': -random.randint(200, 600), 'category': 'Software'},
        {'description': 'Slack Enterprise', 'amount': -random.randint(150, 400), 'category': 'Software'},
        {'description': 'GSuite Business', 'amount': -random.randint(100, 300), 'category': 'Software'},
        {'description': 'Analytics Platform', 'amount': -random.randint(300, 800), 'category': 'Software'},
        {'description': 'CRM Software', 'amount': -random.randint(200, 600), 'category': 'Software'},
        {'description': 'Design Software Licenses', 'amount': -random.randint(100, 400), 'category': 'Software'},
        {'description': 'Coworking Space Rent', 'amount': -random.randint(2000, 5000), 'category': 'Rent'},
        {'description': 'Legal Services', 'amount': -random.randint(1000, 3000), 'category': 'Legal', 'quarterly': True},
        {'description': 'Digital Marketing Campaign', 'amount': -random.randint(1000, 5000), 'category': 'Marketing', 'quarterly': True},
        {'description': 'Recruitment Services', 'amount': -random.randint(1000, 3000), 'category': 'Services', 'quarterly': True}
    ]
    
    # Add monthly recurring expenses
    current_date = start_date
    month_count = 0
    
    while current_date <= end_date:
        if current_date.day == 1:  # First of month
            for expense in tech_expenses:
                if 'quarterly' not in expense or (month_count % 3 == 0 and expense['quarterly']):
                    expense_copy = expense.copy()
                    expense_copy['date'] = current_date
                    # Add some variation to amounts
                    expense_copy['amount'] = int(expense['amount'] * random.uniform(0.9, 1.1))
                    transactions.append(expense_copy)
            month_count += 1
        current_date += datetime.timedelta(days=1)
    
    # Add equipment purchases
    equipment_purchases = [
        {'description': 'Developer Workstations', 'amount': -random.randint(5000, 15000), 'month': random.randint(1, 4)},
        {'description': 'Office Equipment', 'amount': -random.randint(2000, 5000), 'month': random.randint(1, 4)},
        {'description': 'Server Hardware', 'amount': -random.randint(3000, 8000), 'month': random.randint(5, 8)},
        {'description': 'Mobile Test Devices', 'amount': -random.randint(1000, 3000), 'month': random.randint(9, 12)}
    ]
    
    for purchase in equipment_purchases:
        purchase_date = datetime.date(start_date.year, purchase['month'], random.randint(1, 28))
        if start_date <= purchase_date <= end_date:
            transactions.append({
                'date': purchase_date,
                'description': purchase['description'],
                'amount': purchase['amount'],
                'category': 'Hardware'
            })
    
    # Add customer/client revenue (B2B SaaS model)
    # More irregular at first, then gradually more recurring
    client_acquisitions = [
        {'month': 2, 'clients': random.randint(2, 5), 'avg_revenue': random.randint(500, 1500)},
        {'month': 5, 'clients': random.randint(5, 10), 'avg_revenue': random.randint(500, 1500)},
        {'month': 8, 'clients': random.randint(8, 15), 'avg_revenue': random.randint(500, 1500)},
        {'month': 11, 'clients': random.randint(10, 20), 'avg_revenue': random.randint(500, 1500)},
    ]
    
    # Create initial client acquisitions
    active_clients = []
    for acquisition in client_acquisitions:
        acquisition_month = acquisition['month']
        for _ in range(acquisition['clients']):
            client_name = f"Client {random.randint(1000, 9999)}"
            client_revenue = acquisition['avg_revenue'] * random.uniform(0.7, 1.3)
            acquisition_date = datetime.date(start_date.year, acquisition_month, random.randint(1, 28))
            
            if start_date <= acquisition_date <= end_date:
                transactions.append({
                    'date': acquisition_date,
                    'description': f'New Subscription - {client_name}',
                    'amount': client_revenue,
                    'category': 'Revenue'
                })
                
                # Add this client to active recurring clients
                active_clients.append({
                    'name': client_name,
                    'revenue': client_revenue,
                    'start_month': acquisition_month,
                    'churn_chance': random.uniform(0.0, 0.1)  # 0-10% monthly churn rate
                })
    
    # Generate recurring revenue from active clients
    for client in active_clients:
        current_month = client['start_month'] + 1
        churned = False
        
        while current_month <= 12 and not churned:
            # Check if client churns this month
            if random.random() < client['churn_chance']:
                churned = True
                continue
                
            payment_date = datetime.date(start_date.year, current_month, random.randint(1, 28))
            if start_date <= payment_date <= end_date:
                transactions.append({
                    'date': payment_date,
                    'description': f'Monthly Subscription - {client["name"]}',
                    'amount': client['revenue'],
                    'category': 'Revenue'
                })
            
            current_month += 1
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_restaurant_business_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a restaurant business
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for restaurant business
    category_frequencies = {
        'Income': 0.30,        # Daily food & beverage sales (using Income for consistency)
        'Food Inventory': 0.18,  # Food ingredients
        'Beverage Inventory': 0.10, # Drinks inventory
        'Rent': 0.05,          # Restaurant space
        'Utilities': 0.04,      # Higher for restaurants
        'Equipment': 0.03,      # Kitchen equipment
        'Marketing': 0.03,      # Local advertising
        'Payroll': 0.18,        # Staff wages
        'Insurance': 0.02,      # Business insurance
        'Maintenance': 0.03,    # Equipment & facility
        'Services': 0.02,       # POS, delivery platforms
        'Miscellaneous': 0.02   # Other expenses
    }
    
    # Generate restaurant transactions
    transactions = generate_sample_transactions(
        num_transactions=900,   # Restaurants have many daily transactions
        income_range=(15000, 25000),  # Monthly revenue
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.08       # Restaurant profit margins
    )
    
    # Keep 'Income' category for proper income tracking
    # No longer converting Income to Revenue for consistency
    
    # Add specific restaurant transactions
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add daily revenue patterns (higher on weekends)
    current_date = start_date
    while current_date <= end_date:
        # Restaurants have higher sales on weekends
        weekday = current_date.weekday()  # 0-6 (Mon-Sun)
        
        # Weekend revenues (Friday-Sunday)
        if weekday >= 4:  
            # Generate 2-5 larger ticket sales for dinner service
            for _ in range(random.randint(2, 5)):
                transactions.append({
                    'date': current_date,
                    'description': 'Dinner Service Sales',
                    'amount': random.randint(800, 2000),
                    'category': 'Revenue'
                })
                
            # Generate 1-3 lunch service sales
            for _ in range(random.randint(1, 3)):
                transactions.append({
                    'date': current_date,
                    'description': 'Lunch Service Sales',
                    'amount': random.randint(400, 1200),
                    'category': 'Revenue'
                })
        
        # Weekday revenues (Monday-Thursday)  
        else:  
            # Generate 1-3 moderate dinner service sales
            for _ in range(random.randint(1, 3)):
                transactions.append({
                    'date': current_date,
                    'description': 'Dinner Service Sales',
                    'amount': random.randint(500, 1200),
                    'category': 'Revenue'
                })
                
            # Generate 1-2 lunch service sales
            for _ in range(random.randint(1, 2)):
                transactions.append({
                    'date': current_date,
                    'description': 'Lunch Service Sales',
                    'amount': random.randint(300, 800),
                    'category': 'Revenue'
                })
        
        # Special events (randomly about twice a month)
        if random.random() < 0.065:  # ~2 events per month
            transactions.append({
                'date': current_date,
                'description': 'Private Event / Catering',
                'amount': random.randint(1500, 4000),
                'category': 'Revenue'
            })
            
        current_date += datetime.timedelta(days=1)
    
    # Add staff payroll (bi-weekly)
    current_date = start_date
    while current_date <= end_date:
        # Bi-weekly payroll (every other Friday)
        if current_date.weekday() == 4 and current_date.day % 14 < 7:  # Friday and approximately every other week
            transactions.append({
                'date': current_date,
                'description': 'Restaurant Staff Payroll',
                'amount': -random.randint(6000, 9000),
                'category': 'Payroll'
            })
        current_date += datetime.timedelta(days=1)
    
    # Add food and beverage inventory purchases
    # Restaurants typically order multiple times per week
    current_date = start_date
    suppliers = [
        "Sysco Foods", "US Foods", "Local Produce Supplier", "Restaurant Depot", 
        "Seafood Wholesaler", "Meat Distributor", "Specialty Foods"
    ]
    
    beverage_suppliers = [
        "Beverage Distributor", "Wine Wholesaler", "Brewery Distributor", 
        "Liquor Distributor", "Coffee Supplier"
    ]
    
    while current_date <= end_date:
        # Food orders - typically 2-3 times per week (Monday, Thursday)
        if current_date.weekday() in [0, 3]:  # Monday and Thursday
            if random.random() < 0.8:  # 80% chance of ordering on these days
                supplier = random.choice(suppliers)
                transactions.append({
                    'date': current_date,
                    'description': f'Food Inventory - {supplier}',
                    'amount': -random.randint(800, 2500),
                    'category': 'Food Inventory'
                })
        
        # Beverage orders - typically once a week
        if current_date.weekday() == 1:  # Tuesday
            if random.random() < 0.75:  # 75% chance of ordering beverages weekly
                supplier = random.choice(beverage_suppliers)
                transactions.append({
                    'date': current_date,
                    'description': f'Beverage Order - {supplier}',
                    'amount': -random.randint(500, 1800),
                    'category': 'Beverage Inventory'
                })
        
        current_date += datetime.timedelta(days=1)
    
    # Add monthly fixed expenses
    monthly_expenses = [
        {'description': 'Restaurant Rent', 'amount': -random.randint(3500, 6000), 'category': 'Rent'},
        {'description': 'Electricity', 'amount': -random.randint(800, 1500), 'category': 'Utilities'},
        {'description': 'Water and Sewer', 'amount': -random.randint(300, 700), 'category': 'Utilities'},
        {'description': 'Gas', 'amount': -random.randint(400, 900), 'category': 'Utilities'},
        {'description': 'Restaurant Insurance', 'amount': -random.randint(400, 800), 'category': 'Insurance'},
        {'description': 'POS System Subscription', 'amount': -random.randint(100, 300), 'category': 'Services'},
        {'description': 'Waste Management', 'amount': -random.randint(200, 500), 'category': 'Services'},
        {'description': 'Pest Control', 'amount': -random.randint(100, 250), 'category': 'Maintenance', 'monthly': False},
        {'description': 'Equipment Maintenance', 'amount': -random.randint(200, 600), 'category': 'Maintenance', 'monthly': False},
        {'description': 'Cleaning Supplies', 'amount': -random.randint(100, 300), 'category': 'Miscellaneous'},
        {'description': 'Menu Printing', 'amount': -random.randint(50, 150), 'category': 'Marketing', 'monthly': False},
        {'description': 'Local Advertising', 'amount': -random.randint(200, 800), 'category': 'Marketing', 'monthly': False}
    ]
    
    # Add monthly expenses
    current_date = start_date
    month_count = 0
    while current_date <= end_date:
        if current_date.day == 1:  # First of the month for most bills
            for expense in monthly_expenses:
                if 'monthly' not in expense or expense['monthly'] is not False or (month_count % 3 == 0):
                    expense_copy = expense.copy()
                    expense_copy['date'] = current_date
                    expense_copy['amount'] = int(expense['amount'] * random.uniform(0.9, 1.1))  # Slight variation
                    transactions.append(expense_copy)
            month_count += 1
        current_date += datetime.timedelta(days=1)
    
    # Add occasional equipment purchases/replacements
    equipment_purchases = [
        {'description': 'Kitchen Equipment Replacement', 'amount': -random.randint(1000, 5000), 'category': 'Equipment'},
        {'description': 'Dining Furniture Update', 'amount': -random.randint(1500, 4000), 'category': 'Equipment'},
        {'description': 'Bar Equipment', 'amount': -random.randint(800, 3000), 'category': 'Equipment'},
        {'description': 'Refrigeration Repair', 'amount': -random.randint(500, 2000), 'category': 'Equipment'}
    ]
    
    # Add 2-3 equipment purchases throughout the year
    for _ in range(random.randint(2, 3)):
        purchase = random.choice(equipment_purchases)
        purchase_day = random.randint(30, 330)
        purchase_date = start_date + datetime.timedelta(days=purchase_day)
        
        if start_date <= purchase_date <= end_date:
            purchase_copy = purchase.copy()
            purchase_copy['date'] = purchase_date
            transactions.append(purchase_copy)
    
    # Calculate metrics and prepare sample data
    return prepare_sample_data(transactions)

def generate_retail_store_profile() -> Dict[str, Any]:
    """
    Generate a financial profile for a retail store business
    
    Returns:
        Sample data dictionary
    """
    # Customize category frequencies for retail store
    category_frequencies = {
        'Income': 0.30,        # Sales revenue (using Income for consistency)
        'Inventory': 0.25,      # Product inventory
        'Rent': 0.05,          # Store location rent
        'Utilities': 0.03,      # Utilities
        'Equipment': 0.02,      # Store equipment
        'Marketing': 0.06,      # Advertising, promotions
        'Payroll': 0.15,        # Staff wages
        'Insurance': 0.02,      # Business insurance
        'Fixtures': 0.03,       # Store fixtures, displays
        'Services': 0.05,       # POS, security, etc
        'Shipping': 0.02,       # Shipping costs
        'Miscellaneous': 0.02   # Other expenses
    }
    
    # Generate retail transactions
    transactions = generate_sample_transactions(
        num_transactions=800,   # Retail has many transactions
        income_range=(18000, 32000),  # Monthly revenue range
        category_frequencies=category_frequencies,
        months=12,
        savings_rate=0.10       # Retail profit margins
    )
    
    # Keep 'Income' category for proper income tracking
    # No longer converting Income to Revenue for consistency
    
    # Add specific retail transactions
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    
    # Add daily revenue patterns (higher on weekends, seasonal patterns)
    current_date = start_date
    while current_date <= end_date:
        # Get month for seasonal factors
        month = current_date.month
        
        # Seasonal factors: Higher holiday (Nov-Dec), Back-to-school (Aug), summer (Jun-Jul)
        seasonal_factor = 1.0
        if month in [11, 12]:  # Holiday season (Nov-Dec)
            seasonal_factor = 1.8
        elif month == 8:  # Back-to-school
            seasonal_factor = 1.4
        elif month in [6, 7]:  # Summer
            seasonal_factor = 1.2
        elif month in [1, 2]:  # Post-holiday slump
            seasonal_factor = 0.7
        
        # Weekend factor (higher sales on weekend)
        weekday = current_date.weekday()  # 0-6 (Mon-Sun)
        weekend_factor = 1.3 if weekday >= 5 else 1.0  # Weekend boost
        
        # Daily sales factor combines seasonal and weekend effects
        daily_factor = seasonal_factor * weekend_factor
        
        # Generate 2-6 sales transactions per day, higher on busy days
        num_transactions = max(2, min(6, int(daily_factor * 3)))
        
        for _ in range(num_transactions):
            # Base amount adjusted by daily factors
            base_amount = random.randint(300, 1200)
            amount = int(base_amount * daily_factor)
            
            transactions.append({
                'date': current_date,
                'description': 'Store Sales',
                'amount': amount,
                'category': 'Revenue'
            })
        
        # Special sales/promotions (randomly throughout year, more during holiday season)
        promotion_chance = 0.03  # Base chance
        if month in [11, 12]:
            promotion_chance = 0.12  # Higher during holidays
        elif month in [6, 7, 8]:
            promotion_chance = 0.08  # Higher during summer/back-to-school
            
        if random.random() < promotion_chance:
            transactions.append({
                'date': current_date,
                'description': 'Special Promotion Sales',
                'amount': random.randint(1000, 4000),
                'category': 'Revenue'
            })
            
        current_date += datetime.timedelta(days=1)
    
    # Add staff payroll (bi-weekly)
    current_date = start_date
    while current_date <= end_date:
        # Bi-weekly payroll (every other Friday)
        if current_date.weekday() == 4 and current_date.day % 14 < 7:  # Friday and approximately every other week
            base_payroll = random.randint(5000, 7000)
            
            # Higher payroll during holiday season (temp workers)
            if current_date.month in [11, 12]:
                base_payroll = int(base_payroll * 1.4)
                
            transactions.append({
                'date': current_date,
                'description': 'Retail Staff Payroll',
                'amount': -base_payroll,
                'category': 'Payroll'
            })
        current_date += datetime.timedelta(days=1)
    
    # Add inventory purchases (seasonal patterns)
    # Retail typically orders inventory in advance of selling seasons
    current_date = start_date
    suppliers = [
        "Main Distributor", "Wholesale Supplier", "Brand Manufacturer", 
        "Import Company", "Local Producer", "Factory Direct"
    ]
    
    # Define seasonal ordering times (typically order 1-3 months ahead of season)
    seasonal_ordering = [
        {'season': 'Spring', 'months': [1, 2], 'amount_factor': 1.2},  # January-February for Spring
        {'season': 'Summer', 'months': [3, 4], 'amount_factor': 1.4},  # March-April for Summer
        {'season': 'Back-to-School', 'months': [5, 6], 'amount_factor': 1.3},  # May-June for Back-to-School
        {'season': 'Fall', 'months': [7, 8], 'amount_factor': 1.1},  # July-August for Fall
        {'season': 'Holiday', 'months': [9, 10], 'amount_factor': 1.8}   # September-October for Holiday
    ]
    
    while current_date <= end_date:
        # Regular smaller inventory orders (once per week)
        if current_date.weekday() == 2:  # Wednesday
            if random.random() < 0.85:  # 85% chance of weekly orders
                supplier = random.choice(suppliers)
                transactions.append({
                    'date': current_date,
                    'description': f'Regular Inventory - {supplier}',
                    'amount': -random.randint(800, 2000),
                    'category': 'Inventory'
                })
        
        # Seasonal large inventory orders
        month = current_date.month
        for season in seasonal_ordering:
            if month in season['months'] and current_date.day in [10, 25]:  # Twice during ordering months
                if random.random() < 0.6:  # 60% chance on these days during seasonal ordering months
                    supplier = random.choice(suppliers)
                    base_amount = random.randint(5000, 12000)
                    amount = int(base_amount * season['amount_factor'])
                    transactions.append({
                        'date': current_date,
                        'description': f'{season["season"]} Inventory Order - {supplier}',
                        'amount': -amount,
                        'category': 'Inventory'
                    })
        
        current_date += datetime.timedelta(days=1)
    
    # Add monthly fixed expenses
    monthly_expenses = [
        {'description': 'Store Rent', 'amount': -random.randint(3000, 6000), 'category': 'Rent'},
        {'description': 'Electricity', 'amount': -random.randint(400, 900), 'category': 'Utilities'},
        {'description': 'Water', 'amount': -random.randint(100, 250), 'category': 'Utilities'},
        {'description': 'Internet and Phone', 'amount': -random.randint(150, 350), 'category': 'Utilities'},
        {'description': 'Store Insurance', 'amount': -random.randint(300, 700), 'category': 'Insurance'},
        {'description': 'POS System Subscription', 'amount': -random.randint(100, 300), 'category': 'Services'},
        {'description': 'Security System', 'amount': -random.randint(150, 350), 'category': 'Services'},
        {'description': 'Cleaning Service', 'amount': -random.randint(200, 500), 'category': 'Services'},
        {'description': 'Local Advertising', 'amount': -random.randint(500, 1500), 'category': 'Marketing', 'monthly': True},
        {'description': 'Social Media Marketing', 'amount': -random.randint(300, 1000), 'category': 'Marketing', 'monthly': True},
        {'description': 'Shipping Costs', 'amount': -random.randint(200, 800), 'category': 'Shipping'}
    ]
    
    # Add monthly expenses
    current_date = start_date
    month_count = 0
    while current_date <= end_date:
        if current_date.day == 1:  # First of the month for most bills
            for expense in monthly_expenses:
                if 'monthly' not in expense or expense['monthly']:
                    expense_copy = expense.copy()
                    expense_copy['date'] = current_date
                    
                    # Seasonal variation for marketing expenses
                    if expense['category'] == 'Marketing' and current_date.month in [10, 11, 12]:  # Higher holiday marketing
                        expense_copy['amount'] = int(expense['amount'] * random.uniform(1.5, 2.0))
                    else:
                        expense_copy['amount'] = int(expense['amount'] * random.uniform(0.9, 1.1))  # Normal variation
                        
                    transactions.append(expense_copy)
            month_count += 1
        current_date += datetime.timedelta(days=1)
    
    # Add store equipment and fixtures purchases (periodic updates)
    store_updates = [
        {'description': 'Store Fixtures Update', 'amount': -random.randint(2000, 8000), 'category': 'Fixtures'},
        {'description': 'Display Equipment', 'amount': -random.randint(1000, 4000), 'category': 'Fixtures'},
        {'description': 'POS Hardware Upgrade', 'amount': -random.randint(1500, 4000), 'category': 'Equipment'},
        {'description': 'Security System Upgrade', 'amount': -random.randint(1000, 3000), 'category': 'Equipment'},
        {'description': 'Store Renovation', 'amount': -random.randint(5000, 15000), 'category': 'Fixtures'}
    ]
    
    # Add 2-4 store updates throughout the year
    for _ in range(random.randint(2, 4)):
        update = random.choice(store_updates)
        update_day = random.randint(30, 330)
        update_date = start_date + datetime.timedelta(days=update_day)
        
        if start_date <= update_date <= end_date:
            update_copy = update.copy()
            update_copy['date'] = update_date
            transactions.append(update_copy)
    
    # Add seasonal marketing campaigns
    marketing_campaigns = [
        {'description': 'Spring Marketing Campaign', 'amount': -random.randint(2000, 5000), 'month': 3},  # March
        {'description': 'Summer Sale Campaign', 'amount': -random.randint(2000, 5000), 'month': 6},  # June
        {'description': 'Back-to-School Campaign', 'amount': -random.randint(3000, 6000), 'month': 8},  # August
        {'description': 'Black Friday Campaign', 'amount': -random.randint(4000, 8000), 'month': 11},  # November
        {'description': 'Holiday Marketing Campaign', 'amount': -random.randint(4000, 8000), 'month': 12}  # December
    ]
    
    # Add marketing campaigns
    for campaign in marketing_campaigns:
        campaign_date = datetime.date(start_date.year, campaign['month'], random.randint(1, 10))  # Early in month
        if start_date <= campaign_date <= end_date:
            transactions.append({
                'date': campaign_date,
                'description': campaign['description'],
                'amount': campaign['amount'],
                'category': 'Marketing'
            })
    
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
        # Individual profiles
        "young_professional": generate_young_professional_profile,
        "family_budget": generate_family_budget_profile,
        "student_finances": generate_student_finances_profile,
        "retirement_planning": generate_retirement_planning_profile,
        "high_income": generate_high_income_profile,
        "debt_reduction": generate_debt_reduction_profile,
        "freelancer": generate_freelancer_profile,
        "travel_enthusiast": generate_travel_enthusiast_profile,
        
        # Business/company profiles
        "small_business": generate_small_business_profile,
        "tech_startup": generate_tech_startup_profile,
        "restaurant_business": generate_restaurant_business_profile,
        "retail_store": generate_retail_store_profile
    }
    
    if profile_name in profile_generators:
        return profile_generators[profile_name]()
    else:
        # Default to young professional if profile not found
        return generate_young_professional_profile()
