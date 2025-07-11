# SharePoint Company Analyzer

A Python-based NLP solution to extract company names from SharePoint file and folder exports. Specifically designed for analyzing the LPATech.csv file containing ~120,000 rows of SharePoint folder/file data.

## Features

- **Smart Company Detection**: Advanced filtering to identify actual company names vs technical files
- **Memory Efficient**: Processes large files in chunks to handle 120,000+ rows
- **Intelligent Filtering**: Removes technical files (NEM12/NEM13 energy data, BR files, etc.)
- **Multiple Output Formats**: JSON, CSV, and TXT results
- **Interactive Search**: Search through extracted companies
- **Detailed Analytics**: Provides frequency counts and company metadata
- **Fast Preview**: Quick preview mode for rapid analysis

## Files Structure

```
filefolderanalysis/
├── LPATech.csv                          # Your SharePoint export file (40MB)
├── requirements.txt                     # Python package dependencies
├── improved_company_analyzer.py         # Main analysis script (recommended)
├── setup.py                            # Installation and setup script
├── quick_analysis.py                   # Quick preview script
└── README.md                           # This file
```

## Installation

### Step 1: Setup Environment
```bash
# Run the setup script to install all dependencies
python setup.py
```

This will:
- Check your Python version
- Install required packages (pandas, spacy, nltk, etc.)
- Download the spaCy English model
- Verify LPATech.csv exists

### Step 2: Quick Preview (Optional)
```bash
# Get a quick preview of companies in the first 10,000 rows
python quick_analysis.py
```

### Step 3: Full Analysis (Recommended)
```bash
# Run the improved analysis on all rows with smart filtering
python improved_company_analyzer.py
```
## CSV File Structure

The analyzer expects a CSV file with these columns:
- **Name**: Folder/file names (primary source for company names)
- **Modified**: Modification dates
- **Modified By**: Person who modified the item
- **File Size**: Size of files
- **Item Type**: Folder or File
- **Path**: Full path in SharePoint

## Output Files

The analyzer generates timestamped files:

1. **companies_improved_YYYYMMDD_HHMMSS.json**: Basic results with company names and frequencies
2. **companies_detailed_improved_YYYYMMDD_HHMMSS.json**: Detailed results with paths and metadata
3. **companies_improved_YYYYMMDD_HHMMSS.csv**: Spreadsheet-friendly format
4. **companies_improved_YYYYMMDD_HHMMSS.txt**: Human-readable list with details

## Output File Formats

The analyzer generates 4 different output files with timestamps (YYYYMMDD_HHMMSS):

### 1. Basic JSON Format
**File**: `companies_improved_YYYYMMDD_HHMMSS.json`
```json
{
  "Accent Group": 142,
  "Cotton On": 98,
  "Digital Realty": 76,
  "Boston Properties": 54,
  "Jewish Care": 43
}
```
- Simple key-value pairs: company name → folder count
- Lightweight format for basic analysis
- Easy to parse programmatically

### 2. Detailed JSON Format
**File**: `companies_detailed_improved_YYYYMMDD_HHMMSS.json`
```json
{
  "Accent Group": {
    "company_name": "Accent Group",
    "folder_count": 142,
    "folders": ["Accent Group", "Accent AU RFQ", "Accent Calendar"],
    "paths": ["tech/Shared Documents/Managed Services/Accent Group"],
    "modified_by": ["Dasha Naumova", "Andrew Perry"],
    "file_types": ["Folder"]
  }
}
```
- Complete metadata for each company
- Includes all folder names, paths, and modification details
- Best for detailed analysis and verification

### 3. CSV Format (Spreadsheet)
**File**: `companies_improved_YYYYMMDD_HHMMSS.csv`
```csv
Company,Folder_Count
Accent Group,142
Cotton On,98
Digital Realty,76
Boston Properties,54
```
- Two columns: Company name and folder count
- Sorted by frequency (highest first)
- Perfect for Excel, Google Sheets, or data analysis

### 4. Human-Readable Text Format
**File**: `companies_improved_YYYYMMDD_HHMMSS.txt`
```
IMPROVED COMPANY ANALYSIS - LPATECH.CSV
============================================================
Total companies found: 13,434
Total folder entries: 14,443

TOP COMPANIES BY FOLDER COUNT:
----------------------------------------
  1. Accent Group                     (142 folders)
  2. Cotton On                        (98 folders)
  3. Digital Realty                   (76 folders)

COMPANY DETAILS:
----------------------------------------
Accent Group:
  Folders: 142
  Paths: 15
  Modified by: 8 people
  Types: Folder
```
- Complete summary with statistics
- Top companies ranked by frequency
- Detailed breakdown for each company
- Perfect for reports and documentation

## Interactive Features

After running the main analyzer, you can:
- Search for specific companies
- Get detailed information about any company
- View folder counts and paths

```
Search companies > accent
Found 1 matches:
  Accent Group (142 folders)

Search companies > bank
Found 3 matches:
  Berkshire Bank (43 folders)
  First National Bank (12 folders)
  Commonwealth Bank (8 folders)
```

## How It Works

1. **Smart Filtering**: Automatically removes technical files using regex patterns:
   - NEM12/NEM13 energy data files
   - BR numbered files and technical codes
   - Files with extensions (.csv, .xlsx, .pdf, etc.)
   - Templates and system folders

2. **Company Detection**: Uses multiple methods to identify companies:
   - **Pattern Recognition**: Looks for company suffixes (Inc, LLC, Corp, etc.)
   - **Proper Nouns**: Identifies capitalized business names
   - **Known Companies**: Maintains a list of recognized companies
   - **Context Analysis**: Considers folder paths and metadata

3. **Data Aggregation**: Counts occurrences and provides detailed metadata including:
   - Folder counts per company
   - File paths and locations
   - People who modified files
   - File types and categories

## Company Detection Examples

**Successfully Detected:**
- Accent Group ✓ (retail company)
- Boston Properties ✓ (real estate)
- Digital Realty ✓ (technology)
- Jewish Care ✓ (healthcare/services)
- AGL ✓ (energy utility)

**Correctly Filtered Out:**
- NEM12#EL0008EPV0#VRT#SRVCWORKS.csv (technical energy data)
- BR8.csv (numbered technical file)
- _MS Template (system template)
- 2024 Reports (generic folder)

## Requirements

- Python 3.7+
- pandas (data processing)
- numpy (numerical operations)
- spacy (NLP - optional, for enhanced detection)
- nltk (text processing - optional)
- tqdm (progress bars)

## Performance

- **Processing Speed**: ~20,000-25,000 rows per minute
- **Memory Usage**: ~200-500MB RAM for 120,000+ rows
- **Analysis Time**: Complete analysis takes 5-10 minutes
- **Smart Filtering**: Reduces noise by ~60% (70,105 technical files filtered)

## Troubleshooting

**"LPATech.csv not found"**
- Ensure the CSV file is in the same directory as the scripts
- Check the file name matches exactly: `LPATech.csv`

**Memory issues with large files**
- The analyzer processes files in chunks (default: 5,000 rows)
- Reduce chunk size if needed by editing the script

**Low company count**
- The improved analyzer is conservative to avoid false positives
- Check the detailed output files for comprehensive results
- Use the interactive search to find specific companies

## Customization

You can customize the analysis by editing `improved_company_analyzer.py`:

- **Filtering Rules**: Modify `exclude_patterns` to adjust what gets filtered
- **Company Indicators**: Update `company_indicators` to add business types
- **Known Companies**: Add to `known_companies` set for guaranteed detection
- **Chunk Size**: Adjust `chunk_size` for memory management

## Data Privacy

- All processing is done locally on your machine
- No data is sent to external services
- Results are saved locally in the same directory
- Source CSV file is never modified

## Support

If you encounter issues:
1. Run `python setup.py` to ensure all dependencies are installed
2. Try `python quick_analysis.py` for a fast preview
3. Check the generated log files for detailed error information
4. Verify your CSV file format matches the expected structure

## License

This project is provided as-is for analyzing SharePoint exports. Modify as needed for your specific use case. 