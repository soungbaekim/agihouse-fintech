"""
Parser Factory - Creates appropriate parser based on file type
"""

from pathlib import Path
from typing import Union

from parsers.base_parser import BaseParser
from parsers.csv_parser import CSVParser
from parsers.pdf_parser import PDFParser
from parsers.excel_parser import ExcelParser


class ParserFactory:
    """Factory class to create appropriate parser based on file extension"""
    
    def get_parser(self, file_path: Union[str, Path]) -> BaseParser:
        """
        Returns the appropriate parser for the given file
        
        Args:
            file_path: Path to the bank statement file
            
        Returns:
            An instance of the appropriate parser
            
        Raises:
            ValueError: If file extension is not supported
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
            
        # Get file extension
        ext = file_path.suffix.lower()
        
        # Create appropriate parser
        if ext == '.csv':
            return CSVParser()
        elif ext == '.pdf':
            return PDFParser()
        elif ext in ['.xlsx', '.xls']:
            return ExcelParser()
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: .csv, .pdf, .xlsx, .xls")
