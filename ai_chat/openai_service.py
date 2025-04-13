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
        # Explicitly reload environment variables to ensure we get the latest values
        load_dotenv(override=True)
        
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY environment variable is not set. Using mock responses.")
            self.use_mock = True
        else:
            self.use_mock = False
            # Initialize OpenAI client
            try:
                self.client = openai.OpenAI(api_key=api_key)
                print("Successfully initialized OpenAI client")
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.use_mock = True
                
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
    
    def _get_mock_response(self, user_message: str, financial_data: Dict[str, Any], initial_analysis: bool = False) -> str:
        """Generate a mock response when OpenAI API is not available
        
        Args:
            user_message: The message from the user
            financial_data: Dictionary containing financial analysis data
            initial_analysis: Whether this is the initial analysis message
            
        Returns:
            A mock response based on financial data
        """
        income = financial_data.get('income', 0)
        expenses = financial_data.get('expenses', 0)
        savings_rate = financial_data.get('savings_rate', 0)
        net_cash_flow = financial_data.get('net_cash_flow', 0)
        
        # For initial analysis, provide a financial overview
        if initial_analysis:
            return f"""Based on your financial data, here's my analysis:

* Your monthly income is ${income:.2f}
* Your expenses total ${expenses:.2f}
* Your net cash flow is ${net_cash_flow:.2f}
* Your savings rate is {savings_rate:.1f}%

Your financial health appears to be {'good' if savings_rate > 20 else 'fair' if savings_rate > 10 else 'needs attention'}. {'You are saving a healthy portion of your income.' if savings_rate > 20 else 'Consider increasing your savings rate to at least 20% of your income.'}

I'd recommend focusing on these areas:
1. Track your spending in more detail
2. {'Build an emergency fund' if net_cash_flow < 1000 else 'Consider investing some of your savings'}
3. Review recurring subscriptions for potential savings

I'm happy to discuss any specific financial questions you have!"""
        
        # For regular messages, respond based on common financial questions
        if "budget" in user_message.lower() or "spending" in user_message.lower():
            return "Based on your spending patterns, I'd recommend allocating 50% of your income to necessities, 30% to wants, and 20% to savings and debt repayment. This follows the popular 50/30/20 budgeting rule."
        
        elif "save" in user_message.lower() or "saving" in user_message.lower():
            return "To improve your savings, consider automating transfers to a high-yield savings account on payday, cutting unnecessary subscriptions, and following the 24-hour rule for non-essential purchases."
        
        elif "invest" in user_message.lower() or "investment" in user_message.lower():
            return "For investing, first ensure you have an emergency fund covering 3-6 months of expenses. Then consider tax-advantaged accounts like a 401(k) or IRA, followed by a diversified portfolio of index funds for long-term growth."
        
        elif "debt" in user_message.lower():
            return "To tackle debt effectively, prioritize high-interest debt first (like credit cards), consider consolidation for lower interest rates, and maintain minimum payments on all debts while putting extra money toward the highest-interest debt."
        
        else:
            return "I'm here to help with your financial questions! You can ask about budgeting, saving strategies, investment options, debt management, or specific aspects of your financial situation. What would you like to know more about?"
    
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
    
    def get_chat_response(self, user_message: str, financial_data: Dict[str, Any], 
                         conversation_history: List[Dict[str, str]], initial_analysis: bool = False) -> str:
        """Get a response from OpenAI based on user message and financial data
        
        Args:
            user_message: The message from the user
            financial_data: Dictionary containing financial analysis data
            conversation_history: Previous messages in the conversation
            initial_analysis: Whether this is the initial analysis message
            
        Returns:
            Response from the AI assistant
        """
        # If using mock mode, return a predefined response
        if hasattr(self, 'use_mock') and self.use_mock:
            return self._get_mock_response(user_message, financial_data, initial_analysis)
            
        # Format financial data for the system prompt
        financial_data_formatted = self._format_financial_data(financial_data)
        
        # Create system message with financial context
        system_message = self.system_message + financial_data_formatted
        
        # Prepare messages for the API
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add conversation history
        for message in conversation_history:
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })
        
        # If this is not an initial analysis, add the user's message
        if not initial_analysis:
            messages.append({"role": "user", "content": user_message})
        else:
            # For initial analysis, use a specific prompt
            initial_prompt = "Please analyze my financial situation based on the data provided."
            messages.append({"role": "user", "content": initial_prompt})
        
        try:
            # Make the API call to OpenAI
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
