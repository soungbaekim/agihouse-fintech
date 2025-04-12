"""
Base Parser - Abstract base class for all statement parsers
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Union


class BaseParser(ABC):
    """Abstract base class for all statement parsers"""
    
    @abstractmethod
    def parse(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Parse a bank statement file and return a list of transactions
        
        Args:
            file_path: Path to the bank statement file
            
        Returns:
            List of transaction dictionaries with standardized keys:
            - date: Transaction date (datetime.date)
            - description: Transaction description (str)
            - amount: Transaction amount (float, negative for expenses)
            - category: Transaction category if available (str, optional)
            - transaction_type: Type of transaction (e.g., debit, credit) (str, optional)
            
        Raises:
            ValueError: If file cannot be parsed
        """
        pass
    
    def _standardize_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize a transaction dictionary to ensure consistent keys
        
        Args:
            transaction: Raw transaction dictionary
            
        Returns:
            Standardized transaction dictionary
        """
        # Implement common standardization logic here
        # This can be overridden by subclasses if needed
        return transaction
