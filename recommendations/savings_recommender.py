"""
Savings Recommender - Generates personalized savings recommendations
"""

from typing import Dict, Any, List
import re


class SavingsRecommender:
    """Generates personalized savings recommendations based on spending analysis"""
    
    def __init__(self):
        """Initialize the savings recommender"""
        # Define recommendation strategies for different categories
        self.category_strategies = {
            'dining': self._dining_recommendations,
            'entertainment': self._entertainment_recommendations,
            'shopping': self._shopping_recommendations,
            'utilities': self._utilities_recommendations,
            'transportation': self._transportation_recommendations,
            'subscriptions': self._subscription_recommendations,
            'groceries': self._grocery_recommendations,
            'housing': self._housing_recommendations,
        }
        
        # Define thresholds for high spending in each category (monthly)
        self.spending_thresholds = {
            'dining': 300,  # $300/month on dining is considered high
            'entertainment': 200,
            'shopping': 400,
            'utilities': 350,
            'transportation': 300,
            'groceries': 500,
        }
    
    def recommend(self, spending_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate savings recommendations based on spending analysis
        
        Args:
            spending_analysis: Spending analysis results
            
        Returns:
            Dictionary with savings recommendations
        """
        recommendations = []
        total_potential_savings = 0
        
        # Extract relevant data from spending analysis
        spending_by_category = spending_analysis.get('spending_by_category', {})
        recurring_expenses = spending_analysis.get('recurring_expenses', [])
        transactions = spending_analysis.get('transactions', [])
        
        # Find subscription services from transactions
        subscription_services = self._identify_subscription_services(transactions, recurring_expenses)
        if subscription_services:
            # Add subscriptions as a category if not already present
            if 'subscriptions' not in spending_by_category:
                subscription_total = sum(s['average_amount'] for s in subscription_services)
                spending_by_category['subscriptions'] = subscription_total
        
        # Generate recommendations for high-spending categories
        for category, amount in spending_by_category.items():
            # Skip income and investment categories
            if category in ['income', 'investments']:
                continue
                
            # Check if spending is above threshold
            threshold = self.spending_thresholds.get(category, 0)
            if amount > threshold and threshold > 0:
                # Get category-specific recommendations
                if category in self.category_strategies:
                    category_recs = self.category_strategies[category](
                        amount, 
                        transactions, 
                        recurring_expenses,
                        subscription_services if category == 'subscriptions' else None
                    )
                    
                    recommendations.extend(category_recs)
                    
                    # Add up potential savings
                    for rec in category_recs:
                        total_potential_savings += rec.get('potential_savings', 0)
        
        # Add general recommendations if few category-specific ones were found
        if len(recommendations) < 3:
            general_recs = self._general_recommendations(spending_by_category)
            recommendations.extend(general_recs)
            
            # Add up potential savings
            for rec in general_recs:
                total_potential_savings += rec.get('potential_savings', 0)
        
        # Sort recommendations by potential savings (highest first)
        recommendations.sort(key=lambda x: x.get('potential_savings', 0), reverse=True)
        
        return {
            'recommendations': recommendations,
            'total_potential_savings': total_potential_savings
        }
    
    def _identify_subscription_services(
        self, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify subscription services from transactions and recurring expenses"""
        subscription_services = []
        
        # Common subscription keywords
        subscription_keywords = [
            'netflix', 'hulu', 'disney+', 'spotify', 'apple music', 'youtube', 
            'amazon prime', 'hbo', 'paramount+', 'peacock', 'subscription', 
            'membership', 'monthly', 'annual fee'
        ]
        
        # Check recurring expenses first
        for expense in recurring_expenses:
            description = expense['description'].lower()
            
            # Check if it matches subscription keywords
            if any(keyword in description for keyword in subscription_keywords):
                subscription_services.append(expense)
                continue
                
            # Check if it's a monthly or yearly recurring expense
            if expense['frequency'] in ['monthly', 'yearly']:
                # Check amount - subscriptions are usually under $50/month
                if expense['average_amount'] <= 50:
                    subscription_services.append(expense)
        
        return subscription_services
    
    def _dining_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate dining-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (30% of dining expenses)
        potential_savings = amount * 0.3
        
        # Count number of dining transactions
        dining_transactions = [t for t in transactions if t.get('category') == 'dining']
        dining_count = len(dining_transactions)
        
        # Check for food delivery services
        delivery_keywords = ['doordash', 'ubereats', 'grubhub', 'postmates', 'delivery']
        delivery_transactions = [
            t for t in dining_transactions 
            if any(keyword in t['description'].lower() for keyword in delivery_keywords)
        ]
        
        if delivery_transactions:
            delivery_amount = sum(abs(t['amount']) for t in delivery_transactions)
            delivery_count = len(delivery_transactions)
            
            if delivery_amount > 100:  # If spending more than $100 on delivery
                delivery_savings = delivery_amount * 0.7  # 70% savings by cooking instead
                
                recommendations.append({
                    'category': 'dining',
                    'description': f"You spent ${delivery_amount:.2f} on food delivery services "
                                  f"({delivery_count} orders). Consider cooking at home or picking up "
                                  f"takeout directly to save on delivery fees and markups.",
                    'potential_savings': delivery_savings
                })
                
                # Adjust potential savings for other dining recommendations
                potential_savings -= delivery_savings
        
        # General dining recommendation
        if potential_savings > 50:  # Only if potential savings is significant
            recommendations.append({
                'category': 'dining',
                'description': f"You spent ${amount:.2f} on dining out "
                              f"({dining_count} transactions). Consider preparing more meals at home, "
                              f"bringing lunch to work, or finding happy hour specials to reduce expenses.",
                'potential_savings': potential_savings
            })
        
        return recommendations
    
    def _entertainment_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate entertainment-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (25% of entertainment expenses)
        potential_savings = amount * 0.25
        
        recommendations.append({
            'category': 'entertainment',
            'description': f"You spent ${amount:.2f} on entertainment. Look for free or discounted "
                          f"entertainment options like community events, museum free days, or "
                          f"library resources. Consider sharing streaming subscriptions with family members.",
            'potential_savings': potential_savings
        })
        
        return recommendations
    
    def _shopping_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate shopping-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (20% of shopping expenses)
        potential_savings = amount * 0.2
        
        # Count number of shopping transactions
        shopping_transactions = [t for t in transactions if t.get('category') == 'shopping']
        shopping_count = len(shopping_transactions)
        
        # Check for online shopping
        online_keywords = ['amazon', 'ebay', 'etsy', 'walmart.com', 'target.com', 'online']
        online_transactions = [
            t for t in shopping_transactions 
            if any(keyword in t['description'].lower() for keyword in online_keywords)
        ]
        
        if online_transactions:
            online_amount = sum(abs(t['amount']) for t in online_transactions)
            online_count = len(online_transactions)
            
            if online_amount > 200:  # If spending more than $200 on online shopping
                online_savings = online_amount * 0.3  # 30% savings by reducing impulse buys
                
                recommendations.append({
                    'category': 'shopping',
                    'description': f"You made ${online_amount:.2f} in online purchases "
                                  f"({online_count} transactions). Consider implementing a 24-hour rule "
                                  f"before making non-essential purchases to reduce impulse buying.",
                    'potential_savings': online_savings
                })
                
                # Adjust potential savings for other shopping recommendations
                potential_savings -= online_savings
        
        # General shopping recommendation
        if potential_savings > 50:  # Only if potential savings is significant
            recommendations.append({
                'category': 'shopping',
                'description': f"You spent ${amount:.2f} on shopping "
                              f"({shopping_count} transactions). Create a shopping list before going to stores, "
                              f"look for sales and discounts, and consider buying used items when appropriate.",
                'potential_savings': potential_savings
            })
        
        return recommendations
    
    def _utilities_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate utilities-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (15% of utilities expenses)
        potential_savings = amount * 0.15
        
        recommendations.append({
            'category': 'utilities',
            'description': f"You spent ${amount:.2f} on utilities. Consider energy-saving measures like "
                          f"LED bulbs, programmable thermostats, and unplugging devices when not in use. "
                          f"Check if your providers offer better plans or if you can negotiate rates.",
            'potential_savings': potential_savings
        })
        
        return recommendations
    
    def _transportation_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate transportation-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (20% of transportation expenses)
        potential_savings = amount * 0.2
        
        # Count number of transportation transactions
        transportation_transactions = [t for t in transactions if t.get('category') == 'transportation']
        
        # Check for rideshare services
        rideshare_keywords = ['uber', 'lyft', 'taxi', 'cab']
        rideshare_transactions = [
            t for t in transportation_transactions 
            if any(keyword in t['description'].lower() for keyword in rideshare_keywords)
        ]
        
        if rideshare_transactions:
            rideshare_amount = sum(abs(t['amount']) for t in rideshare_transactions)
            rideshare_count = len(rideshare_transactions)
            
            if rideshare_amount > 100:  # If spending more than $100 on rideshares
                rideshare_savings = rideshare_amount * 0.5  # 50% savings by using alternatives
                
                recommendations.append({
                    'category': 'transportation',
                    'description': f"You spent ${rideshare_amount:.2f} on rideshare services "
                                  f"({rideshare_count} rides). Consider using public transportation, "
                                  f"carpooling, or planning trips in advance to reduce costs.",
                    'potential_savings': rideshare_savings
                })
                
                # Adjust potential savings for other transportation recommendations
                potential_savings -= rideshare_savings
        
        # Check for fuel expenses
        fuel_keywords = ['gas', 'fuel', 'shell', 'exxon', 'chevron', 'bp', 'marathon']
        fuel_transactions = [
            t for t in transportation_transactions 
            if any(keyword in t['description'].lower() for keyword in fuel_keywords)
        ]
        
        if fuel_transactions:
            fuel_amount = sum(abs(t['amount']) for t in fuel_transactions)
            
            if fuel_amount > 150:  # If spending more than $150 on fuel
                fuel_savings = fuel_amount * 0.15  # 15% savings by optimizing driving
                
                recommendations.append({
                    'category': 'transportation',
                    'description': f"You spent ${fuel_amount:.2f} on fuel. Consider combining errands, "
                                  f"maintaining proper tire pressure, and using apps to find the cheapest gas prices. "
                                  f"If possible, try carpooling or public transit for commuting.",
                    'potential_savings': fuel_savings
                })
                
                # Adjust potential savings for other transportation recommendations
                potential_savings -= fuel_savings
        
        # General transportation recommendation
        if potential_savings > 30:  # Only if potential savings is significant
            recommendations.append({
                'category': 'transportation',
                'description': f"You spent ${amount:.2f} on transportation. Look for ways to optimize "
                              f"your transportation costs, such as planning routes efficiently, "
                              f"maintaining your vehicle properly, or using alternative transportation methods.",
                'potential_savings': potential_savings
            })
        
        return recommendations
    
    def _subscription_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        subscription_services: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate subscription-specific recommendations"""
        recommendations = []
        
        if not subscription_services:
            return recommendations
        
        # Calculate total subscription costs
        total_subscription_cost = sum(s['average_amount'] for s in subscription_services)
        
        # Calculate potential savings (30% of subscription expenses)
        potential_savings = total_subscription_cost * 0.3
        
        # Group similar subscriptions
        streaming_services = []
        other_subscriptions = []
        
        streaming_keywords = ['netflix', 'hulu', 'disney', 'hbo', 'paramount', 'peacock', 'apple tv', 'amazon prime video']
        music_keywords = ['spotify', 'apple music', 'pandora', 'tidal', 'youtube music']
        
        for subscription in subscription_services:
            description = subscription['description'].lower()
            
            if any(keyword in description for keyword in streaming_keywords):
                streaming_services.append(subscription)
            elif any(keyword in description for keyword in music_keywords):
                streaming_services.append(subscription)
            else:
                other_subscriptions.append(subscription)
        
        # Recommendations for streaming services
        if len(streaming_services) >= 3:
            streaming_cost = sum(s['average_amount'] for s in streaming_services)
            streaming_savings = streaming_cost * 0.5  # 50% savings by reducing services
            
            recommendations.append({
                'category': 'subscriptions',
                'description': f"You have {len(streaming_services)} streaming subscriptions "
                              f"costing ${streaming_cost:.2f} per month. Consider rotating subscriptions "
                              f"(subscribe to one service at a time) or using family plans to reduce costs.",
                'potential_savings': streaming_savings
            })
            
            # Adjust potential savings
            potential_savings -= streaming_savings
        
        # General subscription recommendation
        if potential_savings > 10:  # Only if potential savings is significant
            recommendations.append({
                'category': 'subscriptions',
                'description': f"You're spending ${total_subscription_cost:.2f} on subscription services. "
                              f"Review all your subscriptions and cancel those you rarely use. "
                              f"Look for annual payment options which often provide discounts.",
                'potential_savings': potential_savings
            })
        
        return recommendations
    
    def _grocery_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate grocery-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (15% of grocery expenses)
        potential_savings = amount * 0.15
        
        recommendations.append({
            'category': 'groceries',
            'description': f"You spent ${amount:.2f} on groceries. Consider meal planning, "
                          f"buying in bulk, using store loyalty programs, and choosing store brands "
                          f"to reduce your grocery expenses. Also, check for digital coupons before shopping.",
            'potential_savings': potential_savings
        })
        
        return recommendations
    
    def _housing_recommendations(
        self, 
        amount: float, 
        transactions: List[Dict[str, Any]], 
        recurring_expenses: List[Dict[str, Any]],
        *args
    ) -> List[Dict[str, Any]]:
        """Generate housing-specific recommendations"""
        recommendations = []
        
        # Calculate potential savings (5% of housing expenses)
        potential_savings = amount * 0.05
        
        recommendations.append({
            'category': 'housing',
            'description': f"Your housing expenses are ${amount:.2f}. While this is typically a fixed cost, "
                          f"you might consider negotiating rent upon renewal, refinancing your mortgage if "
                          f"interest rates have dropped, or reviewing your insurance policies for better rates.",
            'potential_savings': potential_savings
        })
        
        return recommendations
    
    def _general_recommendations(self, spending_by_category: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate general savings recommendations"""
        recommendations = []
        
        # Calculate total expenses
        total_expenses = sum(amount for category, amount in spending_by_category.items() 
                             if category not in ['income', 'investments'])
        
        # General savings recommendation
        recommendations.append({
            'category': 'general',
            'description': "Consider implementing the 50/30/20 budget rule: 50% of income for needs, "
                          "30% for wants, and 20% for savings and debt repayment. Track your expenses "
                          "regularly to identify areas where you can cut back.",
            'potential_savings': total_expenses * 0.05  # Estimate 5% potential savings
        })
        
        # Debt management recommendation
        if 'debt' in spending_by_category and spending_by_category['debt'] > 0:
            debt_amount = spending_by_category['debt']
            
            recommendations.append({
                'category': 'debt',
                'description': f"You're paying ${debt_amount:.2f} towards debt. Consider consolidating "
                              f"high-interest debt or negotiating for lower interest rates. Prioritize "
                              f"paying off high-interest debt first while making minimum payments on others.",
                'potential_savings': debt_amount * 0.1  # Estimate 10% potential savings
            })
        
        # Automated savings recommendation
        recommendations.append({
            'category': 'savings',
            'description': "Set up automatic transfers to a savings account on payday. Even small "
                          "amounts add up over time. Consider using a high-yield savings account "
                          "to earn more interest on your emergency fund.",
            'potential_savings': total_expenses * 0.03  # Estimate 3% potential savings
        })
        
        return recommendations
