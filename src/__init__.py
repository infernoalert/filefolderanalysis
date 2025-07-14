"""
Company Analyzer Package

A comprehensive Python package for analyzing CSV files and extracting company names
with AI-enhanced detection capabilities and MCP server integration.
"""

__version__ = "1.0.0"
__author__ = "Company Analyzer Team"
__email__ = "info@companyanalyzer.com"

# Import core modules at package level
from .core.company_analyzer import CompanyAnalyzer
from .core.company_detector import CompanyDetector
from .core.enhanced_company_detector import EnhancedCompanyDetector
from .core.csv_processor import CSVProcessor
from .core.results_manager import ResultsManager
from .config.config import AnalyzerConfig

__all__ = [
    # Core
    "CompanyAnalyzer",
    "CompanyDetector", 
    "EnhancedCompanyDetector",
    "CSVProcessor",
    "ResultsManager",
    
    # Config
    "AnalyzerConfig"
] 