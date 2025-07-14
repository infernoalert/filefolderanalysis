"""
Company Analyzer Main Module

This is the main module that integrates all components of the company analyzer:
- CSV processing
- Company detection
- Results management

It provides a clean, modular interface for analyzing CSV files and extracting
company names with improved organization for MCP integration.
"""

import logging
from collections import Counter, defaultdict
from typing import Dict, Any, List, Optional, Tuple
from tqdm import tqdm
import pandas as pd

from config import config
from csv_processor import CSVProcessor
from company_detector import CompanyDetector
from enhanced_company_detector import EnhancedCompanyDetector
from results_manager import ResultsManager


class CompanyAnalyzer:
    """
    Main company analyzer class that orchestrates the analysis process
    
    This class provides a clean interface for analyzing CSV files and
    extracting company names while maintaining separation of concerns
    through modular design.
    """
    
    def __init__(self, csv_file_path: Optional[str] = None, chunk_size: Optional[int] = None, filter_type: Optional[str] = None):
        """
        Initialize the company analyzer
        
        Args:
            csv_file_path: Path to the CSV file to analyze
            chunk_size: Size of chunks for processing (default from config)
            filter_type: Type of items to analyze ('all', 'folders', 'files')
        """
        self.csv_file_path = csv_file_path or config.default_csv_file
        self.chunk_size = chunk_size or config.chunk_size
        self.filter_type = filter_type or config.filter_type
        
        # Setup logging first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.csv_processor = CSVProcessor(self.csv_file_path, self.chunk_size)
        
        # Try to use enhanced detector, fallback to basic if it fails
        try:
            self.company_detector = EnhancedCompanyDetector()
            self.using_enhanced_detector = True
            self.logger.info("Using Enhanced Company Detector with NLP capabilities")
        except Exception as e:
            self.logger.warning(f"Enhanced detector failed to initialize: {e}")
            self.logger.info("Falling back to basic Company Detector")
            self.company_detector = CompanyDetector()
            self.using_enhanced_detector = False
        
        self.results_manager = ResultsManager()
        
        # Analysis results
        self.companies = Counter()
        self.company_details: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'folders': set(),
            'paths': set(),
            'modified_by': set(),
            'count': 0,
            'file_types': set()
        })
        
        # Statistics
        self.stats = {
            'total_rows_processed': 0,
            'technical_files_filtered': 0,
            'type_filtered': 0,
            'companies_found': 0,
            'processing_time': 0
        }
    
    def analyze(self) -> bool:
        """
        Run the complete analysis process
        
        Returns:
            bool: True if analysis completed successfully, False otherwise
        """
        try:
            self.logger.info("Starting company analysis...")
            
            # Validate input file
            if not self.csv_processor.validate_file():
                self.logger.error("CSV file validation failed")
                return False
            
            # Get file information
            file_info = self.csv_processor.get_file_info()
            self.logger.info(f"Analyzing file: {file_info['file_path']}")
            self.logger.info(f"File size: {file_info['file_size_mb']:.1f} MB")
            self.logger.info(f"Total rows: {file_info['total_rows']:,}")
            
            # Process CSV file
            self._process_csv_file()
            
            # Log results
            self.logger.info(f"Analysis complete!")
            self.logger.info(f"Found {len(self.companies)} unique companies")
            self.logger.info(f"Total company entries: {sum(self.companies.values())}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return False
    
    def _process_csv_file(self):
        """Process the CSV file and extract company names"""
        self.logger.info("Processing CSV file...")
        
        # Reset counters
        self.companies.clear()
        self.company_details.clear()
        self.stats['total_rows_processed'] = 0
        self.stats['technical_files_filtered'] = 0
        self.stats['type_filtered'] = 0
        
        all_companies = []
        
        # Process file in chunks
        for chunk in tqdm(self.csv_processor.get_chunks(), desc="Processing chunks"):
            chunk_companies = self._process_chunk(chunk)
            all_companies.extend(chunk_companies)
        
        # Update final results
        self.companies = Counter(all_companies)
        self.stats['companies_found'] = len(self.companies)
        
        self.logger.info(f"Processed {self.stats['total_rows_processed']:,} rows")
        self.logger.info(f"Filtered {self.stats['technical_files_filtered']:,} technical files")
        if self.filter_type != 'all':
            self.logger.info(f"Filtered {self.stats['type_filtered']:,} items by type ({self.filter_type})")
    
    def _process_chunk(self, chunk: pd.DataFrame) -> List[str]:
        """
        Process a single chunk of CSV data
        
        Args:
            chunk: DataFrame chunk to process
            
        Returns:
            List of company names found in this chunk
        """
        chunk_companies = []
        
        for _, row in chunk.iterrows():
            self.stats['total_rows_processed'] += 1
            
            # Extract row data
            row_data = self.csv_processor.extract_row_data(row)
            name = row_data['name']
            
            # Skip technical files
            if self.company_detector.is_technical_file(name):
                self.stats['technical_files_filtered'] += 1
                continue
            
            # Filter by item type if specified
            if self.filter_type != 'all':
                item_type = row_data['item_type']
                if self.filter_type == 'folders' and item_type != 'Folder':
                    self.stats['type_filtered'] += 1
                    continue
                elif self.filter_type == 'files' and item_type == 'Folder':
                    self.stats['type_filtered'] += 1
                    continue
            
            # Clean and detect companies
            cleaned_name = self.company_detector.clean_company_name(name)
            
            if self.company_detector.is_likely_company(cleaned_name):
                # Store company details
                self.company_details[cleaned_name]['folders'].add(name)
                self.company_details[cleaned_name]['paths'].add(row_data['path'])
                self.company_details[cleaned_name]['modified_by'].add(row_data['modified_by'])
                self.company_details[cleaned_name]['count'] += 1
                
                # Store file type if available
                if row_data['item_type']:
                    self.company_details[cleaned_name]['file_types'].add(row_data['item_type'])
                
                chunk_companies.append(cleaned_name)
        
        return chunk_companies
    
    def get_company_details(self, company_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific company
        
        Args:
            company_name: Name of the company to get details for
            
        Returns:
            Dictionary with company details
        """
        return self.results_manager._format_company_details(company_name, self.company_details)
    
    def search_companies(self, query: str) -> List[Tuple[str, int]]:
        """
        Search for companies matching a query
        
        Args:
            query: Search query
            
        Returns:
            List of (company_name, count) tuples matching the query
        """
        return self.results_manager.search_companies(self.companies, query)
    
    def save_results(self, output_formats: Optional[List[str]] = None) -> List[str]:
        """
        Save analysis results in multiple formats
        
        Args:
            output_formats: List of formats to save (default: all formats)
            
        Returns:
            List of created file paths
        """
        return self.results_manager.save_results(
            self.companies, 
            self.company_details, 
            output_formats,
            self.filter_type
        )
    
    def print_summary(self):
        """Print a summary of the analysis results"""
        self.results_manager.print_summary(self.companies, self.company_details, self.filter_type)
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """
        Get analysis statistics
        
        Returns:
            Dictionary with analysis statistics
        """
        stats = {
            **self.stats,
            'unique_companies': len(self.companies),
            'total_company_entries': sum(self.companies.values()),
            'file_info': self.csv_processor.get_file_info(),
            'detector_type': 'enhanced' if self.using_enhanced_detector else 'basic',
            'filter_type': self.filter_type
        }
        
        # Add enhanced analysis if available
        if self.using_enhanced_detector:
            try:
                company_names = list(self.companies.keys())
                if company_names:
                    # Type check for enhanced detector
                    if hasattr(self.company_detector, 'get_analysis_summary'):
                        enhanced_stats = getattr(self.company_detector, 'get_analysis_summary')(company_names)
                        stats['enhanced_analysis'] = enhanced_stats
            except Exception as e:
                self.logger.warning(f"Enhanced analysis failed: {e}")
        
        return stats
    
    def export_for_mcp(self) -> Dict[str, Any]:
        """
        Export results in a format suitable for MCP integration
        
        Returns:
            Dictionary formatted for MCP
        """
        return self.results_manager.export_for_mcp(self.companies, self.company_details)
    
    def configure_csv_columns(self, column_mappings: Dict[str, str]):
        """
        Configure CSV column mappings for different file structures
        
        Args:
            column_mappings: Dictionary mapping internal names to CSV column names
        """
        self.csv_processor.set_column_mappings(column_mappings)
    
    def add_known_company(self, company_name: str):
        """
        Add a known company to improve detection
        
        Args:
            company_name: Name of the company to add
        """
        self.company_detector.add_known_company(company_name)
    
    def get_top_companies(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top N companies by frequency
        
        Args:
            n: Number of top companies to return
            
        Returns:
            List of (company_name, count) tuples
        """
        return self.companies.most_common(n)
    
    def get_csv_structure_info(self) -> Dict[str, Any]:
        """
        Get information about the CSV file structure
        
        Returns:
            Dictionary with CSV structure information
        """
        return self.csv_processor.detect_csv_structure()
    
    def validate_setup(self) -> Dict[str, bool]:
        """
        Validate the analyzer setup
        
        Returns:
            Dictionary with validation results
        """
        return {
            'csv_file_exists': self.csv_processor.validate_file(),
            'csv_readable': len(self.csv_processor.get_sample_data()) > 0,
            'config_loaded': config is not None,
            'components_initialized': all([
                self.csv_processor is not None,
                self.company_detector is not None,
                self.results_manager is not None
            ])
        }
    
    def get_detection_details(self, company_name: str) -> Dict[str, Any]:
        """
        Get detailed detection analysis for a company name (enhanced detector only)
        
        Args:
            company_name: Name to analyze
            
        Returns:
            Dict with detailed analysis or basic info if using basic detector
        """
        if self.using_enhanced_detector and hasattr(self.company_detector, 'get_detection_details'):
            try:
                return getattr(self.company_detector, 'get_detection_details')(company_name)
            except Exception as e:
                self.logger.warning(f"Enhanced detection details failed: {e}")
        
        # Fallback for basic detector
        return {
            'is_company': self.company_detector.is_likely_company(company_name),
            'detector_type': 'basic',
            'confidence': 1.0 if self.company_detector.is_likely_company(company_name) else 0.0,
            'reasons': ['basic_pattern_matching']
        }
    
    def batch_analyze_names(self, names: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze multiple names at once (enhanced detector only)
        
        Args:
            names: List of names to analyze
            
        Returns:
            List of analysis results
        """
        if self.using_enhanced_detector and hasattr(self.company_detector, 'batch_analyze'):
            try:
                return getattr(self.company_detector, 'batch_analyze')(names)
            except Exception as e:
                self.logger.warning(f"Batch analysis failed: {e}")
        
        # Fallback for basic detector
        results = []
        for name in names:
            is_company = self.company_detector.is_likely_company(name)
            results.append({
                'name': name,
                'is_company': is_company,
                'confidence': 1.0 if is_company else 0.0,
                'reasons': ['basic_pattern_matching'],
                'detector_type': 'basic'
            })
        return results
    
    def run_interactive_search(self):
        """Run an interactive search session"""
        if not self.companies:
            print("No analysis results available. Run analyze() first.")
            return
        
        print("\n" + "="*60)
        print("INTERACTIVE COMPANY SEARCH")
        print("="*60)
        if self.using_enhanced_detector:
            print("🚀 Enhanced detector with NLP capabilities active")
            print("Type 'details <company>' for detailed analysis")
        print("Type 'quit' or 'exit' to stop")
        print()
        
        while True:
            try:
                query = input("Search companies > ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not query:
                    continue
                
                # Check for details command
                if query.lower().startswith('details ') and self.using_enhanced_detector:
                    company_name = query[8:].strip()
                    details = self.get_detection_details(company_name)
                    print(f"\n🔍 Detailed Analysis for: '{company_name}'")
                    print("-" * 40)
                    print(f"Is Company: {details.get('is_company', 'Unknown')}")
                    print(f"Confidence: {details.get('confidence', 0):.2f}")
                    print(f"Reasons: {', '.join(details.get('reasons', []))}")
                    if 'spacy_analysis' in details:
                        print(f"spaCy Entities: {details['spacy_analysis'].get('entities', [])}")
                    print()
                    continue
                
                matches = self.search_companies(query)
                if matches:
                    print(f"Found {len(matches)} matches:")
                    for company, count in matches[:config.max_search_results]:
                        print(f"  {company} ({count} folders)")
                    
                    if len(matches) > config.max_search_results:
                        print(f"  ... and {len(matches) - config.max_search_results} more")
                else:
                    print("No matches found.")
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                break 