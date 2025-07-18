"""
Results Management Module

This module handles saving, formatting, and exporting analysis results
in various formats (JSON, CSV, TXT). It provides a clean interface
for managing company analysis output.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional, Counter
from datetime import datetime
import logging
from ..config.config import config
from .name_categorizer import NameCategorizer


class ResultsManager:
    """Manages analysis results and exports"""
    
    def __init__(self, base_filename: str = "companies"):
        """
        Initialize results manager
        
        Args:
            base_filename: Base name for output files
        """
        self.base_filename = base_filename
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = logging.getLogger(__name__)
        
        # Initialize name categorizer for offline analysis
        try:
            self.name_categorizer = NameCategorizer()
            self.logger.info("Name categorizer initialized successfully")
        except Exception as e:
            self.logger.warning(f"Failed to initialize name categorizer: {e}")
            self.name_categorizer = None
        
    def save_results(self, companies: Counter, company_details: Dict[str, Any], 
                    output_formats: Optional[List[str]] = None, filter_type: str = 'all') -> List[str]:
        """
        Save analysis results in multiple formats
        
        Args:
            companies: Counter object with company frequencies
            company_details: Dictionary with detailed company information
            output_formats: List of formats to save (default: all formats)
            filter_type: Type of items analyzed ('all', 'folders', 'files')
            
        Returns:
            List of created file paths
        """
        if not companies:
            self.logger.warning("No companies to save")
            return []
        
        output_formats = output_formats or config.output_formats
        created_files = []
        
        for format_type in output_formats:
            try:
                if format_type == 'json':
                    files = self._save_json(companies, company_details)
                    created_files.extend(files)
                elif format_type == 'csv':
                    file_path = self._save_csv(companies)
                    created_files.append(file_path)
                elif format_type == 'txt':
                    file_path = self._save_txt(companies, company_details, filter_type)
                    created_files.append(file_path)
                else:
                    self.logger.warning(f"Unknown output format: {format_type}")
                    
            except Exception as e:
                self.logger.error(f"Error saving {format_type} format: {str(e)}")
        
        return created_files
    
    def _save_json(self, companies: Counter, company_details: Dict[str, Any]) -> List[str]:
        """Save results in JSON format"""
        created_files = []
        
        # Basic JSON with company counts
        basic_file = f"{self.base_filename}_{self.timestamp}.json"
        try:
            with open(basic_file, 'w', encoding='utf-8') as f:
                json.dump(dict(companies), f, indent=2, ensure_ascii=False)
            created_files.append(basic_file)
            self.logger.info(f"Basic JSON saved: {basic_file}")
        except Exception as e:
            self.logger.error(f"Error saving basic JSON: {str(e)}")
        
        # Detailed JSON with full information
        detailed_file = f"{self.base_filename}_detailed_{self.timestamp}.json"
        try:
            detailed_data = {}
            for company in companies.keys():
                detailed_data[company] = self._format_company_details(company, company_details)
            
            with open(detailed_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_data, f, indent=2, ensure_ascii=False, default=str)
            created_files.append(detailed_file)
            self.logger.info(f"Detailed JSON saved: {detailed_file}")
        except Exception as e:
            self.logger.error(f"Error saving detailed JSON: {str(e)}")
        
        return created_files
    
    def _save_csv(self, companies: Counter) -> str:
        """Save results in CSV format with categorization"""
        csv_file = f"{self.base_filename}_{self.timestamp}.csv"
        
        try:
            # Prepare data with categorization
            csv_data = []
            
            for company, count in companies.most_common():
                # Get category and description
                if self.name_categorizer:
                    category, description = self.name_categorizer.categorize_name(company)
                else:
                    category = 'Unknown'
                    description = f'Name: {company}'
                
                csv_data.append({
                    'Name': company,
                    'Folder_Count': count,
                    'Category': category,
                    'Description': description
                })
            
            df = pd.DataFrame(csv_data)
            df.to_csv(csv_file, index=False)
            self.logger.info(f"Enhanced CSV saved: {csv_file}")
            return csv_file
        except Exception as e:
            self.logger.error(f"Error saving CSV: {str(e)}")
            return ""
    
    def _save_txt(self, companies: Counter, company_details: Dict[str, Any], filter_type: str = 'all') -> str:
        """Save results in human-readable text format"""
        txt_file = f"{self.base_filename}_{self.timestamp}.txt"
        
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                self._write_text_report(f, companies, company_details, filter_type)
            self.logger.info(f"Text report saved: {txt_file}")
            return txt_file
        except Exception as e:
            self.logger.error(f"Error saving text report: {str(e)}")
            return ""
    
    def _write_text_report(self, file_handle, companies: Counter, company_details: Dict[str, Any], filter_type: str = 'all'):
        """Write formatted text report"""
        f = file_handle
        
        # Header
        f.write(f"ENHANCED COMPANY ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Filter type: {filter_type}\n")
        f.write(f"Total names found: {len(companies):,}\n")
        f.write(f"Total folder entries: {sum(companies.values()):,}\n")
        
        # Category analysis
        if self.name_categorizer:
            f.write(f"Name categorization: ENABLED\n\n")
            
            # Get category summary
            company_names = list(companies.keys())
            category_summary = self.name_categorizer.get_category_summary(company_names)
            
            f.write("NAME CATEGORIZATION SUMMARY:\n")
            f.write("-" * 40 + "\n")
            for category, count in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
                f.write(f"{category:<25} {count:3d} names\n")
            f.write("\n")
        else:
            f.write(f"Name categorization: DISABLED\n\n")
        
        # Top companies
        f.write("TOP NAMES BY FOLDER COUNT:\n")
        f.write("-" * 40 + "\n")
        
        for i, (company, count) in enumerate(companies.most_common(config.max_summary_companies), 1):
            if self.name_categorizer:
                category, description = self.name_categorizer.categorize_name(company)
                f.write(f"{i:3d}. {company:<30} ({count:3d} folders) - {category}\n")
            else:
                f.write(f"{i:3d}. {company:<40} ({count:3d} folders)\n")
        
        # Distribution analysis
        counts = list(companies.values())
        f.write(f"\nDISTRIBUTION ANALYSIS:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Companies with 1 folder:      {sum(1 for c in counts if c == 1):3d}\n")
        f.write(f"Companies with 2-5 folders:   {sum(1 for c in counts if 2 <= c <= 5):3d}\n")
        f.write(f"Companies with 6-10 folders:  {sum(1 for c in counts if 6 <= c <= 10):3d}\n")
        f.write(f"Companies with 11-20 folders: {sum(1 for c in counts if 11 <= c <= 20):3d}\n")
        f.write(f"Companies with 21+ folders:   {sum(1 for c in counts if c > 20):3d}\n")
        
        # Detailed name information
        f.write("\nDETAILED NAME INFORMATION:\n")
        f.write("-" * 40 + "\n")
        
        for company in sorted(companies.keys()):
            details = self._format_company_details(company, company_details)
            f.write(f"\n{company}:\n")
            
            # Add categorization information
            if self.name_categorizer:
                category, description = self.name_categorizer.categorize_name(company)
                f.write(f"  Category: {category}\n")
                f.write(f"  Description: {description}\n")
            
            f.write(f"  Folders: {details['folder_count']}\n")
            f.write(f"  Unique paths: {len(details['paths'])}\n")
            f.write(f"  Modified by: {len(details['modified_by'])} people\n")
            if details['file_types']:
                f.write(f"  File types: {', '.join(details['file_types'])}\n")
        
        # Footer
        f.write(f"\nNote: Technical files and system folders have been filtered out.\n")
        if filter_type != 'all':
            f.write(f"Analysis filtered to {filter_type} only.\n")
        if self.name_categorizer:
            f.write("This enhanced report includes intelligent name categorization to distinguish\n")
            f.write("between actual companies and other entities like abbreviations, technical terms,\n")
            f.write("and document references.\n")
        else:
            f.write("This report focuses on detected names that may include companies and other entities.\n")
    
    def _format_company_details(self, company: str, company_details: Dict[str, Any]) -> Dict[str, Any]:
        """Format detailed company information"""
        if company not in company_details:
            return {
                'company_name': company,
                'folder_count': 0,
                'folders': [],
                'paths': [],
                'modified_by': [],
                'file_types': []
            }
        
        details = company_details[company]
        return {
            'company_name': company,
            'folder_count': int(details.get('count', 0)),
            'folders': sorted(list(details.get('folders', set()))),
            'paths': sorted(list(details.get('paths', set()))),
            'modified_by': sorted(list(details.get('modified_by', set()))),
            'file_types': sorted(list(details.get('file_types', set())))
        }
    
    def print_summary(self, companies: Counter, company_details: Dict[str, Any], filter_type: str = 'all'):
        """Print a summary of the analysis results"""
        if not companies:
            print("No analysis results available.")
            return
        
        print("\n" + "="*80)
        print("ENHANCED COMPANY ANALYSIS SUMMARY")
        print("="*80)
        print(f"Filter type: {filter_type}")
        print(f"Total unique names found: {len(companies):,}")
        print(f"Total folder entries: {sum(companies.values()):,}")
        
        # Category analysis
        if self.name_categorizer:
            print(f"Name categorization: ENABLED")
            
            # Get category summary
            company_names = list(companies.keys())
            category_summary = self.name_categorizer.get_category_summary(company_names)
            
            print(f"\nName Categorization Summary:")
            print("-" * 40)
            for category, count in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(companies)) * 100
                print(f"{category:<25} {count:3d} names ({percentage:5.1f}%)")
        else:
            print(f"Name categorization: DISABLED")
        
        print(f"\nTop {min(config.max_summary_companies, len(companies))} Names by Folder Count:")
        print("-" * 60)
        for i, (company, count) in enumerate(companies.most_common(config.max_summary_companies), 1):
            if self.name_categorizer:
                category, description = self.name_categorizer.categorize_name(company)
                print(f"{i:2d}. {company:<35} ({count:3d} folders) - {category}")
            else:
                print(f"{i:2d}. {company:<45} ({count:3d} folders)")
        
        # Distribution statistics
        counts = list(companies.values())
        print(f"\nDistribution Analysis:")
        print("-" * 30)
        print(f"Companies with 1 folder:      {sum(1 for c in counts if c == 1):3d}")
        print(f"Companies with 2-5 folders:   {sum(1 for c in counts if 2 <= c <= 5):3d}")
        print(f"Companies with 6-10 folders:  {sum(1 for c in counts if 6 <= c <= 10):3d}")
        print(f"Companies with 11-20 folders: {sum(1 for c in counts if 11 <= c <= 20):3d}")
        print(f"Companies with 21+ folders:   {sum(1 for c in counts if c > 20):3d}")
        
        print(f"\nNote: Technical files and system folders have been filtered out.")
        if filter_type != 'all':
            print(f"Analysis filtered to {filter_type} only.")
        print("Results focus on actual company/organization names.")
    
    def search_companies(self, companies: Counter, query: str) -> List[tuple]:
        """
        Search for companies matching a query
        
        Args:
            companies: Counter object with company data
            query: Search query
            
        Returns:
            List of (company, count) tuples matching the query
        """
        if not companies:
            return []
        
        query_lower = query.lower()
        matches = []
        
        for company, count in companies.items():
            if query_lower in company.lower():
                matches.append((company, count))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    

    
    def get_file_list(self) -> List[str]:
        """Get list of expected output files"""
        return [
            f"{self.base_filename}_{self.timestamp}.json",
            f"{self.base_filename}_detailed_{self.timestamp}.json",
            f"{self.base_filename}_{self.timestamp}.csv",
            f"{self.base_filename}_{self.timestamp}.txt"
        ] 