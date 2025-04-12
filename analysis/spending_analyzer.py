"""
Spending Analyzer - Categorizes transactions and analyzes spending patterns
"""

import os
import json
import datetime
import re
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from collections import defaultdict

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class SpendingAnalyzer:
    """Analyzes spending patterns and categorizes transactions"""
    
    # Default spending categories
    DEFAULT_CATEGORIES = {
        'housing': ['rent', 'mortgage', 'property tax', 'hoa', 'maintenance', 'repair'],
        'utilities': ['electric', 'water', 'gas', 'internet', 'phone', 'cable', 'utility'],
        'groceries': ['grocery', 'supermarket', 'food', 'market'],
        'dining': ['restaurant', 'cafe', 'coffee', 'bar', 'grubhub', 'doordash', 'ubereats', 'dining'],
        'transportation': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'transit', 'parking', 'toll', 'car', 'auto', 'vehicle'],
        'entertainment': ['movie', 'theatre', 'concert', 'netflix', 'hulu', 'spotify', 'disney', 'subscription', 'game'],
        'shopping': ['amazon', 'walmart', 'target', 'costco', 'shop', 'store', 'retail', 'clothing', 'electronics'],
        'health': ['doctor', 'hospital', 'medical', 'pharmacy', 'health', 'fitness', 'gym', 'insurance'],
        'education': ['tuition', 'school', 'college', 'university', 'course', 'book', 'education'],
        'travel': ['hotel', 'flight', 'airline', 'airbnb', 'vacation', 'travel'],
        'personal': ['haircut', 'salon', 'spa', 'beauty', 'personal'],
        'income': ['salary', 'deposit', 'paycheck', 'payment received', 'direct deposit', 'income'],
        'investments': ['investment', 'dividend', 'interest', 'stock', 'bond', 'etf', 'mutual fund'],
        'debt': ['credit card', 'loan', 'debt', 'interest payment'],
        'insurance': ['insurance', 'premium'],
        'taxes': ['tax', 'irs', 'state tax'],
        'gifts_donations': ['gift', 'donation', 'charity', 'nonprofit'],
        'business': ['business', 'office', 'professional', 'service'],
        'other': []  # Catch-all category
    }
    
    def __init__(self, custom_categories_path: Optional[str] = None):
        """
        Initialize the spending analyzer
        
        Args:
            custom_categories_path: Optional path to a JSON file with custom categories
        """
        # Load categories
        self.categories = self.DEFAULT_CATEGORIES.copy()
        
        # Load custom categories if provided
        if custom_categories_path:
            self._load_custom_categories(custom_categories_path)
        
        # Initialize TFIDF vectorizer for text similarity
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        
        # Prepare category keywords for vectorization
        self.category_keywords = {}
        for category, keywords in self.categories.items():
            if keywords:
                self.category_keywords[category] = ' '.join(keywords)
        
        # Vectorize category keywords
        if self.category_keywords:
            self.category_vectors = self.vectorizer.fit_transform(self.category_keywords.values())
            self.category_names = list(self.category_keywords.keys())
        else:
            self.category_vectors = None
            self.category_names = []
    
    def analyze(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze transactions and categorize spending
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Dictionary with spending analysis results
        """
        # Categorize transactions
        categorized_transactions = self._categorize_transactions(transactions)
        
        # Group transactions by category
        category_spending = defaultdict(list)
        for transaction in categorized_transactions:
            category = transaction.get('category', 'other')
            # Only include expenses (negative amounts)
            if transaction['amount'] < 0:
                category_spending[category].append(transaction)
        
        # Calculate total spending by category
        spending_by_category = {}
        for category, transactions in category_spending.items():
            total = sum(t['amount'] for t in transactions)
            spending_by_category[category] = abs(total)  # Convert to positive for display
        
        # Calculate monthly spending trends
        monthly_spending = self._calculate_monthly_spending(categorized_transactions)
        
        # Identify recurring expenses
        recurring_expenses = self._identify_recurring_expenses(categorized_transactions)
        
        # Identify unusual spending
        unusual_spending = self._identify_unusual_spending(categorized_transactions, monthly_spending)
        
        # Calculate income vs. expenses
        income = sum(t['amount'] for t in categorized_transactions if t['amount'] > 0)
        expenses = abs(sum(t['amount'] for t in categorized_transactions if t['amount'] < 0))
        
        # Prepare analysis results
        analysis_results = {
            'transactions': categorized_transactions,
            'spending_by_category': spending_by_category,
            'monthly_spending': monthly_spending,
            'recurring_expenses': recurring_expenses,
            'unusual_spending': unusual_spending,
            'income': income,
            'expenses': expenses,
            'net_cash_flow': income - expenses,
            'savings_rate': (income - expenses) / income if income > 0 else 0,
            'top_spending_categories': self._get_top_spending_categories(spending_by_category, 5),
            'top_merchants': self._get_top_merchants(categorized_transactions, 5)
        }
        
        return analysis_results
    
    def _load_custom_categories(self, custom_categories_path: str) -> None:
        """Load custom categories from a JSON file"""
        try:
            with open(custom_categories_path, 'r') as f:
                custom_categories = json.load(f)
                
            # Validate and merge custom categories
            for category, keywords in custom_categories.items():
                if isinstance(keywords, list):
                    if category in self.categories:
                        # Merge with existing category
                        self.categories[category].extend(keywords)
                    else:
                        # Add new category
                        self.categories[category] = keywords
        except Exception as e:
            print(f"Warning: Failed to load custom categories: {e}")
    
    def _categorize_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Categorize transactions based on their descriptions"""
        categorized_transactions = []
        
        # Extract descriptions for vectorization
        descriptions = [t['description'].lower() for t in transactions]
        
        # Vectorize descriptions if we have category vectors
        if self.category_vectors is not None and descriptions:
            try:
                # Transform descriptions using the same vectorizer
                desc_vectors = self.vectorizer.transform(descriptions)
                
                # Calculate similarity between descriptions and category keywords
                similarities = cosine_similarity(desc_vectors, self.category_vectors)
                
                # Assign categories based on highest similarity
                for i, transaction in enumerate(transactions):
                    transaction_copy = transaction.copy()
                    
                    # Check if transaction already has a category
                    if 'category' not in transaction_copy:
                        # Find the most similar category
                        max_sim_idx = np.argmax(similarities[i])
                        max_sim = similarities[i][max_sim_idx]
                        
                        # Only assign category if similarity is above threshold
                        if max_sim > 0.1:
                            transaction_copy['category'] = self.category_names[max_sim_idx]
                        else:
                            # Use rule-based categorization as fallback
                            transaction_copy['category'] = self._rule_based_categorization(transaction_copy)
                    
                    categorized_transactions.append(transaction_copy)
            except Exception:
                # Fallback to rule-based categorization if vectorization fails
                for transaction in transactions:
                    transaction_copy = transaction.copy()
                    if 'category' not in transaction_copy:
                        transaction_copy['category'] = self._rule_based_categorization(transaction_copy)
                    categorized_transactions.append(transaction_copy)
        else:
            # Use rule-based categorization if no category vectors
            for transaction in transactions:
                transaction_copy = transaction.copy()
                if 'category' not in transaction_copy:
                    transaction_copy['category'] = self._rule_based_categorization(transaction_copy)
                categorized_transactions.append(transaction_copy)
        
        return categorized_transactions
    
    def _rule_based_categorization(self, transaction: Dict[str, Any]) -> str:
        """Categorize a transaction using rule-based approach"""
        description = transaction['description'].lower()
        
        # Handle income (positive amounts)
        if transaction['amount'] > 0:
            for keyword in self.categories.get('income', []):
                if keyword.lower() in description:
                    return 'income'
        
        # Check each category for keyword matches
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in description:
                    return category
        
        # Default to 'other' if no match found
        return 'other'
    
    def _calculate_monthly_spending(self, transactions: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Calculate monthly spending by category"""
        monthly_spending = defaultdict(lambda: defaultdict(float))
        
        for transaction in transactions:
            # Skip income (positive amounts)
            if transaction['amount'] >= 0:
                continue
                
            date = transaction['date']
            category = transaction.get('category', 'other')
            amount = abs(transaction['amount'])  # Convert to positive for display
            
            # Create month key (YYYY-MM)
            month_key = f"{date.year}-{date.month:02d}"
            
            # Add to monthly spending
            monthly_spending[month_key][category] += amount
        
        # Convert defaultdict to regular dict for serialization
        return {
            month: dict(categories) for month, categories in monthly_spending.items()
        }
    
    def _identify_recurring_expenses(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify recurring expenses based on similar descriptions and amounts"""
        # Group transactions by similar descriptions
        description_groups = defaultdict(list)
        
        for transaction in transactions:
            # Skip income (positive amounts)
            if transaction['amount'] >= 0:
                continue
                
            # Simplify description for grouping
            simple_desc = self._simplify_description(transaction['description'])
            description_groups[simple_desc].append(transaction)
        
        recurring_expenses = []
        
        for simple_desc, group in description_groups.items():
            # Only consider groups with multiple transactions
            if len(group) < 2:
                continue
                
            # Sort by date
            sorted_group = sorted(group, key=lambda t: t['date'])
            
            # Check for similar amounts
            amounts = [t['amount'] for t in sorted_group]
            amount_mean = np.mean(amounts)
            amount_std = np.std(amounts)
            
            # If amounts are similar (low standard deviation relative to mean)
            if abs(amount_std / amount_mean) < 0.2 or amount_std < 5:
                # Calculate average time between transactions
                dates = [t['date'] for t in sorted_group]
                intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                
                if intervals:
                    avg_interval = sum(intervals) / len(intervals)
                    
                    # Check if the interval suggests monthly, weekly, or yearly recurrence
                    frequency = None
                    if 25 <= avg_interval <= 35:
                        frequency = 'monthly'
                    elif 6 <= avg_interval <= 8:
                        frequency = 'weekly'
                    elif 350 <= avg_interval <= 380:
                        frequency = 'yearly'
                    
                    if frequency:
                        recurring_expenses.append({
                            'description': sorted_group[0]['description'],
                            'category': sorted_group[0].get('category', 'other'),
                            'average_amount': abs(amount_mean),  # Convert to positive for display
                            'frequency': frequency,
                            'transactions': sorted_group
                        })
        
        return recurring_expenses
    
    def _identify_unusual_spending(
        self, 
        transactions: List[Dict[str, Any]], 
        monthly_spending: Dict[str, Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """Identify unusual spending patterns"""
        unusual_spending = []
        
        # Skip if not enough monthly data
        if len(monthly_spending) < 2:
            return unusual_spending
        
        # Calculate average monthly spending by category
        avg_monthly_by_category = defaultdict(list)
        
        for month, categories in monthly_spending.items():
            for category, amount in categories.items():
                avg_monthly_by_category[category].append(amount)
        
        # Calculate mean and standard deviation for each category
        category_stats = {}
        for category, amounts in avg_monthly_by_category.items():
            if len(amounts) >= 2:  # Need at least 2 months to calculate stats
                mean = np.mean(amounts)
                std = np.std(amounts)
                category_stats[category] = {'mean': mean, 'std': std}
        
        # Check each month for unusual spending
        for month, categories in monthly_spending.items():
            month_unusual = []
            
            for category, amount in categories.items():
                if category in category_stats:
                    stats = category_stats[category]
                    
                    # If spending is more than 1.5 standard deviations above mean
                    if amount > stats['mean'] + 1.5 * stats['std'] and amount > 50:  # Minimum threshold
                        month_unusual.append({
                            'category': category,
                            'amount': amount,
                            'average': stats['mean'],
                            'percent_increase': (amount - stats['mean']) / stats['mean'] * 100
                        })
            
            if month_unusual:
                unusual_spending.append({
                    'month': month,
                    'unusual_categories': month_unusual
                })
        
        return unusual_spending
    
    def _get_top_spending_categories(self, spending_by_category: Dict[str, float], limit: int) -> List[Dict[str, Any]]:
        """Get top spending categories"""
        # Sort categories by spending amount (descending)
        sorted_categories = sorted(
            spending_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top N categories
        return [
            {'category': category, 'amount': amount}
            for category, amount in sorted_categories[:limit]
        ]
    
    def _get_top_merchants(self, transactions: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Get top merchants by spending amount"""
        # Group transactions by merchant
        merchant_spending = defaultdict(float)
        
        for transaction in transactions:
            # Skip income (positive amounts)
            if transaction['amount'] >= 0:
                continue
                
            merchant = self._extract_merchant(transaction['description'])
            merchant_spending[merchant] += abs(transaction['amount'])
        
        # Sort merchants by spending amount (descending)
        sorted_merchants = sorted(
            merchant_spending.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top N merchants
        return [
            {'merchant': merchant, 'amount': amount}
            for merchant, amount in sorted_merchants[:limit]
        ]
    
    def _simplify_description(self, description: str) -> str:
        """Simplify transaction description for grouping similar transactions"""
        # Convert to lowercase
        desc = description.lower()
        
        # Remove common prefixes/suffixes and numbers
        desc = re.sub(r'#\d+', '', desc)
        desc = re.sub(r'\d{4}-\d{2}-\d{2}', '', desc)
        desc = re.sub(r'\d+\.\d+', '', desc)
        
        # Remove common transaction words
        common_words = ['payment', 'purchase', 'transaction', 'debit', 'credit']
        for word in common_words:
            desc = desc.replace(word, '')
        
        # Remove extra whitespace
        desc = ' '.join(desc.split())
        
        return desc
    
    def _extract_merchant(self, description: str) -> str:
        """Extract merchant name from transaction description"""
        # This is a simplified approach and may need to be customized
        # for specific bank statement formats
        
        # Remove common prefixes
        prefixes = ['purchase ', 'payment to ', 'pos purchase ', 'debit card purchase ']
        desc = description.lower()
        
        for prefix in prefixes:
            if desc.startswith(prefix):
                desc = desc[len(prefix):]
                break
        
        # Extract first part of description (likely the merchant)
        parts = desc.split()
        if parts:
            # Use first 3 words or fewer if description is shorter
            merchant = ' '.join(parts[:min(3, len(parts))])
            return merchant.title()  # Convert to title case
        
        return description  # Fallback to original description
