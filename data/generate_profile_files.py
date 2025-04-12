#!/usr/bin/env python3
"""
Generate sample data files for different financial profiles
"""

import os
import json
import csv
import datetime
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.sample_profiles import get_profile_names, get_sample_profile

def save_profile_to_csv(profile_name: str, profile_data: Dict[str, Any], output_dir: str):
    """
    Save profile transactions to a CSV file
    
    Args:
        profile_name: Name of the profile
        profile_data: Profile data dictionary
        output_dir: Directory to save the file
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the output file path
    file_path = os.path.join(output_dir, f"{profile_name}.csv")
    
    # Extract transactions
    transactions = profile_data['transactions']
    
    # Ensure there are income transactions
    has_income = any(t['amount'] > 0 for t in transactions)
    if not has_income:
        # Add income transactions if none exist
        income_amount = 4500  # Default income amount
        if profile_name == 'young_professional':
            income_amount = 4500
        elif profile_name == 'family_budget':
            income_amount = 7500
        elif profile_name == 'student_finances':
            income_amount = 1500
        elif profile_name == 'retirement_planning':
            income_amount = 5000
        elif profile_name == 'high_income':
            income_amount = 15000
        elif profile_name == 'debt_reduction':
            income_amount = 5000
            
        # Add bi-weekly income for the past year
        start_date = datetime.date.today() - datetime.timedelta(days=365)
        current_date = start_date
        end_date = datetime.date.today()
        payment_interval = 14  # bi-weekly
        
        while current_date <= end_date:
            transactions.append({
                'date': current_date,
                'description': 'Employer Payroll',
                'amount': income_amount,
                'category': 'Income'
            })
            current_date += datetime.timedelta(days=payment_interval)
    
    # Write transactions to CSV
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['date', 'description', 'amount', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for transaction in transactions:
            # Convert date to string if it's a datetime object
            if isinstance(transaction['date'], datetime.date):
                transaction = transaction.copy()
                transaction['date'] = transaction['date'].isoformat()
            writer.writerow(transaction)
    
    print(f"Created {file_path}")
    
    # Recalculate analysis data with correct income
    income = sum(float(t['amount']) for t in transactions if float(t['amount']) > 0)
    expenses = abs(sum(float(t['amount']) for t in transactions if float(t['amount']) < 0))
    net_cash_flow = income - expenses
    savings_rate = round((net_cash_flow / income) * 100, 2) if income > 0 else 0
    
    # Update analysis data
    profile_data['analysis']['income'] = income
    profile_data['analysis']['expenses'] = expenses
    profile_data['analysis']['net_cash_flow'] = net_cash_flow
    profile_data['analysis']['savings_rate'] = savings_rate
    
    # Also save analysis and recommendations as JSON
    json_file_path = os.path.join(output_dir, f"{profile_name}_analysis.json")
    with open(json_file_path, 'w') as jsonfile:
        # Create a copy of the data without transactions (to save space)
        analysis_data = {
            'analysis': profile_data['analysis'],
            'recommendations': profile_data['recommendations']
        }
        json.dump(analysis_data, jsonfile, indent=2, default=str)
    
    print(f"Created {json_file_path}")

def main():
    """Generate and save sample data files for all profiles"""
    # Create sample_profiles directory inside the data directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_profiles")
    
    # Get all profile names
    profile_names = get_profile_names()
    
    # Generate and save each profile
    for profile_name in profile_names:
        print(f"Generating {profile_name} profile...")
        profile_data = get_sample_profile(profile_name)
        if profile_data:
            save_profile_to_csv(profile_name, profile_data, output_dir)
        else:
            print(f"Error: Could not generate {profile_name} profile")

if __name__ == "__main__":
    main()
