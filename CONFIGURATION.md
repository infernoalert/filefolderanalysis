# Configuration Guide

This guide explains how to configure the Company Analyzer with the enhanced configuration system.

## Quick Start

### Basic Usage (Default Configuration)
```python
from config import config
# Uses default settings and environment variables
```

### Load from Configuration File
```python
from config import AnalyzerConfig

# Load from JSON
config = AnalyzerConfig(config_file="my_config.json")

# Load from YAML
config = AnalyzerConfig(config_file="my_config.yaml")

# Specify environment
config = AnalyzerConfig(config_file="config.yaml", environment="production")
```

## Configuration Methods

### 1. Environment Variables
Set environment variables with the `ANALYZER_` prefix:

```bash
# Core settings
export ANALYZER_CHUNK_SIZE=3000
export ANALYZER_DEFAULT_CSV="my_data.csv"
export ANALYZER_FILTER_TYPE="folders"

# Performance settings
export ANALYZER_MAX_WORKERS=6
export ANALYZER_ENABLE_CACHING=true
export ANALYZER_ENABLE_PARALLEL=true

# Logging
export ANALYZER_LOG_LEVEL="DEBUG"
export ANALYZER_LOG_FILE="analyzer.log"

# Detection settings
export ANALYZER_CONFIDENCE_THRESHOLD=0.5
export ANALYZER_STRICT_MODE=true
export ANALYZER_ENABLE_ENHANCED=true
```

### 2. Environment-Specific Variables
Use environment-specific prefixes for different deployment environments:

```bash
# Development environment
export ANALYZER_DEV_LOG_LEVEL="DEBUG"
export ANALYZER_DEV_CHUNK_SIZE=1000

# Production environment
export ANALYZER_PROD_LOG_LEVEL="WARNING"
export ANALYZER_PROD_CHUNK_SIZE=10000
export ANALYZER_PROD_ENABLE_PARALLEL=true
```

Then load with:
```python
config = AnalyzerConfig(environment="dev")  # or "prod"
```

### 3. Configuration Files

#### JSON Configuration
Create a `config.json` file:
```json
{
  "chunk_size": 3000,
  "enable_enhanced_detection": true,
  "log_level": "DEBUG",
  "known_companies": ["My Company Inc", "Another Corp"],
  "exclude_patterns": ["^TEST_.*", ".*_BACKUP$"]
}
```

#### YAML Configuration (Recommended)
Create a `config.yaml` file:
```yaml
# Core settings
chunk_size: 3000
filter_type: "folders"

# Detection settings
confidence_threshold: 0.5
strict_mode: true

# Known companies
known_companies:
  - "My Company Inc"
  - "Another Corp"

# Custom patterns
exclude_patterns:
  - "^TEST_.*"
  - ".*_BACKUP$"
```

## Configuration Options

### Core Processing Settings
- `chunk_size` (int): Number of rows to process at once (default: 5000)
- `default_csv_file` (str): Default CSV file to analyze (default: "LPATech.csv")
- `min_company_name_length` (int): Minimum company name length (default: 2)
- `max_company_name_length` (int): Maximum company name length (default: 50)
- `filter_type` (str): Type of items to analyze - "all", "folders", or "files" (default: "all")

### Performance Settings
- `max_workers` (int): Maximum number of worker threads (default: 4)
- `cache_size` (int): Cache size for compiled patterns (default: 1000)
- `enable_caching` (bool): Enable pattern caching (default: true)
- `enable_parallel_processing` (bool): Enable parallel processing (default: false)

### Detection Settings
- `confidence_threshold` (float): Minimum confidence for company detection (0.0-1.0, default: 0.3)
- `strict_mode` (bool): Enable strict validation (default: false)
- `enable_enhanced_detection` (bool): Use NLP-enhanced detection (default: true)
- `spacy_model` (str): spaCy model to use (default: "en_core_web_sm")

### Logging Settings
- `enable_logging` (bool): Enable logging (default: true)
- `log_level` (str): Log level - DEBUG, INFO, WARNING, ERROR, CRITICAL (default: "INFO")
- `log_file` (str): Log file path (default: "company_analyzer.log")
- `log_format` (str): Log message format

### Output Settings
- `output_formats` (list): Output formats - json, csv, txt, xlsx (default: ["json", "csv", "txt"])
- `max_search_results` (int): Maximum search results to return (default: 10)
- `max_summary_companies` (int): Maximum companies in summary (default: 50)
- `output_directory` (str): Directory for output files (default: "output")

## Advanced Usage

### Custom Company Detection
```python
from config import AnalyzerConfig, ConfigurationError

config = AnalyzerConfig()

# Add known companies
config.add_known_company("My Custom Company Inc")

# Add exclusion patterns
config.add_exclude_pattern(r"^CUSTOM_.*")

# Add company indicator patterns  
config.add_company_indicator(r"\b(startup|venture)\b")
```

### Configuration Validation
```python
try:
    config = AnalyzerConfig("invalid_config.json")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

### Save Current Configuration
```python
# Save as JSON
config.save_to_file("current_config.json", "json")

# Save as YAML
config.save_to_file("current_config.yaml", "yaml")
```

### Configuration Export
```python
# Get configuration as dictionary
config_dict = config.to_dict()

# Get environment information
env_info = config.get_environment_info()
print(f"Environment: {env_info['environment']}")
print(f"Enhanced detection: {env_info['enable_enhanced_detection']}")
```

### Cache Management
```python
# Clear compiled pattern caches
config.clear_cache()

# Reload configuration
config.reload()  # Reload from original sources
config.reload("new_config.yaml")  # Load new config file
```

## Error Handling

The enhanced configuration system includes comprehensive error handling:

```python
from config import ConfigurationError

try:
    config = AnalyzerConfig("config.yaml")
except ConfigurationError as e:
    print(f"Configuration failed: {e}")
    # Handle configuration errors appropriately
```

Common errors:
- Invalid file paths
- Malformed JSON/YAML
- Invalid regex patterns
- Out-of-range values
- Missing required dependencies

## Best Practices

### 1. Use YAML for Human-Readable Configs
YAML is more readable and supports comments:
```yaml
# This is a comment
chunk_size: 3000  # Process 3000 rows at a time
```

### 2. Environment-Specific Configurations
Use different configurations for different environments:
- `config_dev.yaml` for development
- `config_prod.yaml` for production
- `config_test.yaml` for testing

### 3. Validate Configurations
Always validate configurations in production:
```python
config = AnalyzerConfig("prod_config.yaml")
config.validate()  # Raises ConfigurationError if invalid
```

### 4. Use Environment Variables for Secrets
Don't put sensitive information in config files:
```bash
export ANALYZER_API_KEY="secret_key"
export ANALYZER_DATABASE_PASSWORD="secret_password"
```

### 5. Version Control Configuration
- Include example config files in version control
- Don't include actual config files with sensitive data
- Use `.gitignore` to exclude sensitive configs

## Migration from Old Configuration

If you're upgrading from the old configuration system:

1. **Backup your current config.py modifications**
2. **Create a new configuration file** based on your current settings
3. **Update your code** to use the new configuration loading:

```python
# Old way
from config import config

# New way - same result if no config file specified
from config import config  # Still works!

# Or explicitly load from file
config = AnalyzerConfig("my_config.yaml")
```

## Troubleshooting

### PyYAML Not Found
```bash
pip install PyYAML>=6.0
```

### Invalid Regex Patterns
Check regex patterns using online validators or Python:
```python
import re
try:
    re.compile(r"your_pattern_here")
    print("Pattern is valid")
except re.error as e:
    print(f"Invalid pattern: {e}")
```

### Environment Variables Not Working
Check environment variable names and values:
```bash
printenv | grep ANALYZER_
```

### Configuration Not Loading
Enable debug logging to see what's happening:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
config = AnalyzerConfig("config.yaml")
``` 