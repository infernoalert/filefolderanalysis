# Local Configuration Guide

## Overview
I've cleaned up the configuration files to focus ONLY on what's needed for **local analysis**. All AI, online, and advanced features have been removed to eliminate confusion.

## Key Configuration: `filter_type`

**This is the setting you were looking for!** It controls what gets analyzed:

```json
"filter_type": "all"
```

### Options:
- `"all"` - Analyze both files and folders (default)
- `"folders"` - Only analyze folders
- `"files"` - Only analyze files (excluding folders)

## Configuration Files

### 1. `local_config_sample.json`
- **Format**: JSON
- **Use**: Easy to read and edit
- **Best for**: Simple configuration

### 2. `config_example.yaml` (in src/config/)
- **Format**: YAML  
- **Use**: More readable with comments
- **Best for**: Understanding all options

## Essential Settings Explained

### What to Analyze
```yaml
filter_type: "all"  # What to analyze: "all", "folders", or "files"
```

### CSV Column Mapping
```yaml
csv_columns:
  name: "Name"           # Column with file/folder names
  item_type: "Item Type" # Column that says "File" or "Folder"
  path: "Path"           # Column with file paths
```

**Important**: If your CSV has different column names, update these mappings!

### Processing Settings
```yaml
chunk_size: 5000              # Rows to process at once
confidence_threshold: 0.3     # How sure to be about company detection
```

### Output Settings
```yaml
output_formats: ["json", "csv", "txt"]  # Which formats to save
max_summary_companies: 50               # How many to show in results
```

## What Was Removed

To simplify for local usage, I removed:
- ❌ AI/OpenAI settings
- ❌ MCP server settings  
- ❌ Advanced NLP configuration
- ❌ Complex logging options
- ❌ Performance tuning settings
- ❌ Parallel processing options
- ❌ Custom patterns and indicators

## How to Use

1. **Copy the config file** you prefer to your project
2. **Update CSV column mappings** to match your file structure
3. **Set `filter_type`** to what you want to analyze:
   - `"all"` for everything
   - `"folders"` for folders only
   - `"files"` for files only
4. **Adjust other settings** as needed

## Example: Analyzing Only Folders

```json
{
  "filter_type": "folders",
  "csv_columns": {
    "name": "Name",
    "item_type": "Item Type"
  }
}
```

This will only analyze rows where `Item Type` column contains "Folder".

## Example: Custom CSV Structure

If your CSV has different column names:

```json
{
  "csv_columns": {
    "name": "Company Name",        # Your CSV column name
    "path": "File Path",           # Your CSV column name  
    "item_type": "Type",           # Your CSV column name
    "modified_by": "Author"        # Your CSV column name
  }
}
```

## Questions?

The configuration is now much simpler and focused on local usage only. The main setting you were looking for is `filter_type` - it controls whether to analyze files, folders, or both! 