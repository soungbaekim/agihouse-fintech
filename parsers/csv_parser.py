"""
CSV Parser - Parser for CSV bank statements
"""

import csv
import datetime
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

import pandas as pd

from parsers.base_parser import BaseParser
from utils.date_utils import parse_date


class CSVParser(BaseParser):
    """Parser for CSV bank statements"""
    
    def parse(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Parse a CSV bank statement file
        
        Args:
            file_path: Path to the CSV bank statement file
            
        Returns:
            List of standardized transaction dictionaries
        """
        try:
            # Try to detect the CSV format automatically
            df = pd.read_csv(file_path)
            
            # Try to identify the columns based on common naming patterns
            date_col = self._find_column(df, ['date', 'transaction date', 'posted date'])
            desc_col = self._find_column(df, ['description', 'payee', 'merchant', 'transaction'])
            amount_col = self._find_column(df, ['amount', 'transaction amount'])
            
            # If we couldn't find the essential columns, try to infer them
            if not all([date_col, desc_col, amount_col]):
                # Infer columns based on content
                for col in df.columns:
                    # Check if column contains dates
                    if not date_col and self._is_date_column(df[col]):
                        date_col = col
                    # Check if column contains mostly text (descriptions)
                    elif not desc_col and self._is_description_column(df[col]):
                        desc_col = col
                    # Check if column contains monetary values
                    elif not amount_col and self._is_amount_column(df[col]):
                        amount_col = col
            
            if not all([date_col, desc_col, amount_col]):
                raise ValueError("Could not identify required columns in CSV file")
            
            # Process transactions
            transactions = []
            for _, row in df.iterrows():
                # Parse date
                date_str = str(row[date_col])
                date = parse_date(date_str)
                
                # Parse description
                description = str(row[desc_col]).strip()
                
                # Parse amount
                amount = self._parse_amount(row[amount_col])
                
                # Create standardized transaction
                transaction = {
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'raw_data': row.to_dict()  # Store original data for reference
                }
                
                transactions.append(transaction)
            
            return transactions
            
        except Exception as e:
            raise ValueError(f"Failed to parse CSV file: {e}")
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """Find a column in the DataFrame based on possible names"""
        for name in possible_names:
            for col in df.columns:
                if name.lower() in col.lower():
                    return col
        return None
    
    def _is_date_column(self, series: pd.Series) -> bool:
        """Check if a column contains dates"""
        try:
            # Try to convert to datetime
            pd.to_datetime(series, errors='raise')
            return True
        except:
            return False
    
    def _is_description_column(self, series: pd.Series) -> bool:
        """Check if a column contains mostly text (descriptions)"""
        # Check if column has string type and longer text values
        if series.dtype == 'object':
            # Check average string length
            avg_len = series.astype(str).str.len().mean()
            return avg_len > 10
        return False
    
    def _is_amount_column(self, series: pd.Series) -> bool:
        """Check if a column contains monetary values"""
        try:
            # Try to convert to numeric
            numeric_series = pd.to_numeric(series, errors='coerce')
            # Check if most values are not NaN
            return numeric_series.notna().mean() > 0.7
        except:
            return False
    
    def _parse_amount(self, amount_value: Any) -> float:
        """Parse amount value to float"""
        if isinstance(amount_value, (int, float)):
            return float(amount_value)
        
        # Handle string amounts
        if isinstance(amount_value, str):
            # Remove currency symbols and commas
            clean_amount = amount_value.replace('$', '').replace(',', '').strip()
            
            # Handle parentheses for negative values: (123.45) -> -123.45
            if clean_amount.startswith('(') and clean_amount.endswith(')'):
                clean_amount = '-' + clean_amount[1:-1]
                
            try:
                return float(clean_amount)
            except ValueError:
                pass
        
        # Default fallback
        return 0.0
