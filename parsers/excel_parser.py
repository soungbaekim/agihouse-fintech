"""
Excel Parser - Parser for Excel bank statements
"""

import datetime
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

import pandas as pd

from parsers.base_parser import BaseParser
from utils.date_utils import parse_date


class ExcelParser(BaseParser):
    """Parser for Excel bank statements"""
    
    def parse(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Parse an Excel bank statement file
        
        Args:
            file_path: Path to the Excel bank statement file
            
        Returns:
            List of standardized transaction dictionaries
        """
        try:
            # Try to read all sheets
            excel_file = pd.ExcelFile(file_path)
            
            # Look for sheets that might contain transactions
            transaction_sheet = None
            sheet_names = excel_file.sheet_names
            
            # Try to find a sheet with transactions based on common naming patterns
            transaction_sheet_names = ['transactions', 'statement', 'activity', 'account']
            for name in transaction_sheet_names:
                matching_sheets = [s for s in sheet_names if name.lower() in s.lower()]
                if matching_sheets:
                    transaction_sheet = matching_sheets[0]
                    break
            
            # If no transaction sheet was found, use the first sheet
            if not transaction_sheet and sheet_names:
                transaction_sheet = sheet_names[0]
            
            if not transaction_sheet:
                raise ValueError("No sheets found in Excel file")
            
            # Read the transaction sheet
            df = pd.read_excel(file_path, sheet_name=transaction_sheet)
            
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
                raise ValueError("Could not identify required columns in Excel file")
            
            # Process transactions
            transactions = []
            for _, row in df.iterrows():
                # Skip header rows or empty rows
                if self._is_header_row(row):
                    continue
                
                # Parse date
                date_value = row[date_col]
                
                # Handle pandas Timestamp objects
                if isinstance(date_value, pd.Timestamp):
                    date = date_value.date()
                else:
                    date_str = str(date_value)
                    date = parse_date(date_str)
                
                # Skip if date parsing failed
                if not date:
                    continue
                
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
            raise ValueError(f"Failed to parse Excel file: {e}")
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """Find a column in the DataFrame based on possible names"""
        for name in possible_names:
            for col in df.columns:
                if isinstance(col, str) and name.lower() in col.lower():
                    return col
        return None
    
    def _is_date_column(self, series: pd.Series) -> bool:
        """Check if a column contains dates"""
        # Check if column has datetime type
        if pd.api.types.is_datetime64_any_dtype(series):
            return True
            
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
    
    def _is_header_row(self, row: pd.Series) -> bool:
        """Check if a row is likely a header row"""
        # Convert all values to string and lowercase
        values = [str(v).lower() for v in row.values]
        
        # Check for common header terms
        header_terms = ['date', 'description', 'amount', 'balance', 'transaction']
        matches = sum(1 for term in header_terms if any(term in v for v in values))
        
        # If multiple header terms are found, it's likely a header row
        return matches >= 2
    
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
