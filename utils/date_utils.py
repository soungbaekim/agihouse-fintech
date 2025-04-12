"""
Date Utilities - Helper functions for date parsing and manipulation
"""

import re
import datetime
from typing import Optional, Union
from dateutil import parser as date_parser


def parse_date(date_str: str) -> Optional[datetime.date]:
    """
    Parse a date string into a datetime.date object
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        datetime.date object or None if parsing fails
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    # Clean the date string
    date_str = date_str.strip()
    
    # Try common date formats
    try:
        # Try dateutil parser first (handles many formats)
        return date_parser.parse(date_str).date()
    except (ValueError, TypeError):
        pass
    
    # Try manual parsing for common formats
    try:
        # MM/DD/YYYY or DD/MM/YYYY
        if re.match(r'\d{1,2}/\d{1,2}/\d{2,4}', date_str):
            parts = date_str.split('/')
            if len(parts) == 3:
                # Assume MM/DD/YYYY for US bank statements
                month, day, year = parts
                
                # Handle 2-digit years
                if len(year) == 2:
                    year = '20' + year if int(year) < 50 else '19' + year
                
                return datetime.date(int(year), int(month), int(day))
        
        # YYYY-MM-DD
        elif re.match(r'\d{4}-\d{1,2}-\d{1,2}', date_str):
            parts = date_str.split('-')
            if len(parts) == 3:
                year, month, day = parts
                return datetime.date(int(year), int(month), int(day))
        
        # DD-MM-YYYY
        elif re.match(r'\d{1,2}-\d{1,2}-\d{4}', date_str):
            parts = date_str.split('-')
            if len(parts) == 3:
                day, month, year = parts
                return datetime.date(int(year), int(month), int(day))
        
        # Month name formats: Jan 1, 2023 or January 1, 2023
        elif re.match(r'[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4}', date_str):
            return date_parser.parse(date_str).date()
    
    except (ValueError, TypeError, IndexError):
        pass
    
    # Return None if all parsing attempts fail
    return None


def get_month_name(month: int) -> str:
    """
    Get the name of a month from its number
    
    Args:
        month: Month number (1-12)
        
    Returns:
        Month name
    """
    return datetime.date(2000, month, 1).strftime('%B')


def get_date_range(start_date: datetime.date, end_date: datetime.date) -> list:
    """
    Get a list of dates between start_date and end_date (inclusive)
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        List of datetime.date objects
    """
    delta = end_date - start_date
    return [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]


def get_month_start_end(year: int, month: int) -> tuple:
    """
    Get the start and end dates for a given month
    
    Args:
        year: Year
        month: Month (1-12)
        
    Returns:
        Tuple of (start_date, end_date)
    """
    start_date = datetime.date(year, month, 1)
    
    # Get the last day of the month
    if month == 12:
        end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    
    return (start_date, end_date)
