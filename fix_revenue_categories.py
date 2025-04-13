#!/usr/bin/env python3
"""
Fix Revenue categories in sample profiles CSV files
"""

import os
import csv
import sys

def fix_revenue_categories(file_path):
    """Convert Revenue category to Income in a CSV file"""
    print(f"Processing {file_path}...")
    
    # Read the file
    rows = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Get the header
        rows.append(header)
        
        # Read and modify rows
        revenue_count = 0
        for row in reader:
            if len(row) >= 4 and row[3] == 'Revenue':
                row[3] = 'Income'
                revenue_count += 1
            rows.append(row)
    
    # Write back to the file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print(f"Converted {revenue_count} 'Revenue' entries to 'Income' in {file_path}")

def main():
    """Process all business profile CSV files"""
    profile_dir = os.path.join('data', 'sample_profiles')
    business_profiles = [
        os.path.join(profile_dir, 'restaurant_business.csv'),
        os.path.join(profile_dir, 'tech_startup.csv'),
        os.path.join(profile_dir, 'retail_store.csv'),
        os.path.join(profile_dir, 'small_business.csv')
    ]
    
    for profile in business_profiles:
        if os.path.exists(profile):
            fix_revenue_categories(profile)
        else:
            print(f"Warning: {profile} not found")

if __name__ == "__main__":
    main()
