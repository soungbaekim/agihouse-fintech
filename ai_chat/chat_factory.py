"""
Chat Service Factory for Finance Analyzer
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatServiceFactory:
    """
    Factory for creating chat service instances based on configuration
    """
    
    @staticmethod
    def get_chat_service():
        """
        Get the appropriate chat service based on environment configuration
        
        Returns:
            An instance of a chat service
        """
        # Determine which AI provider to use
        ai_provider = os.getenv("AI_PROVIDER", "openai").lower()
        
        if ai_provider == "openai":
            from ai_chat.openai_service import OpenAIChatService
            return OpenAIChatService()
        elif ai_provider == "claude":
            from ai_chat.claude_service import ClaudeChatService
            return ClaudeChatService()
        else:
            raise ValueError(f"Unsupported AI provider: {ai_provider}")
    
    @staticmethod
    def get_chat_response(user_message: str, 
                         financial_data: Dict[str, Any],
                         conversation_history: Optional[Dict[str, Any]] = None) -> str:
        """
        Get a response from the configured chat service
        
        Args:
            user_message: The user's message
            financial_data: Dictionary containing user's financial data
            conversation_history: Optional conversation history
            
        Returns:
            The AI's response
        """
        try:
            service = ChatServiceFactory.get_chat_service()
            return service.get_chat_response(user_message, financial_data, conversation_history)
        except Exception as e:
            return f"Sorry, I couldn't process your request: {str(e)}"
