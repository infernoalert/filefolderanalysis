"""
Configuration settings for the Company Analyzer

This module contains all configuration parameters including:
- Exclusion patterns for technical files
- Company detection patterns
- Known companies list
- Default settings
- Environment variable support
- Configuration loading from external files
- Validation and error handling
"""

from typing import List, Dict, Any, Optional, Union
import re
import json
import os
import logging
from pathlib import Path
from functools import lru_cache
import yaml


class ConfigurationError(Exception):
    """Custom exception for configuration-related errors"""
    pass


class AnalyzerConfig:
    """Configuration class for the company analyzer with enhanced features"""
    
    def __init__(self, config_file: Optional[str] = None, environment: str = "default"):
        """
        Initialize configuration
        
        Args:
            config_file: Path to external configuration file (JSON/YAML)
            environment: Configuration environment (default, dev, prod, test)
        """
        self.environment = environment
        self._compiled_patterns_cache = None
        self._compiled_indicators_cache = None
        
        # Load default settings first
        self._load_defaults()
        
        # Load from file if provided
        if config_file:
            self.load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_environment()
        
        # Validate configuration
        self.validate()
        
        # Setup logging if requested
        if self.enable_logging:
            self._setup_logging()
    
    def _load_defaults(self):
        """Load default configuration values"""
        # Core processing settings
        self.chunk_size = int(os.getenv('ANALYZER_CHUNK_SIZE', '5000'))
        self.default_csv_file = os.getenv('ANALYZER_DEFAULT_CSV', "LPATech.csv")
        self.min_company_name_length = int(os.getenv('ANALYZER_MIN_COMPANY_LENGTH', '2'))
        self.max_company_name_length = int(os.getenv('ANALYZER_MAX_COMPANY_LENGTH', '50'))
        self.filter_type = os.getenv('ANALYZER_FILTER_TYPE', 'all')  # Options: 'all', 'folders', 'files'
        
        # Performance settings
        self.max_workers = int(os.getenv('ANALYZER_MAX_WORKERS', '4'))
        self.cache_size = int(os.getenv('ANALYZER_CACHE_SIZE', '1000'))
        self.enable_caching = os.getenv('ANALYZER_ENABLE_CACHING', 'true').lower() == 'true'
        
        # Logging settings
        self.enable_logging = os.getenv('ANALYZER_ENABLE_LOGGING', 'true').lower() == 'true'
        self.log_level = os.getenv('ANALYZER_LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('ANALYZER_LOG_FILE', 'company_analyzer.log')
        self.log_format = os.getenv('ANALYZER_LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Detection thresholds
        self.confidence_threshold = float(os.getenv('ANALYZER_CONFIDENCE_THRESHOLD', '0.3'))
        self.strict_mode = os.getenv('ANALYZER_STRICT_MODE', 'false').lower() == 'true'
        
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
        self.max_search_results = int(os.getenv('ANALYZER_MAX_SEARCH_RESULTS', '10'))
        self.max_summary_companies = int(os.getenv('ANALYZER_MAX_SUMMARY_COMPANIES', '50'))
        self.output_directory = os.getenv('ANALYZER_OUTPUT_DIR', 'output')
        
        # Enhanced detection settings (for NLP features)
        self.enable_enhanced_detection = os.getenv('ANALYZER_ENABLE_ENHANCED', 'true').lower() == 'true'
        self.spacy_model = os.getenv('ANALYZER_SPACY_MODEL', 'en_core_web_sm')
        self.enable_parallel_processing = os.getenv('ANALYZER_ENABLE_PARALLEL', 'false').lower() == 'true'
    
    def _load_from_environment(self):
        """Load configuration from environment variables"""
        # Environment-specific overrides can be added here
        env_prefix = f"ANALYZER_{self.environment.upper()}_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                if hasattr(self, config_key):
                    current_value = getattr(self, config_key)
                    # Type conversion based on current value type
                    if isinstance(current_value, bool):
                        setattr(self, config_key, value.lower() == 'true')
                    elif isinstance(current_value, int):
                        setattr(self, config_key, int(value))
                    elif isinstance(current_value, float):
                        setattr(self, config_key, float(value))
                    else:
                        setattr(self, config_key, value)
    
    def load_from_file(self, config_file: str) -> None:
        """
        Load configuration from external file (JSON or YAML)
        
        Args:
            config_file: Path to configuration file
            
        Raises:
            ConfigurationError: If file cannot be loaded or parsed
        """
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                raise ConfigurationError(f"Configuration file not found: {config_file}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    try:
                        import yaml
                        data = yaml.safe_load(f)
                    except ImportError:
                        raise ConfigurationError("PyYAML is required for YAML configuration files")
                elif config_path.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    raise ConfigurationError(f"Unsupported configuration file format: {config_path.suffix}")
            
            # Apply configuration
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    logging.warning(f"Unknown configuration key: {key}")
                    
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration from {config_file}: {str(e)}")
    
    def save_to_file(self, config_file: str, format_type: str = 'json') -> None:
        """
        Save current configuration to file
        
        Args:
            config_file: Path to save configuration
            format_type: Format to save in ('json' or 'yaml')
            
        Raises:
            ConfigurationError: If file cannot be saved
        """
        try:
            config_data = self.to_dict()
            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                if format_type.lower() == 'yaml':
                    try:
                        import yaml
                        yaml.dump(config_data, f, default_flow_style=False, indent=2)
                    except ImportError:
                        raise ConfigurationError("PyYAML is required for YAML configuration files")
                else:
                    json.dump(config_data, f, indent=2, default=str)
                    
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration to {config_file}: {str(e)}")
    
    def validate(self) -> None:
        """
        Validate configuration values
        
        Raises:
            ConfigurationError: If configuration is invalid
        """
        errors = []
        
        # Validate numeric ranges
        if self.chunk_size <= 0:
            errors.append("chunk_size must be positive")
        
        if self.min_company_name_length < 1:
            errors.append("min_company_name_length must be at least 1")
            
        if self.max_company_name_length <= self.min_company_name_length:
            errors.append("max_company_name_length must be greater than min_company_name_length")
        
        if not 0 <= self.confidence_threshold <= 1:
            errors.append("confidence_threshold must be between 0 and 1")
        
        # Validate filter type
        if self.filter_type not in ['all', 'folders', 'files']:
            errors.append(f"Invalid filter_type: {self.filter_type}")
        
        # Validate output formats
        valid_formats = ['json', 'csv', 'txt', 'xlsx']
        for fmt in self.output_formats:
            if fmt not in valid_formats:
                errors.append(f"Invalid output format: {fmt}")
        
        # Validate regex patterns
        for i, pattern in enumerate(self.exclude_patterns):
            try:
                re.compile(pattern)
            except re.error as e:
                errors.append(f"Invalid exclude pattern {i}: {e}")
        
        for i, pattern in enumerate(self.company_indicators):
            try:
                re.compile(pattern)
            except re.error as e:
                errors.append(f"Invalid company indicator pattern {i}: {e}")
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_log_levels:
            errors.append(f"Invalid log_level: {self.log_level}")
        
        if errors:
            raise ConfigurationError("Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))
    
    @lru_cache(maxsize=1)
    def get_compiled_patterns(self) -> List[re.Pattern]:
        """Get compiled regex patterns for exclusion (cached)"""
        if not self.enable_caching or self._compiled_patterns_cache is None:
            self._compiled_patterns_cache = [re.compile(pattern, re.IGNORECASE) for pattern in self.exclude_patterns]
        return self._compiled_patterns_cache
    
    @lru_cache(maxsize=1)
    def get_compiled_company_indicators(self) -> List[re.Pattern]:
        """Get compiled regex patterns for company indicators (cached)"""
        if not self.enable_caching or self._compiled_indicators_cache is None:
            self._compiled_indicators_cache = [re.compile(pattern, re.IGNORECASE) for pattern in self.company_indicators]
        return self._compiled_indicators_cache
    
    def clear_cache(self) -> None:
        """Clear compiled pattern caches"""
        self._compiled_patterns_cache = None
        self._compiled_indicators_cache = None
        # Clear LRU cache
        self.get_compiled_patterns.cache_clear()
        self.get_compiled_company_indicators.cache_clear()
    
    def add_known_company(self, company_name: str) -> None:
        """
        Add a new known company
        
        Args:
            company_name: Company name to add
            
        Raises:
            ConfigurationError: If company name is invalid
        """
        if not company_name or not company_name.strip():
            raise ConfigurationError("Company name cannot be empty")
        
        company_name = company_name.strip()
        if len(company_name) < self.min_company_name_length:
            raise ConfigurationError(f"Company name too short: {company_name}")
        
        if len(company_name) > self.max_company_name_length:
            raise ConfigurationError(f"Company name too long: {company_name}")
        
        self.known_companies.add(company_name)
    
    def add_exclude_pattern(self, pattern: str) -> None:
        """
        Add a new exclusion pattern
        
        Args:
            pattern: Regex pattern to add
            
        Raises:
            ConfigurationError: If pattern is invalid
        """
        try:
            re.compile(pattern)
        except re.error as e:
            raise ConfigurationError(f"Invalid regex pattern: {pattern} - {e}")
        
        self.exclude_patterns.append(pattern)
        self.clear_cache()  # Clear cache to force recompilation
    
    def add_company_indicator(self, pattern: str) -> None:
        """
        Add a new company indicator pattern
        
        Args:
            pattern: Regex pattern to add
            
        Raises:
            ConfigurationError: If pattern is invalid
        """
        try:
            re.compile(pattern)
        except re.error as e:
            raise ConfigurationError(f"Invalid regex pattern: {pattern} - {e}")
        
        self.company_indicators.append(pattern)
        self.clear_cache()  # Clear cache to force recompilation
    
    def set_csv_column_mapping(self, column_mappings: Dict[str, str]) -> None:
        """
        Set custom CSV column mappings
        
        Args:
            column_mappings: Dictionary mapping internal names to CSV column names
        """
        if not isinstance(column_mappings, dict):
            raise ConfigurationError("Column mappings must be a dictionary")
        
        self.csv_columns.update(column_mappings)
    
    def set_filter_type(self, filter_type: str) -> None:
        """
        Set the filter type for analysis
        
        Args:
            filter_type: Filter type ('all', 'folders', 'files')
            
        Raises:
            ConfigurationError: If filter type is invalid
        """
        if filter_type not in ['all', 'folders', 'files']:
            raise ConfigurationError(f"Invalid filter type: {filter_type}. Must be 'all', 'folders', or 'files'")
        self.filter_type = filter_type
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary
        
        Returns:
            Dictionary representation of configuration
        """
        config_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and not callable(value):
                if isinstance(value, set):
                    config_dict[key] = list(value)
                else:
                    config_dict[key] = value
        return config_dict
    
    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get information about the current environment
        
        Returns:
            Dictionary with environment information
        """
        return {
            'environment': self.environment,
            'config_file': getattr(self, 'config_file', None),
            'enable_enhanced_detection': self.enable_enhanced_detection,
            'enable_caching': self.enable_caching,
            'enable_parallel_processing': self.enable_parallel_processing,
            'log_level': self.log_level,
            'strict_mode': self.strict_mode,
            'cache_size': self.cache_size
        }
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        try:
            # Convert string log level to logging constant
            log_level = getattr(logging, self.log_level.upper())
            
            # Create logger
            logger = logging.getLogger('company_analyzer')
            logger.setLevel(log_level)
            
            # Avoid duplicate handlers
            if not logger.handlers:
                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_level)
                console_formatter = logging.Formatter(self.log_format)
                console_handler.setFormatter(console_formatter)
                logger.addHandler(console_handler)
                
                # File handler
                if self.log_file:
                    file_handler = logging.FileHandler(self.log_file)
                    file_handler.setLevel(log_level)
                    file_formatter = logging.Formatter(self.log_format)
                    file_handler.setFormatter(file_formatter)
                    logger.addHandler(file_handler)
                    
        except Exception as e:
            print(f"Warning: Failed to setup logging: {e}")
    
    def reload(self, config_file: Optional[str] = None) -> None:
        """
        Reload configuration
        
        Args:
            config_file: Optional new configuration file to load
        """
        self.clear_cache()
        self._load_defaults()
        
        if config_file:
            self.load_from_file(config_file)
        
        self._load_from_environment()
        self.validate()


# Create default configuration instance
config = AnalyzerConfig() 