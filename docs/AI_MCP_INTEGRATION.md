# AI and MCP Integration Guide

This guide explains how to use the new AI-enhanced analysis and Model Context Protocol (MCP) server features.

## 🚀 Overview

The enhanced company analyzer now includes:
- **🤖 AI Analysis** - OpenAI ChatGPT integration for business insights
- **🔗 MCP Server** - Model Context Protocol server for AI assistant integration
- **📊 Advanced Analytics** - Industry classification, risk assessment, market insights
- **💼 Executive Summaries** - AI-generated business reports

## 🛠️ Setup and Installation

### 1. Install Dependencies

```bash
# Install new dependencies
pip install -r requirements.txt

# Required for AI features
pip install openai>=1.3.0 fastapi>=0.104.0 uvicorn>=0.24.0

# Download spaCy model if not already installed
python -m spacy download en_core_web_sm
```

### 2. Configure API Keys

Create a `.env` file:

```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

Required environment variables:
```bash
# OpenAI API key (required for AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Enable AI analysis
ANALYZER_ENABLE_AI=true

# Enable MCP server
ANALYZER_ENABLE_MCP=true
```

### 3. Verify Setup

```bash
# Check dependencies
python run_mcp_server.py --check-deps

# Validate configuration
python run_mcp_server.py --validate-config
```

## 🤖 AI-Enhanced Analysis

### Basic Usage

```python
from company_analyzer_ai import AIEnhancedCompanyAnalyzer

# Initialize with AI enabled
analyzer = AIEnhancedCompanyAnalyzer(
    csv_file_path="your_data.csv",
    enable_ai=True
)

# Run analysis (includes AI analysis automatically)
success = analyzer.analyze()

if success:
    # Print AI insights
    analyzer.print_ai_summary()
    
    # Get specific insights
    industry_insights = analyzer.get_industry_insights()
    risk_assessment = analyzer.get_risk_assessment()
    recommendations = analyzer.get_recommendations()
    
    # Save AI results
    ai_files = analyzer.save_ai_results()
    print(f"AI results saved to: {ai_files}")
```

### AI Analysis Features

#### 1. **Industry Classification**
```python
industry_data = analyzer.get_industry_insights()

# Example output:
{
    "industries": {
        "Technology": ["Microsoft Corporation", "Apple Inc"],
        "Healthcare": ["Johnson & Johnson"],
        "Finance": ["JPMorgan Chase"]
    },
    "industry_summary": {
        "most_common": "Technology",
        "diversity_score": 0.8,
        "total_industries": 5
    }
}
```

#### 2. **Risk Assessment**
```python
risk_data = analyzer.get_risk_assessment()

# Example output:
{
    "risk_summary": {
        "overall_risk_level": "medium",
        "key_concerns": ["data_concentration", "regulatory_compliance"]
    },
    "company_risks": {
        "Microsoft Corporation": {
            "risk_level": "low",
            "risk_factors": ["market_dependency"],
            "recommendations": ["diversify_suppliers"]
        }
    }
}
```

#### 3. **Business Relationships**
```python
relationships = analyzer.get_business_relationships()

# Example output:
{
    "partnerships": [
        {"companies": ["Microsoft", "OpenAI"], "type": "strategic_alliance", "likelihood": 0.9}
    ],
    "competitors": [
        {"companies": ["Apple", "Google"], "market": "consumer_tech", "intensity": "high"}
    ]
}
```

#### 4. **Market Insights**
```python
market_data = analyzer.get_market_insights()

# Example output:
{
    "market_trends": [
        {"trend": "AI adoption", "impact": "positive", "companies": ["tech_companies"]}
    ],
    "growth_opportunities": [
        {"opportunity": "cloud migration", "potential": "high", "timeframe": "2024-2025"}
    ]
}
```

#### 5. **Strategic Recommendations**
```python
recommendations = analyzer.get_recommendations()

# Example output:
{
    "strategic_recommendations": [
        {
            "category": "data_management",
            "recommendation": "Implement data governance framework",
            "priority": "high",
            "rationale": "Large volume of unstructured company data"
        }
    ],
    "immediate_actions": [
        {"action": "data_audit", "timeline": "30_days", "impact": "high"}
    ]
}
```

### Interactive AI Analysis

```python
# Run interactive session with AI commands
analyzer.run_interactive_ai_search()

# Available commands:
# - 'ai summary' - Show AI analysis summary
# - 'ai industry' - Show industry classification
# - 'ai risk' - Show risk assessment
# - 'ai market' - Show market insights
# - 'ai recommendations' - Show strategic recommendations
# - 'ai executive' - Show executive summary
```

## 🔗 MCP Server Integration

### Starting the MCP Server

```bash
# Basic startup
python run_mcp_server.py

# Custom configuration
python run_mcp_server.py --host localhost --port 8080 --verbose

# With configuration file
python run_mcp_server.py --config production_config.yaml
```

### MCP Server Endpoints

#### Core Endpoints

- **Health Check**: `GET /health`
- **Server Info**: `GET /`
- **API Documentation**: `GET /docs` (Swagger UI)

#### Analysis Endpoints

```bash
# Start analysis
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_file_path": "data.csv",
    "enable_ai_analysis": true,
    "filter_type": "all"
  }'

# Get analysis results
curl "http://localhost:8000/analysis/{analysis_id}"

# List all analyses
curl "http://localhost:8000/analyses"
```

#### Search and AI Endpoints

```bash
# Search companies
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "microsoft", "max_results": 10}'

# Get AI insights for specific companies
curl -X POST "http://localhost:8000/ai/insights" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": ["Microsoft Corporation", "Apple Inc"],
    "analysis_type": "comprehensive"
  }'

# Get AI statistics
curl "http://localhost:8000/ai/stats"
```

### MCP Tools for AI Assistants

The server exposes these tools for MCP-compatible AI assistants:

#### 1. `analyze_companies`
```json
{
  "name": "analyze_companies",
  "description": "Analyze CSV file to extract and classify company names with AI insights",
  "inputSchema": {
    "type": "object",
    "properties": {
      "csv_file_path": {"type": "string"},
      "filter_type": {"enum": ["all", "folders", "files"]},
      "enable_ai_analysis": {"type": "boolean"}
    }
  }
}
```

#### 2. `search_companies`
```json
{
  "name": "search_companies", 
  "description": "Search for companies across analysis results",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "max_results": {"type": "integer"}
    }
  }
}
```

#### 3. `get_ai_insights`
```json
{
  "name": "get_ai_insights",
  "description": "Get AI-powered business insights for specific companies",
  "inputSchema": {
    "type": "object", 
    "properties": {
      "companies": {"type": "array", "items": {"type": "string"}},
      "analysis_type": {"enum": ["comprehensive", "industry", "risk", "market"]}
    }
  }
}
```

## 📊 Example Workflows

### 1. Complete AI Analysis Workflow

```python
# 1. Initialize AI-enhanced analyzer
analyzer = AIEnhancedCompanyAnalyzer("data.csv", enable_ai=True)

# 2. Run complete analysis
analyzer.analyze()

# 3. Print comprehensive summary
analyzer.print_summary()  # Basic analysis
analyzer.print_ai_summary()  # AI insights

# 4. Save all results
basic_files = analyzer.save_results()
ai_files = analyzer.save_ai_results()

# 5. Export for MCP
mcp_data = analyzer.export_for_mcp_ai()
```

### 2. MCP Server Integration Workflow

```bash
# 1. Start MCP server
python run_mcp_server.py --verbose

# 2. Submit analysis job
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"csv_file_path": "data.csv", "enable_ai_analysis": true}'

# 3. Monitor progress
curl "http://localhost:8000/analysis/analysis_1_20241201_120000"

# 4. Get AI insights for top companies
curl -X POST "http://localhost:8000/ai/insights" \
  -H "Content-Type: application/json" \
  -d '{"companies": ["Microsoft Corporation", "Apple Inc"]}'
```

### 3. Custom AI Analysis

```python
from ai_analyzer import AICompanyAnalyzer
from collections import Counter

# Direct AI analysis without CSV processing
ai_analyzer = AICompanyAnalyzer()

# Create company data
companies = Counter({
    "Microsoft Corporation": 45,
    "Apple Inc": 32,
    "Google LLC": 28
})

# Run AI analysis
ai_results = await ai_analyzer.analyze_companies(companies, {})

# Generate executive summary
summary = await ai_analyzer.generate_executive_summary(companies, ai_results)
print(summary)
```

## ⚙️ Configuration Options

### AI Configuration

```bash
# AI Analysis Settings
ANALYZER_ENABLE_AI=true
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3
AI_MAX_COMPANIES_BATCH=20
```

### MCP Server Configuration

```bash
# MCP Server Settings
ANALYZER_ENABLE_MCP=true
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_ENABLE_CORS=true
```

### Performance Tuning

```bash
# Performance Settings
ANALYZER_ENABLE_CACHING=true
ANALYZER_MAX_WORKERS=4
ANALYZER_CACHE_SIZE=1000
ANALYZER_ENABLE_PARALLEL=false  # Experimental
```

## 🔒 Security Considerations

### API Key Security
- Store OpenAI API keys in environment variables
- Never commit API keys to version control
- Use `.env` files for local development
- Consider using key management services in production

### MCP Server Security
- Configure CORS appropriately for your environment
- Use authentication/authorization in production
- Consider running behind a reverse proxy
- Monitor API usage and set rate limits

### Data Privacy
- AI analysis sends company names to OpenAI
- Review OpenAI's data usage policies
- Consider data retention and deletion policies
- Implement audit logging for compliance

## 🚨 Troubleshooting

### Common Issues

#### 1. OpenAI API Errors
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### 2. MCP Server Won't Start
```bash
# Check dependencies
python run_mcp_server.py --check-deps

# Check configuration
python run_mcp_server.py --validate-config

# Check port availability
netstat -an | grep 8000
```

#### 3. AI Analysis Fails
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check AI analyzer initialization
analyzer = AIEnhancedCompanyAnalyzer(enable_ai=True)
print(analyzer.get_ai_analysis_stats())
```

### Performance Issues

#### Large Files
- Increase chunk size: `ANALYZER_CHUNK_SIZE=10000`
- Reduce AI batch size: `AI_MAX_COMPANIES_BATCH=10`
- Enable caching: `ANALYZER_ENABLE_CACHING=true`

#### Slow AI Analysis
- Use faster model: `OPENAI_MODEL=gpt-3.5-turbo`
- Reduce max tokens: `OPENAI_MAX_TOKENS=1000`
- Cache results to avoid re-analysis

## 📈 Benefits and Use Cases

### Business Benefits
- **🎯 Better Decision Making** - AI-powered insights for strategic decisions
- **⚡ Faster Analysis** - Automated industry classification and risk assessment
- **🔍 Deep Insights** - Understand business relationships and market trends
- **📊 Executive Reporting** - Professional summaries for leadership

### Use Cases
- **Due Diligence** - Risk assessment for M&A transactions
- **Portfolio Analysis** - Understand industry exposure and concentration
- **Competitive Intelligence** - Identify market relationships and trends
- **Compliance** - Industry-specific risk and regulatory analysis
- **Strategic Planning** - Data-driven recommendations for growth

### Integration Scenarios
- **AI Assistants** - Direct integration with ChatGPT, Claude, etc.
- **Business Intelligence** - Feed insights into BI dashboards
- **Workflow Automation** - Trigger actions based on analysis results
- **Reporting Systems** - Automated generation of business reports

---

## 🎉 Next Steps

1. **Install Dependencies** - Set up OpenAI API and install packages
2. **Configure Environment** - Set up `.env` file with your settings  
3. **Run First Analysis** - Test with a small CSV file
4. **Start MCP Server** - Enable AI assistant integration
5. **Explore AI Features** - Try different analysis types and insights

For more advanced usage and customization, see the individual module documentation in the codebase. 