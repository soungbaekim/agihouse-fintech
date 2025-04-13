"""
OpenAI Chat Service for Finance Analyzer
"""

import os
import json
from typing import Dict, List, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIChatService:
    """
    Service for interacting with OpenAI's API to provide financial insights
    and recommendations based on user data
    """
    
    def __init__(self):
        """Initialize the OpenAI chat service"""
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # System message template for financial advisor
        self.system_message = """
        You are an AI financial advisor for the Finance Analyzer application. 
        Your role is to provide personalized financial insights, recommendations, and answer questions 
        based on the user's financial data. Be helpful, clear, and concise in your responses.
        
        The user's financial data will be provided to you in each conversation. This includes:
        1. Summary financial metrics (income, expenses, cash flow)
        2. Detailed spending by category
        3. Top merchants where money is spent
        4. Current savings and investment recommendations
        5. Specific transaction data with dates, descriptions, amounts, and categories
        
        When analyzing the user's financial situation, refer to specific transactions and patterns in their data.
        For example, instead of saying "You spend a lot on dining", say "I notice you spent $X at Restaurant Y on [date]"
        or "Your largest dining expense was $X at Restaurant Y". Use this specific information to make your advice 
        more relevant and actionable.
        
        Key areas to focus on:
        1. Spending patterns and anomalies (identify specific high-value transactions)
        2. Savings opportunities (suggest specific areas where spending could be reduced based on transaction data)
        3. Budget optimization (analyze spending frequency and timing from transaction dates)
        4. Debt management strategies (identify recurring payments and suggest optimization)
        5. Investment suggestions based on their financial situation (consider cash flow patterns)
        
        The user is viewing the Finance Analyzer dashboard, which shows their financial data visualizations.
        They might be on different pages (transactions, recommendations, category details), and your response
        should be tailored to what they're currently viewing.
        
        Keep your responses focused on financial matters and avoid giving advice outside your expertise.
        """
    
    def _format_financial_data(self, financial_data: Dict[str, Any]) -> str:
        """
        Format financial data for the AI in a structured way
        
        Args:
            financial_data (Dict[str, Any]): User's financial data
        
        Returns:
            str: Formatted financial data as context
        """
        try:
            context = "USER FINANCIAL DATA SUMMARY:\n\n"
            
            # Add basic financial metrics
            income = financial_data.get('income', 0)
            expenses = financial_data.get('expenses', 0)
            net_cash_flow = financial_data.get('net_cash_flow', 0)
            savings_rate = financial_data.get('savings_rate', 0)
            
            context += f"Income: ${income:.2f}\n"
            context += f"Expenses: ${expenses:.2f}\n"
            context += f"Net Cash Flow: ${net_cash_flow:.2f}\n"
            context += f"Savings Rate: {savings_rate:.1f}%\n\n"
            
            # Add top spending categories
            top_categories = financial_data.get('top_categories', [])
            if top_categories:
                context += "TOP SPENDING CATEGORIES:\n"
                for category in top_categories:
                    context += f"- {category['category'].title()}: ${float(category['amount']):.2f}\n"
                context += "\n"
            
            # Add potential savings information
            total_savings_potential = financial_data.get('total_savings_potential', 0)
            if total_savings_potential:
                context += f"Potential Monthly Savings: ${float(total_savings_potential):.2f}\n\n"
            
            # Add transaction data and insights
            transactions = financial_data.get('transactions', [])
            if transactions:
                # Calculate spending patterns
                monthly_totals = {}
                category_totals = {}
                merchants = {}
                
                for tx in transactions:
                    # Extract transaction details
                    date = tx.get('date', 'N/A')
                    if isinstance(date, str) and len(date) >= 7:
                        month_year = date[:7]  # Format: YYYY-MM
                    else:
                        month_year = 'unknown'
                        
                    amount = float(tx.get('amount', 0))
                    category = tx.get('category', 'uncategorized').lower()
                    description = tx.get('description', 'N/A')
                    
                    # Skip income transactions for certain calculations
                    if amount < 0 or category == 'income':
                        continue
                        
                    # Update monthly totals
                    if month_year not in monthly_totals:
                        monthly_totals[month_year] = 0
                    monthly_totals[month_year] += amount
                    
                    # Update category totals
                    if category not in category_totals:
                        category_totals[category] = 0
                    category_totals[category] += amount
                    
                    # Update merchant data
                    if description not in merchants:
                        merchants[description] = 0
                    merchants[description] += amount
                
                # Add spending trends
                if monthly_totals:
                    context += "MONTHLY SPENDING TRENDS:\n"
                    for month, total in sorted(monthly_totals.items()):
                        context += f"- {month}: ${total:.2f}\n"
                    context += "\n"
                
                # Add top merchants
                if merchants:
                    top_merchants = sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:10]
                    context += "TOP MERCHANTS BY SPENDING:\n"
                    for merchant, amount in top_merchants:
                        context += f"- {merchant}: ${amount:.2f}\n"
                    context += "\n"
                
                # Add sample transactions (most recent 5 transactions)
                sample_size = min(5, len(transactions))
                sample_transactions = sorted(transactions, key=lambda x: x.get('date', ''), reverse=True)[:sample_size]
                
                context += f"RECENT TRANSACTIONS (showing {sample_size} of {len(transactions)}):\n"
                for tx in sample_transactions:
                    date = tx.get('date', 'N/A')
                    description = tx.get('description', 'N/A')
                    amount = float(tx.get('amount', 0))
                    category = tx.get('category', 'uncategorized')
                    
                    context += f"- {date}: {description} | ${amount:.2f} | {category}\n"
                context += "\n"
                
                # Add recurring expenses detection
                recurring = self._detect_recurring_expenses(transactions)
                if recurring:
                    context += "POTENTIAL RECURRING EXPENSES:\n"
                    for item, amount in recurring.items():
                        context += f"- {item}: ${amount:.2f} per month\n"
                    context += "\n"
            
            return context
        except Exception as e:
            print(f"Error formatting financial data: {str(e)}")
            return "Error: Unable to format financial data properly."
    
    def _detect_recurring_expenses(self, transactions: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Detect recurring expenses from transaction data
        
        Args:
            transactions (List[Dict[str, Any]]): List of transactions
        
        Returns:
            Dict[str, float]: Recurring expenses with their monthly amounts
        """
        # Implement recurring expense detection logic here
        # For now, return an empty dictionary
        return {}
    
    def get_chat_response(self, 
                         user_message: str, 
                         financial_data: Dict[str, Any], 
                         conversation_history: Optional[List[Dict[str, str]]] = None, 
                         initial_analysis: bool = False) -> str:
        """
        Get response from OpenAI chat completion API
        
        Args:
            user_message (str): User's message
            financial_data (Dict[str, Any]): User's financial data
            conversation_history (Optional[List[Dict[str, str]]]): Previous conversation history
            initial_analysis (bool): Whether this is the initial analysis request
        
        Returns:
            str: AI response message
        """
        try:
            # Format financial data for context
            financial_context = self._format_financial_data(financial_data)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": self.system_message}
            ]
            
            # Add financial context
            messages.append({"role": "system", "content": financial_context})
            
            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history)
            
            # For initial analysis, provide a specific prompt to guide the AI
            if initial_analysis:
                analysis_prompt = (
                    "Based on the financial data provided, please:"
                    "\n1. Give a brief overview of the user's financial health"
                    "\n2. Identify 2-3 key areas where they could improve their finances"
                    "\n3. Provide 2-3 specific, actionable recommendations tailored to their spending patterns"
                    "\n4. Highlight any unusual transactions or concerning patterns"
                    "\n\nKeep your response friendly, constructive, and personalized to their specific situation."
                )
                messages.append({"role": "user", "content": analysis_prompt})
            else:
                # Add user message for normal conversation
                messages.append({"role": "user", "content": user_message})
            
            # Call the OpenAI API with function calling abilities
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1500,
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # Log the error
            print(f"Error in OpenAI chat response: {str(e)}")
            raise
