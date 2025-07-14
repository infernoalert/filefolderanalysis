# 📁 File Folder Analysis Tool - Simple UI

A user-friendly web interface for analyzing CSV files and extracting company names with both local and AI-enhanced analysis capabilities.

## 🚀 Quick Start

### 1. Install and Launch

```bash
# Run the launcher script (it handles everything automatically)
python run_ui.py
```

**Or manually:**

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the UI
streamlit run app.py
```

### 2. Access the Application

The application will automatically open in your web browser at:
- **URL**: `http://localhost:8501`
- **Port**: 8501 (default)

## 📋 How to Use

### Step 1: Choose Analysis Mode

**In the sidebar, select:**
- **Local (Offline)**: Fast analysis without internet connection
- **AI-Enhanced Analysis**: AI-powered business insights (when configured)

### Step 2: Upload Files

**Upload your CSV file:**
- Click "Upload CSV File"
- Select your CSV file (SharePoint exports work best)
- Preview will show automatically

### Step 3: Configure Analysis

**Option A: Upload Configuration File**
- Click "Upload Configuration (JSON)"
- Select your custom configuration file

**Option B: Use Default Configuration**
- The app uses smart defaults if no config is uploaded
- Download templates to customize later

**Option C: For AI Analysis**
- Enter your OpenAI API key
- Configure AI settings in the JSON file

### Step 4: Run Analysis

- Click "Start Analysis"
- Wait for processing to complete
- View results in organized tabs

## 📊 Results Overview

### 📈 Summary Tab
- **Total Companies Found**: Count of unique companies
- **Total Entries**: Total mentions across all files
- **Detector Type**: NLP-enhanced or basic detection
- **AI Executive Summary**: Business insights (AI mode only)

### 🏢 Companies Tab
- **Company List**: All detected companies with counts
- **Interactive Chart**: Visual representation of top companies
- **Sortable Table**: Click columns to sort

### 📋 Details Tab
- **Technical Stats**: Processing details and performance
- **AI Analysis**: Industry classifications and risk assessments (AI mode)
- **Configuration Used**: Settings applied for the analysis

## ⚙️ Configuration Files

### Local Configuration (local_config.json)

```json
{
  "chunk_size": 5000,
  "filter_type": "all",
  "confidence_threshold": 0.3,
  "enable_enhanced_detection": true,
  "enable_caching": true,
  "log_level": "INFO",
  "output_formats": ["json", "csv", "txt"],
  "max_search_results": 10,
  "max_summary_companies": 50,
  "known_companies": [
    "Microsoft Corporation",
    "Apple Inc",
    "Google LLC"
  ],
  "csv_columns": {
    "name": "Name",
    "path": "Path",
    "modified_by": "Modified By",
    "item_type": "Item Type"
  }
}
```



## 🔧 Configuration Options

### Core Settings
- **chunk_size**: Number of rows to process at once (default: 5000)
- **filter_type**: What to analyze (`"all"`, `"folders"`, `"files"`)
- **confidence_threshold**: Minimum confidence for detection (0.0-1.0)

### Analysis Options
- **enable_enhanced_detection**: Use NLP models for better accuracy
- **enable_caching**: Cache results for faster repeat analysis
- **log_level**: Logging verbosity (`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`)

### AI Options (AI Mode)
- **enable_ai_analysis**: Enable AI-powered insights
- **openai_model**: GPT model to use (`"gpt-3.5-turbo"`, `"gpt-4"`)
- **openai_max_tokens**: Maximum tokens per API call
- **openai_temperature**: Creativity level (0.0-2.0)

### Output Settings
- **output_formats**: Result formats (`["json", "csv", "txt"]`)
- **max_search_results**: Maximum results to show
- **max_summary_companies**: Top companies to display

## 🎯 Use Cases

### 📁 SharePoint Document Analysis
- **Upload**: SharePoint export CSV files
- **Analyze**: Extract company names from folder/file structures
- **Results**: Clean list of business entities

### 🏢 Business Intelligence
- **Local Mode**: Quick company extraction for compliance
- **AI Mode**: AI-powered industry analysis and risk assessment
- **Reports**: Executive summaries and strategic recommendations

### 📊 Data Cleaning
- **Filter**: Remove technical files and system folders
- **Validate**: High-confidence company detection
- **Export**: Clean data in multiple formats

## 🛠️ Troubleshooting

### Common Issues

**"CSV file validation failed"**
- Ensure CSV file is properly formatted
- Check that required columns exist
- Try with a smaller sample file first

**"Enhanced detector failed to initialize"**
- Run: `python -m spacy download en_core_web_sm`
- Install NLTK data: `python -c "import nltk; nltk.download('punkt_tab')"`

**"OpenAI API key is required"**
- Get API key from: https://platform.openai.com/
- Enter in the "API Configuration" section
- Ensure you have sufficient credits

**"Analysis failed"**
- Check the configuration file format
- Verify CSV file structure
- Look at the error message for specific issues

### Performance Tips

**For Large Files:**
- Reduce `chunk_size` to 2000-3000
- Use `"folders"` filter_type for faster processing
- Enable caching for repeated analysis

**For Better Accuracy:**
- Use `enable_enhanced_detection: true`
- Adjust `confidence_threshold` (lower = more results)
- Add known companies to the configuration

## 📦 Sample Files

When you first run the application, sample configuration files are created in:
- `config_samples/local_config_sample.json`


Use these as templates for your custom configurations.

## 🆘 Support

**For help with:**
- **Setup Issues**: Check Python version (3.8+) and run `python run_ui.py`
- **Configuration**: Download and modify the sample templates
- **Analysis Problems**: Check CSV file format and column mappings
- **AI Features**: Verify OpenAI API key and model availability

## 🚀 Advanced Features

### CSV Column Mapping
Customize column names in your configuration:
```json
{
  "csv_columns": {
    "name": "Your_Name_Column",
    "path": "Your_Path_Column",
    "modified_by": "Your_Modified_By_Column",
    "item_type": "Your_Type_Column"
  }
}
```

### Custom Company Lists
Add known companies to improve detection:
```json
{
  "known_companies": [
    "Your Company Inc",
    "Partner Business LLC",
    "Client Corp"
  ]
}
```

### AI Batch Processing
Configure AI analysis batching:
```json
{
  "ai_max_companies_batch": 20,
  "openai_max_tokens": 2000,
  "openai_temperature": 0.3
}
```

---

**🎉 Ready to analyze your data!** Upload your CSV file and start extracting valuable business insights. 