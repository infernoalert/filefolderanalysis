"""
Configuration settings for the Company Analyzer

This module contains all configuration parameters including:
- Exclusion patterns for technical files
- Company detection patterns
- Known companies list
- Default settings
"""

from typing import List, Dict, Any
import re

class AnalyzerConfig:
    """Configuration class for the company analyzer"""
    
    def __init__(self):
        self.chunk_size = 5000
        self.default_csv_file = "LPATech.csv"
        self.min_company_name_length = 2
        self.max_company_name_length = 50
        self.filter_type = 'all'  # Options: 'all', 'folders', 'files'
        
        # Exclusion patterns for technical files
        self.exclude_patterns = [
            r'^NEM1[23]#.*',  # NEM12, NEM13 energy files
            r'^EL\d{4}EP[VA]\d\.csv$',  # Energy meter files
            r'^BR\d+\.csv$',  # BR numbered files
            r'^RC\d{4}VT[A-Z]\d+#.*',  # Technical reference files
            r'.*\.(csv|xlsx|xls|docx|doc|pptx|ppt|pdf|zip|log|msg|ods|xlsb)$',  # Files with extensions
            r'^_.*',  # Underscore prefixed
            r'^\d{4}.*',  # Year prefixed
            r'^[A-Z]{2,3}\d+.*',  # Technical codes
            r'.*[#@].*',  # Files with special characters
            r'^(Archive|Migration|Opportunities|Projects|Managed Services|Template|Folder|Reports|Data|Files|Documents)$',  # Common folder names
            r'.*Timesheet.*',  # Timesheet files
            r'.*Reconciliation.*',  # Reconciliation files
            r'.*Invoice.*',  # Invoice files
            r'.*Sample.*',  # Sample files
            r'.*Report.*',  # Report files
            r'.*How to.*',  # How-to files
            r'.*Meeting.*',  # Meeting files
            r'.*Implementation.*',  # Implementation files
            r'.*Acc\d+.*',  # Account numbers
            r'.*FY\d{2}.*',  # Financial year references
            r'.*\d{4}-\d{2}-\d{2}.*',  # Date patterns
            r'.*\d{8}.*',  # Date stamps
        ]
        
        # Company indicator patterns
        self.company_indicators = [
            r'\b(inc|incorporated|llc|corp|corporation|company|co|ltd|limited|pty|plc)\b',
            r'\b(group|holdings|partners|associates|solutions|services|technologies|systems)\b',
            r'\b(consulting|enterprises|international|global|worldwide)\b',
            r'\b(bank|financial|properties|realty|capital|investments|fund|trust)\b',
            r'\b(insurance|healthcare|medical|pharmaceuticals|biotech)\b',
            r'\b(energy|oil|gas|utilities|mining|construction|manufacturing)\b',
            r'\b(retail|hospitality|restaurants|hotels|airlines|logistics|transport)\b',
            r'\b(communications|media|entertainment|software|tech|technology)\b',
            r'\b(university|college|school|hospital|clinic|care|legal|law)\b',
            r'\b(accounting|advisory|management|consulting|professional)\b'
        ]
        
        # Known companies (can be expanded)
        self.known_companies = {
            'Accent Group', 'AGL', 'BXP', 'Altogether', 'Cleanpeak', 'Cotton On',
            'Digital Realty', 'EnerConnex', 'GCG', 'Jewish Care', 'Berkshire Bank',
            'Boston Properties', 'Bright and Duggan'
        }
        
        # Common non-company words to exclude
        self.exclude_words = {
            'Archive', 'Migration', 'Projects', 'Documents', 'Files', 'Folders', 
            'Templates', 'Forms', 'Reports', 'Data', 'Information', 'Resources', 
            'Tools', 'Utilities', 'Settings', 'Configuration', 'Administration', 
            'Management', 'Operations', 'Support', 'Help', 'Training', 'Education', 
            'Research', 'Development', 'Testing', 'Production', 'Staging', 'Backup', 
            'Recovery', 'Security', 'Privacy', 'Compliance', 'Audit', 'Finance', 
            'Accounting', 'Legal', 'Human', 'Resources', 'Marketing', 'Sales', 
            'Customer', 'Service', 'Quality', 'Agreements', 'Contracts', 'Thermal', 
            'Active', 'Apportionment', 'Accuracy', 'April', 'March'
        }
        
        # CSV column mappings (can be customized for different CSV structures)
        self.csv_columns = {
            'name': 'Name',
            'path': 'Path',
            'modified_by': 'Modified By',
            'item_type': 'Item Type',
            'file_size': 'File Size',
            'modified': 'Modified'
        }
        
        # Output settings
        self.output_formats = ['json', 'csv', 'txt']
        self.max_search_results = 10
        self.max_summary_companies = 50
        
    def get_compiled_patterns(self) -> List[re.Pattern]:
        """Get compiled regex patterns for exclusion"""
        return [re.compile(pattern, re.IGNORECASE) for pattern in self.exclude_patterns]
    
    def get_compiled_company_indicators(self) -> List[re.Pattern]:
        """Get compiled regex patterns for company indicators"""
        return [re.compile(pattern, re.IGNORECASE) for pattern in self.company_indicators]
    
    def add_known_company(self, company_name: str) -> None:
        """Add a new known company"""
        self.known_companies.add(company_name)
    
    def add_exclude_pattern(self, pattern: str) -> None:
        """Add a new exclusion pattern"""
        self.exclude_patterns.append(pattern)
    
    def set_csv_column_mapping(self, column_mappings: Dict[str, str]) -> None:
        """Set custom CSV column mappings"""
        self.csv_columns.update(column_mappings)
    
    def set_filter_type(self, filter_type: str) -> None:
        """Set the filter type for analysis"""
        if filter_type in ['all', 'folders', 'files']:
            self.filter_type = filter_type
        else:
            raise ValueError(f"Invalid filter type: {filter_type}. Must be 'all', 'folders', or 'files'")

# Create default configuration instance
config = AnalyzerConfig() 