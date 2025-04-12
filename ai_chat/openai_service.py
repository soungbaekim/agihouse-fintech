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
        
        The user's financial data will be provided to you in each conversation. Use this data to provide 
        specific and actionable advice. Always base your recommendations on the actual numbers and patterns 
        in their data.
        
        Key areas to focus on:
        1. Spending patterns and anomalies
        2. Savings opportunities
        3. Budget optimization
        4. Debt management strategies
        5. Investment suggestions based on their financial situation
        
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
        Get a response from the OpenAI API based on the user's message and financial data
        
        Args:
            user_message: The user's message
            financial_data: Dictionary containing user's financial data
            conversation_history: Optional list of previous messages
            
        Returns:
            The AI's response
        """
        # Prepare the financial context
        financial_context = self.prepare_financial_context(financial_data)
        
        # Initialize messages with system message
        messages = [
            {"role": "system", "content": self.system_message}
        ]
        
        # Add financial context as a system message
        messages.append({
            "role": "system", 
            "content": f"Here is the user's current financial data:\n{financial_context}"
        })
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add the user's current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and return the response text
            return response.choices[0].message.content
        
        except Exception as e:
            # Handle API errors
            return f"Sorry, I encountered an error: {str(e)}"
