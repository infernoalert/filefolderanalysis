# 🤖 AI Analysis Configurations

This directory contains JSON configuration files for different types of AI-powered analysis. These configurations define how the AI should analyze manually selected terms/phrases to identify companies and provide business insights.

## 📁 Available Configurations

### 1. `company_extraction.json`
**Purpose**: Extract and validate company names from manually selected terms/phrases

**Features**:
- Identifies which terms are actual company names
- Provides confidence scores for each identification
- Classifies companies by type (corporation, LLC, etc.)
- Assigns industry classifications
- Provides reasoning for each decision

**Best for**: When you have a list of terms and want to know which ones are real companies

### 2. `industry_classification.json`
**Purpose**: Classify companies by industry and provide detailed industry analysis

**Features**:
- Primary and secondary industry classification
- Market position analysis (leader, challenger, niche)
- Industry descriptions and insights
- Confidence scores for classifications

**Best for**: When you have confirmed company names and want industry insights

### 3. `business_intelligence.json`
**Purpose**: Comprehensive business analysis including risk assessment and strategic recommendations

**Features**:
- Risk assessment (regulatory, market, operational)
- Market insights and trends
- Strategic recommendations
- Competitive analysis
- Growth potential evaluation

**Best for**: When you need comprehensive business intelligence for decision-making

## 🎯 How to Use

### 1. In the Web UI
1. Select "Manual AI Analysis" from the analysis mode dropdown
2. Enter your OpenAI API key
3. Choose an analysis configuration from the dropdown
4. Provide terms to analyze using one of the input methods:
   - **Text Input**: Type terms one per line
   - **File Upload**: Upload a text or CSV file
   - **CSV Column Selection**: Upload CSV and select a column
5. Click "Start Analysis"

### 2. Creating Custom Configurations
You can create your own analysis configurations by adding JSON files to this directory. Each configuration should include:

```json
{
  "analysis_type": "your_analysis_type",
  "name": "Your Analysis Name",
  "description": "Description of what this analysis does",
  "openai_model": "gpt-3.5-turbo",
  "max_tokens": 2000,
  "temperature": 0.3,
  "instructions": {
    "task": "What the AI should do",
    "output_format": "json",
    "required_fields": ["field1", "field2"]
  },
  "prompt_template": "Your prompt template with {terms} placeholder",
  "validation_rules": {
    "min_confidence": 0.7,
    "required_fields": ["field1", "field2"]
  },
  "output_processing": {
    "filter_by_confidence": true,
    "min_confidence_threshold": 0.7
  }
}
```

## 🔧 Configuration Parameters

### Core Parameters
- **analysis_type**: Unique identifier for the analysis type
- **name**: Human-readable name for the configuration
- **description**: Detailed description of what the analysis does
- **openai_model**: GPT model to use (gpt-3.5-turbo, gpt-4, etc.)
- **max_tokens**: Maximum tokens for AI response
- **temperature**: Creativity level (0.0-2.0, lower = more focused)

### Instructions Section
- **task**: Clear description of what the AI should accomplish
- **output_format**: Expected response format (usually "json")
- **required_fields**: Fields that must be present in AI response

### Prompt Template
- Use `{terms}` placeholder where the terms should be inserted
- Provide clear instructions for the AI
- Specify the expected JSON structure

### Validation Rules
- **min_confidence**: Minimum confidence score for valid results
- **required_fields**: Fields that must be present in each result
- **company_indicators**: Keywords that suggest a term is a company

### Output Processing
- **filter_by_confidence**: Whether to filter results by confidence
- **min_confidence_threshold**: Minimum confidence for inclusion
- **include_reasoning**: Whether to include AI reasoning in results

## 📊 Example Usage

### Company Extraction
Input terms: `["Microsoft Corp", "T&C", "Apple Inc", "v2.1.3"]`

Expected output:
```json
[
  {
    "company_name": "Microsoft Corp",
    "is_company": true,
    "confidence_score": 0.95,
    "company_type": "corporation",
    "industry": "Technology",
    "reasoning": "Known technology company with corporate suffix"
  },
  {
    "company_name": "T&C",
    "is_company": false,
    "confidence_score": 0.1,
    "company_type": "abbreviation",
    "industry": "N/A",
    "reasoning": "Common abbreviation for Terms and Conditions"
  }
]
```

## 🚀 Tips for Best Results

1. **Use specific configurations**: Choose the configuration that matches your analysis needs
2. **Provide context**: Include relevant terms that might help the AI understand your domain
3. **Review results**: Always review AI results for accuracy
4. **Adjust confidence thresholds**: Lower thresholds for exploratory analysis, higher for production use
5. **Export results**: Use the export features to save results for further analysis

## 🔍 Troubleshooting

### Common Issues
- **No configurations found**: Ensure JSON files are in the `ai_analysis_configs/` directory
- **API key errors**: Verify your OpenAI API key is valid and has sufficient credits
- **Poor results**: Try adjusting the temperature or using a different model
- **Timeout errors**: Reduce the number of terms or use a faster model

### Getting Help
- Check the main UI README for general troubleshooting
- Verify your OpenAI API key at https://platform.openai.com/
- Review the configuration JSON files for syntax errors 