"""
Investment Recommender - Generates personalized investment recommendations
"""

from typing import Dict, Any, List
import datetime


class InvestmentRecommender:
    """Generates personalized investment recommendations based on spending analysis and savings potential"""
    
    def __init__(self):
        """Initialize the investment recommender"""
        # Define investment options with risk levels and potential returns
        self.investment_options = {
            'low_risk': [
                {
                    'title': 'High-Yield Savings Account',
                    'description': 'FDIC-insured savings accounts with higher interest rates than traditional banks. '
                                  'Ideal for emergency funds and short-term savings goals.',
                    'potential_return': '1-2% annually',
                    'min_investment': 0,
                    'liquidity': 'High',
                    'risk_level': 'Very Low'
                },
                {
                    'title': 'Certificates of Deposit (CDs)',
                    'description': 'Time deposits that offer higher interest rates in exchange for leaving your money '
                                  'untouched for a fixed period (typically 3 months to 5 years).',
                    'potential_return': '1-3% annually',
                    'min_investment': 500,
                    'liquidity': 'Low to Medium',
                    'risk_level': 'Very Low'
                },
                {
                    'title': 'Treasury Securities',
                    'description': 'Government bonds, notes, and bills backed by the U.S. Treasury. '
                                  'These are considered among the safest investments available.',
                    'potential_return': '1-3% annually',
                    'min_investment': 100,
                    'liquidity': 'Medium',
                    'risk_level': 'Very Low'
                }
            ],
            'medium_risk': [
                {
                    'title': 'Bond Index Funds',
                    'description': 'Mutual funds or ETFs that track bond market indices. '
                                  'These provide diversification across many bonds with lower fees.',
                    'potential_return': '2-4% annually',
                    'min_investment': 1000,
                    'liquidity': 'Medium to High',
                    'risk_level': 'Low to Medium'
                },
                {
                    'title': 'Balanced Mutual Funds',
                    'description': 'Funds that invest in a mix of stocks and bonds to provide both growth potential '
                                  'and income with moderate risk.',
                    'potential_return': '4-6% annually',
                    'min_investment': 1000,
                    'liquidity': 'Medium to High',
                    'risk_level': 'Medium'
                },
                {
                    'title': 'Dividend Stock ETFs',
                    'description': 'Exchange-traded funds that focus on stocks paying regular dividends, '
                                  'providing both income and growth potential.',
                    'potential_return': '3-5% annually plus potential growth',
                    'min_investment': 1000,
                    'liquidity': 'High',
                    'risk_level': 'Medium'
                }
            ],
            'high_risk': [
                {
                    'title': 'Stock Index Funds',
                    'description': 'Mutual funds or ETFs that track stock market indices like the S&P 500. '
                                  'These provide broad market exposure with lower fees than actively managed funds.',
                    'potential_return': '7-10% annually (historical average)',
                    'min_investment': 1000,
                    'liquidity': 'High',
                    'risk_level': 'Medium to High'
                },
                {
                    'title': 'Growth Stock Funds',
                    'description': 'Funds that invest in companies expected to grow faster than average. '
                                  'These offer higher potential returns but with increased volatility.',
                    'potential_return': '8-12% annually (potential)',
                    'min_investment': 2000,
                    'liquidity': 'High',
                    'risk_level': 'High'
                },
                {
                    'title': 'Real Estate Investment Trusts (REITs)',
                    'description': 'Companies that own, operate, or finance income-producing real estate. '
                                  'REITs provide exposure to real estate without directly buying property.',
                    'potential_return': '5-8% annually plus potential growth',
                    'min_investment': 1000,
                    'liquidity': 'High',
                    'risk_level': 'Medium to High'
                }
            ]
        }
        
        # Define retirement account options
        self.retirement_options = [
            {
                'title': '401(k) or 403(b) Employer Plans',
                'description': 'If your employer offers a retirement plan, especially with matching contributions, '
                              'this should be your first investment priority. Contribute at least enough to get the full match.',
                'potential_return': 'Varies based on investment choices, employer match is immediate 100% return',
                'tax_advantage': 'Tax-deferred growth, potential employer match, contributions may be tax-deductible'
            },
            {
                'title': 'Traditional IRA',
                'description': 'Individual Retirement Account that allows tax-deductible contributions (subject to income limits) '
                              'and tax-deferred growth until retirement.',
                'potential_return': 'Varies based on investment choices',
                'tax_advantage': 'Tax-deductible contributions (income limits apply), tax-deferred growth'
            },
            {
                'title': 'Roth IRA',
                'description': 'Individual Retirement Account funded with after-tax dollars. Qualified withdrawals in retirement '
                              'are completely tax-free, including all earnings.',
                'potential_return': 'Varies based on investment choices',
                'tax_advantage': 'Tax-free growth and qualified withdrawals, no required minimum distributions'
            }
        ]
        
        # Define debt payoff as an investment option
        self.debt_payoff = {
            'title': 'High-Interest Debt Payoff',
            'description': 'Paying off high-interest debt (like credit cards) is often the best "investment" you can make. '
                          'A credit card with 18% interest means you get an immediate, guaranteed 18% return by paying it off.',
            'potential_return': 'Equal to the interest rate on your debt (often 10-25% for credit cards)',
            'risk_level': 'None (guaranteed return)'
        }
    
    def recommend(
        self, 
        spending_analysis: Dict[str, Any], 
        savings_recommendations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate investment recommendations based on spending analysis and savings potential
        
        Args:
            spending_analysis: Spending analysis results
            savings_recommendations: Savings recommendations
            
        Returns:
            Dictionary with investment recommendations
        """
        recommendations = []
        
        # Extract relevant data
        income = spending_analysis.get('income', 0)
        expenses = spending_analysis.get('expenses', 0)
        net_cash_flow = spending_analysis.get('net_cash_flow', 0)
        savings_rate = spending_analysis.get('savings_rate', 0)
        potential_savings = savings_recommendations.get('total_potential_savings', 0)
        
        # Calculate investment capacity
        current_monthly_surplus = max(0, net_cash_flow)
        potential_monthly_surplus = current_monthly_surplus + potential_savings
        
        # Check for high-interest debt
        has_debt = 'debt' in spending_analysis.get('spending_by_category', {})
        debt_amount = spending_analysis.get('spending_by_category', {}).get('debt', 0)
        
        # 1. First priority: Emergency Fund
        emergency_fund_recommendation = self._emergency_fund_recommendation(
            income, expenses, current_monthly_surplus
        )
        if emergency_fund_recommendation:
            recommendations.append(emergency_fund_recommendation)
        
        # 2. Second priority: High-interest debt payoff
        if has_debt and debt_amount > 0:
            recommendations.append(self.debt_payoff)
        
        # 3. Third priority: Retirement accounts
        retirement_recommendation = self._retirement_account_recommendation(
            income, current_monthly_surplus, potential_monthly_surplus
        )
        if retirement_recommendation:
            recommendations.append(retirement_recommendation)
        
        # 4. Fourth priority: Additional investments based on risk profile
        risk_profile = self._determine_risk_profile(spending_analysis)
        
        investment_recommendations = self._investment_options_recommendation(
            risk_profile, potential_monthly_surplus
        )
        recommendations.extend(investment_recommendations)
        
        # 5. Add general investment advice
        general_advice = self._general_investment_advice(
            current_monthly_surplus, potential_monthly_surplus
        )
        recommendations.append(general_advice)
        
        return {
            'recommendations': recommendations,
            'current_monthly_surplus': current_monthly_surplus,
            'potential_monthly_surplus': potential_monthly_surplus,
            'risk_profile': risk_profile
        }
    
    def _emergency_fund_recommendation(
        self, 
        income: float, 
        expenses: float, 
        monthly_surplus: float
    ) -> Dict[str, Any]:
        """Generate emergency fund recommendation"""
        # Calculate target emergency fund (3-6 months of expenses)
        target_emergency_fund = expenses * 3  # Start with 3 months
        
        # Calculate how long it would take to build the emergency fund
        months_to_build = target_emergency_fund / monthly_surplus if monthly_surplus > 0 else float('inf')
        
        description = (
            f"Before investing, establish an emergency fund of 3-6 months of expenses (${target_emergency_fund:,.2f}). "
            f"Keep this money in a high-yield savings account for easy access in case of unexpected expenses or income loss. "
        )
        
        if monthly_surplus > 0:
            if months_to_build <= 12:
                description += f"At your current savings rate, you could build this fund in about {int(months_to_build)} months."
            else:
                description += (
                    f"At your current savings rate, it would take over {int(months_to_build)} months to build this fund. "
                    f"Consider implementing the savings recommendations to accelerate this process."
                )
        else:
            description += (
                "Your current income doesn't exceed your expenses, making it difficult to build an emergency fund. "
                "Focus on reducing expenses or increasing income before investing."
            )
        
        return {
            'title': 'Build an Emergency Fund',
            'description': description,
            'priority': 'High',
            'potential_return': 'Peace of mind and financial security'
        }
    
    def _retirement_account_recommendation(
        self, 
        income: float, 
        current_monthly_surplus: float,
        potential_monthly_surplus: float
    ) -> Dict[str, Any]:
        """Generate retirement account recommendation"""
        # Choose the most appropriate retirement option based on income and surplus
        
        # For simplicity, recommend 401(k) if surplus is significant
        if current_monthly_surplus > 500 or potential_monthly_surplus > 500:
            return self.retirement_options[0]  # 401(k) or 403(b)
        
        # Otherwise, recommend Roth IRA for its flexibility
        return self.retirement_options[2]  # Roth IRA
    
    def _determine_risk_profile(self, spending_analysis: Dict[str, Any]) -> str:
        """Determine risk profile based on spending patterns"""
        # This is a simplified approach - a real system would use more factors
        
        # Extract relevant data
        income = spending_analysis.get('income', 0)
        expenses = spending_analysis.get('expenses', 0)
        savings_rate = spending_analysis.get('savings_rate', 0)
        
        # Check for high-risk spending patterns
        spending_by_category = spending_analysis.get('spending_by_category', {})
        
        # High entertainment or shopping spending might indicate higher risk tolerance
        entertainment_ratio = spending_by_category.get('entertainment', 0) / expenses if expenses > 0 else 0
        shopping_ratio = spending_by_category.get('shopping', 0) / expenses if expenses > 0 else 0
        
        # Determine risk profile
        if savings_rate > 0.3 and (entertainment_ratio > 0.1 or shopping_ratio > 0.15):
            # High savings rate and discretionary spending suggests higher risk tolerance
            return 'high_risk'
        elif savings_rate > 0.15 or (entertainment_ratio > 0.08 or shopping_ratio > 0.1):
            # Moderate savings rate or discretionary spending suggests medium risk tolerance
            return 'medium_risk'
        else:
            # Low savings rate or conservative spending suggests lower risk tolerance
            return 'low_risk'
    
    def _investment_options_recommendation(
        self, 
        risk_profile: str, 
        monthly_surplus: float
    ) -> List[Dict[str, Any]]:
        """Generate investment options based on risk profile"""
        # Select investment options based on risk profile
        if risk_profile in self.investment_options:
            options = self.investment_options[risk_profile]
            
            # Filter options based on monthly surplus
            annual_investment = monthly_surplus * 12
            suitable_options = [
                option for option in options 
                if option['min_investment'] <= annual_investment
            ]
            
            # If no suitable options, return low risk options
            if not suitable_options and risk_profile != 'low_risk':
                return self._investment_options_recommendation('low_risk', monthly_surplus)
            
            return suitable_options[:2]  # Return top 2 options
        
        # Default to low risk if profile not found
        return self.investment_options['low_risk'][:2]
    
    def _general_investment_advice(
        self, 
        current_monthly_surplus: float, 
        potential_monthly_surplus: float
    ) -> Dict[str, Any]:
        """Generate general investment advice"""
        if current_monthly_surplus < 100 and potential_monthly_surplus < 200:
            # Very limited investment capacity
            return {
                'title': 'Focus on Increasing Investment Capacity',
                'description': "Your current financial situation limits your investment options. "
                              "Focus on implementing the savings recommendations to increase your "
                              "investment capacity. Even small, regular investments can grow significantly "
                              "over time thanks to compound interest.",
                'priority': 'High'
            }
        elif current_monthly_surplus < 300 and potential_monthly_surplus < 500:
            # Limited investment capacity
            return {
                'title': 'Start Small and Consistent',
                'description': "With your current surplus, focus on consistent, small investments. "
                              "Consider setting up automatic transfers to a low-cost index fund or ETF. "
                              "Remember that consistency is key - even $50-100 per month can grow significantly "
                              "over time through compound interest.",
                'priority': 'Medium'
            }
        else:
            # Decent investment capacity
            return {
                'title': 'Diversify Your Investments',
                'description': "With your investment capacity, you can build a diversified portfolio. "
                              "Consider a mix of the recommended investments based on your goals and risk tolerance. "
                              "Remember to periodically rebalance your portfolio and adjust your strategy as your "
                              "financial situation changes. Consider consulting with a financial advisor for personalized advice.",
                'priority': 'Medium'
            }
        
