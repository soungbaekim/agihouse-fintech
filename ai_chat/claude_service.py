"""
Claude AI Chat Service for Finance Analyzer
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeChatService:
    """
    Service for interacting with Anthropic's Claude API to provide financial insights
    and recommendations based on user data
    """
    
    def __init__(self):
        """Initialize the Claude chat service"""
        # Get API key from environment variable
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        # Initialize Claude API settings
        self.api_key = api_key
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
        
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
    
    def prepare_financial_context(self, financial_data: Dict[str, Any]) -> str:
        """
        Prepare the financial context to be sent to the AI
        
        Args:
            financial_data: Dictionary containing user's financial data
            
        Returns:
            String representation of the financial data
        """
        # Extract key financial metrics
        income = financial_data.get('analysis_data', {}).get('income', 0)
        expenses = financial_data.get('analysis_data', {}).get('expenses', 0)
        net_cash_flow = financial_data.get('analysis_data', {}).get('net_cash_flow', 0)
        savings_rate = financial_data.get('analysis_data', {}).get('savings_rate', 0)
        
        # Get spending by category
        spending_by_category = financial_data.get('chart_data', {}).get('spending_by_category', {})
        
        # Get top merchants
        top_merchants = financial_data.get('chart_data', {}).get('top_merchants', [])
        
        # Get recommendations
        savings_recommendations = financial_data.get('recommendations', {}).get('savings', [])
        investment_recommendations = financial_data.get('recommendations', {}).get('investments', [])
        
        # Get transactions data
        transactions = financial_data.get('transactions', [])
        
        # Get page context if available
        page_context = financial_data.get('page_context', {})
        current_page = page_context.get('page', '')
        current_view = page_context.get('data', {}).get('view', '')
        current_category = page_context.get('data', {}).get('category', '')
        
        # Format the context
        context = f"""
        FINANCIAL SUMMARY:
        - Total Income: ${income:,.2f}
        - Total Expenses: ${expenses:,.2f}
        - Net Cash Flow: ${net_cash_flow:,.2f}
        - Savings Rate: {savings_rate:.1f}%
        
        SPENDING BY CATEGORY:
        {json.dumps(spending_by_category, indent=2)}
        
        TOP MERCHANTS:
        {json.dumps(top_merchants, indent=2)}
        
        CURRENT RECOMMENDATIONS:
        Savings Opportunities:
        {json.dumps(savings_recommendations, indent=2)}
        
        Investment Suggestions:
        {json.dumps(investment_recommendations, indent=2)}
        """
        
        # Add transactions data (limited to most relevant ones for better context)
        transaction_sample_size = 15  # Limit to prevent token overflow
        
        # Get transactions by category if user is viewing a specific category
        if current_category:
            category_transactions = [t for t in transactions if t.get('category') == current_category]
            if category_transactions:
                # Sort by amount (descending) and take top transactions
                sorted_transactions = sorted(category_transactions, key=lambda t: float(t.get('amount', 0)), reverse=True)
                transaction_sample = sorted_transactions[:transaction_sample_size]
                context += f"""
                
                TRANSACTIONS IN CATEGORY '{current_category.upper()}':
                {json.dumps(transaction_sample, indent=2)}
                """
        # Otherwise, just include the most significant transactions overall
        elif transactions:
            # Sort by amount (descending) and take top transactions
            sorted_transactions = sorted(transactions, key=lambda t: abs(float(t.get('amount', 0))), reverse=True)
            transaction_sample = sorted_transactions[:transaction_sample_size]
            context += f"""
            
            SIGNIFICANT TRANSACTIONS:
            {json.dumps(transaction_sample, indent=2)}
            """
        
        # Add context-specific information based on current view
        if current_view == 'transactions' or 'transactions' in current_page:
            context += """
            
            CURRENT VIEW: Transactions
            The user is currently viewing their transaction history. You can provide insights about spending patterns,
            unusual transactions, or suggestions for categorizing transactions better.
            """
        elif current_view == 'recommendations' or 'recommendations' in current_page:
            context += """
            
            CURRENT VIEW: Recommendations
            The user is currently viewing savings and investment recommendations. You can provide more detailed
            explanations about these recommendations, how they were calculated, or additional personalized advice.
            """
        elif current_view == 'category' or 'category' in current_page:
            # Find the specific category data
            category_data = {}
            if current_category and current_category in spending_by_category:
                category_data = spending_by_category[current_category]
            
            context += f"""
            
            CURRENT VIEW: Category Details - {current_category}
            The user is currently viewing details for the {current_category} spending category.
            Category data: {json.dumps(category_data, indent=2)}
            You can provide specific insights about this category, such as how their spending compares to
            typical benchmarks, or strategies to optimize spending in this category.
            """
        
        return context
    
    def get_chat_response(self, 
                         user_message: str, 
                         financial_data: Dict[str, Any],
                         conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Get a response from the Claude API based on the user's message and financial data
        
        Args:
            user_message: The user's message
            financial_data: Dictionary containing user's financial data
            conversation_history: Optional list of previous messages
            
        Returns:
            The AI's response
        """
        # Prepare the financial context
        financial_context = self.prepare_financial_context(financial_data)
        
        # Prepare the conversation history in Claude's format
        messages = []
        if conversation_history:
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    messages.append({"role": "assistant", "content": msg["content"]})
        
        # Add the current user message with financial context
        current_message = f"""
        {financial_context}
        
        User Question: {user_message}
        """
        
        # Prepare the API request
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": self.model,
            "system": self.system_message,
            "messages": messages + [{"role": "user", "content": current_message}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            # Call the Claude API
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Extract and return the response text
            return response.json()["content"][0]["text"]
        
        except Exception as e:
            # Handle API errors
            return f"Sorry, I encountered an error: {str(e)}"
