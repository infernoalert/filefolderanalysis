"""
CSV Processing Module

This module handles reading and processing CSV files for company analysis.
It provides a flexible interface for different CSV structures and handles
large files efficiently using chunked processing.
"""

import pandas as pd
import numpy as np
from typing import Iterator, Dict, Any, Optional, List
from pathlib import Path
import logging
from config import config


class CSVProcessor:
    """Handles CSV file processing for company analysis"""
    
    def __init__(self, csv_file_path: str, chunk_size: Optional[int] = None):
        """
        Initialize CSV processor
        
        Args:
            csv_file_path: Path to the CSV file
            chunk_size: Size of chunks for processing (default from config)
        """
        self.csv_file_path = Path(csv_file_path)
        self.chunk_size = chunk_size or config.chunk_size
        self.column_mappings = config.csv_columns.copy()
        self.total_rows = 0
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def validate_file(self) -> bool:
        """
        Validate that the CSV file exists and is readable
        
        Returns:
            bool: True if file is valid, False otherwise
        """
        if not self.csv_file_path.exists():
            self.logger.error(f"CSV file not found: {self.csv_file_path}")
            return False
        
        if not self.csv_file_path.is_file():
            self.logger.error(f"Path is not a file: {self.csv_file_path}")
            return False
        
        try:
            # Try to read just the header to validate structure
            df_sample = pd.read_csv(self.csv_file_path, nrows=1)
            self.logger.info(f"CSV file validated. Columns: {list(df_sample.columns)}")
            return True
        except Exception as e:
            self.logger.error(f"Error validating CSV file: {str(e)}")
            return False
    
    def get_file_info(self) -> Dict[str, Any]:
        """
        Get basic information about the CSV file
        
        Returns:
            Dict containing file information
        """
        info = {
            'file_path': str(self.csv_file_path),
            'file_size_mb': 0,
            'total_rows': 0,
            'columns': [],
            'exists': False
        }
        
        if not self.csv_file_path.exists():
            return info
        
        info['exists'] = True
        info['file_size_mb'] = self.csv_file_path.stat().st_size / (1024 * 1024)
        
        try:
            # Get column names
            df_sample = pd.read_csv(self.csv_file_path, nrows=1)
            info['columns'] = list(df_sample.columns)
            
            # Count total rows
            info['total_rows'] = self._count_rows()
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {str(e)}")
        
        return info
    
    def _count_rows(self) -> int:
        """Count total rows in the CSV file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin1']
            for encoding in encodings:
                try:
                    with open(self.csv_file_path, 'r', encoding=encoding) as f:
                        return sum(1 for _ in f) - 1  # Subtract header
                except UnicodeDecodeError:
                    continue
            
            return 0
        except Exception as e:
            self.logger.error(f"Error counting rows: {str(e)}")
            return 0
    
    def set_column_mappings(self, mappings: Dict[str, str]) -> None:
        """
        Set custom column mappings for different CSV structures
        
        Args:
            mappings: Dictionary mapping internal names to CSV column names
        """
        self.column_mappings.update(mappings)
    
    def get_chunks(self) -> Iterator[pd.DataFrame]:
        """
        Get CSV data in chunks for memory-efficient processing
        
        Yields:
            pd.DataFrame: Chunks of the CSV data
        """
        encodings = ['utf-8', 'utf-8-sig', 'latin1']
        
        for encoding in encodings:
            try:
                chunk_iter = pd.read_csv(
                    self.csv_file_path,
                    chunksize=self.chunk_size,
                    encoding=encoding
                )
                
                for chunk in chunk_iter:
                    yield chunk
                
                return  # Success, exit the encoding loop
                
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.logger.error(f"Error reading CSV with encoding {encoding}: {str(e)}")
                continue
        
        # If we reach here, all encodings failed
        raise Exception("Could not read CSV file with any supported encoding")
    
    def get_column_data(self, chunk: pd.DataFrame, column_key: str) -> pd.Series:
        """
        Get data from a specific column using the column mappings
        
        Args:
            chunk: DataFrame chunk
            column_key: Internal column key (e.g., 'name', 'path')
            
        Returns:
            pd.Series: The column data
        """
        column_name = self.column_mappings.get(column_key, column_key)
        
        if column_name in chunk.columns:
            column_data = chunk[column_name]
            # Ensure we return a Series even if it's a single column DataFrame
            return column_data if isinstance(column_data, pd.Series) else pd.Series(column_data)
        else:
            self.logger.warning(f"Column '{column_name}' not found in CSV")
            return pd.Series(dtype=object)
    
    def extract_row_data(self, row: pd.Series) -> Dict[str, Any]:
        """
        Extract relevant data from a row using column mappings
        
        Args:
            row: DataFrame row
            
        Returns:
            Dict with extracted data
        """
        return {
            'name': row.get(self.column_mappings.get('name', 'Name'), ''),
            'path': row.get(self.column_mappings.get('path', 'Path'), ''),
            'modified_by': row.get(self.column_mappings.get('modified_by', 'Modified By'), ''),
            'item_type': row.get(self.column_mappings.get('item_type', 'Item Type'), ''),
            'file_size': row.get(self.column_mappings.get('file_size', 'File Size'), ''),
            'modified': row.get(self.column_mappings.get('modified', 'Modified'), '')
        }
    
    def process_csv_for_analysis(self, process_func, progress_callback=None) -> Any:
        """
        Process the CSV file using a custom processing function
        
        Args:
            process_func: Function to call for each chunk
            progress_callback: Optional callback for progress updates
            
        Returns:
            Result from the processing function
        """
        if not self.validate_file():
            raise ValueError("Invalid CSV file")
        
        total_rows = self._count_rows()
        processed_rows = 0
        results = []
        
        self.logger.info(f"Starting CSV processing: {total_rows:,} rows")
        
        try:
            for chunk_num, chunk in enumerate(self.get_chunks()):
                # Process the chunk
                chunk_result = process_func(chunk, chunk_num)
                results.append(chunk_result)
                
                # Update progress
                processed_rows += len(chunk)
                if progress_callback:
                    progress_callback(processed_rows, total_rows)
                
                self.logger.info(f"Processed chunk {chunk_num + 1}, rows: {processed_rows:,}/{total_rows:,}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error during CSV processing: {str(e)}")
            raise
    
    def get_sample_data(self, num_rows: int = 100) -> pd.DataFrame:
        """
        Get a sample of data from the CSV file
        
        Args:
            num_rows: Number of rows to sample
            
        Returns:
            pd.DataFrame: Sample data
        """
        try:
            return pd.read_csv(self.csv_file_path, nrows=num_rows)
        except Exception as e:
            self.logger.error(f"Error getting sample data: {str(e)}")
            return pd.DataFrame()
    
    def detect_csv_structure(self) -> Dict[str, Any]:
        """
        Analyze the CSV structure to suggest column mappings
        
        Returns:
            Dict with structure analysis
        """
        sample = self.get_sample_data(10)
        
        if sample.empty:
            return {}
        
        structure = {
            'columns': list(sample.columns),
            'suggested_mappings': {},
            'data_types': sample.dtypes.to_dict()
        }
        
        # Try to auto-detect column mappings
        columns_lower = [col.lower() for col in sample.columns]
        
        mapping_hints = {
            'name': ['name', 'filename', 'file_name', 'item_name'],
            'path': ['path', 'file_path', 'full_path', 'location'],
            'modified_by': ['modified_by', 'modified by', 'author', 'created_by'],
            'item_type': ['item_type', 'item type', 'type', 'file_type'],
            'file_size': ['file_size', 'file size', 'size', 'file_size_bytes'],
            'modified': ['modified', 'date_modified', 'last_modified', 'modification_date']
        }
        
        for internal_key, possible_names in mapping_hints.items():
            for possible_name in possible_names:
                if possible_name in columns_lower:
                    # Find the actual column name (with original case)
                    actual_col = sample.columns[columns_lower.index(possible_name)]
                    structure['suggested_mappings'][internal_key] = actual_col
                    break
        
        return structure 