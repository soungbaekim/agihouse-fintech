"""
PDF Parser - Parser for PDF bank statements
"""

import re
import datetime
from pathlib import Path
from typing import List, Dict, Any, Union

import pdfplumber
import tabula
import pandas as pd

from parsers.base_parser import BaseParser
from utils.date_utils import parse_date


class PDFParser(BaseParser):
    """Parser for PDF bank statements"""
    
    def parse(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Parse a PDF bank statement file
        
        Args:
            file_path: Path to the PDF bank statement file
            
        Returns:
            List of standardized transaction dictionaries
        """
        try:
            # First try tabula-py to extract tables
            transactions = self._parse_with_tabula(file_path)
            
            # If tabula didn't find transactions, try pdfplumber
            if not transactions:
                transactions = self._parse_with_pdfplumber(file_path)
                
            if not transactions:
                raise ValueError("Could not extract transactions from PDF")
                
            return transactions
            
        except Exception as e:
            raise ValueError(f"Failed to parse PDF file: {e}")
    
    def _parse_with_tabula(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Parse PDF using tabula-py (good for structured tables)"""
        try:
            # Extract all tables from the PDF
            tables = tabula.read_pdf(str(file_path), pages='all', multiple_tables=True)
            
            if not tables:
                return []
                
            transactions = []
            
            for df in tables:
                # Skip empty tables
                if df.empty:
                    continue
                    
                # Try to identify the columns based on common naming patterns
                date_col = self._find_column(df, ['date', 'transaction date', 'posted'])
                desc_col = self._find_column(df, ['description', 'payee', 'merchant', 'transaction'])
                amount_col = self._find_column(df, ['amount', 'transaction amount', 'withdrawal', 'deposit'])
                
                # If we couldn't find the essential columns, try the next table
                if not all([date_col, desc_col, amount_col]):
                    continue
                
                # Process transactions
                for _, row in df.iterrows():
                    # Skip header rows or empty rows
                    if self._is_header_row(row):
                        continue
                        
                    # Parse date
                    date_str = str(row[date_col])
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
            
        except Exception:
            # Return empty list if tabula fails
            return []
    
    def _parse_with_pdfplumber(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Parse PDF using pdfplumber (good for text extraction)"""
        transactions = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                
                if not text:
                    continue
                
                # Try to extract transactions using regex patterns
                # This is a simplified approach and may need to be customized for specific bank formats
                
                # Common patterns for transaction lines
                # Format: Date Description Amount
                transaction_patterns = [
                    # Pattern 1: MM/DD/YYYY or DD/MM/YYYY followed by description and amount
                    r'(\d{1,2}/\d{1,2}/\d{2,4})\s+([A-Za-z0-9\s\-\.,&\'\"]+?)\s+([\-\$\d\.,]+)',
                    
                    # Pattern 2: YYYY-MM-DD followed by description and amount
                    r'(\d{4}-\d{2}-\d{2})\s+([A-Za-z0-9\s\-\.,&\'\"]+?)\s+([\-\$\d\.,]+)',
                ]
                
                for pattern in transaction_patterns:
                    matches = re.finditer(pattern, text)
                    
                    for match in matches:
                        date_str, description, amount_str = match.groups()
                        
                        # Parse date
                        date = parse_date(date_str)
                        
                        # Skip if date parsing failed
                        if not date:
                            continue
                        
                        # Parse description
                        description = description.strip()
                        
                        # Parse amount
                        amount = self._parse_amount(amount_str)
                        
                        # Create standardized transaction
                        transaction = {
                            'date': date,
                            'description': description,
                            'amount': amount,
                            'raw_data': {'text': match.group(0)}  # Store original text for reference
                        }
                        
                        transactions.append(transaction)
                
                # If we found transactions with regex, return them
                if transactions:
                    return transactions
                    
                # If regex didn't work, try to extract tables
                tables = page.extract_tables()
                
                for table in tables:
                    # Skip empty tables
                    if not table or len(table) <= 1:  # Skip tables with only headers
                        continue
                    
                    # Assume first row is header
                    headers = table[0]
                    
                    # Find date, description, and amount columns
                    date_idx = self._find_header_index(headers, ['date', 'transaction date', 'posted'])
                    desc_idx = self._find_header_index(headers, ['description', 'payee', 'merchant', 'transaction'])
                    amount_idx = self._find_header_index(headers, ['amount', 'transaction amount', 'withdrawal', 'deposit'])
                    
                    # If we couldn't find the essential columns, try the next table
                    if not all([date_idx is not None, desc_idx is not None, amount_idx is not None]):
                        continue
                    
                    # Process transactions
                    for row in table[1:]:  # Skip header row
                        # Skip empty rows
                        if not row or len(row) <= max(date_idx, desc_idx, amount_idx):
                            continue
                        
                        # Parse date
                        date_str = str(row[date_idx])
                        date = parse_date(date_str)
                        
                        # Skip if date parsing failed
                        if not date:
                            continue
                        
                        # Parse description
                        description = str(row[desc_idx]).strip()
                        
                        # Parse amount
                        amount = self._parse_amount(row[amount_idx])
                        
                        # Create standardized transaction
                        transaction = {
                            'date': date,
                            'description': description,
                            'amount': amount,
                            'raw_data': dict(zip(headers, row))  # Store original data for reference
                        }
                        
                        transactions.append(transaction)
        
        return transactions
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Union[str, None]:
        """Find a column in the DataFrame based on possible names"""
        for name in possible_names:
            for col in df.columns:
                if isinstance(col, str) and name.lower() in col.lower():
                    return col
        return None
    
    def _find_header_index(self, headers: List[str], possible_names: List[str]) -> Union[int, None]:
        """Find a header index based on possible names"""
        for name in possible_names:
            for i, header in enumerate(headers):
                if isinstance(header, str) and name.lower() in header.lower():
                    return i
        return None
    
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
