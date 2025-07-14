# 🚀 Simple Guide: MCP + AI Analysis

## 🤔 What is MCP? (Simple Explanation)

**MCP (Model Context Protocol)** is like a **bridge** that lets you:
1. Take your **offline company analysis results** (from main.py)
2. **Enhance them with AI** (ChatGPT/OpenAI) to get business insights
3. **Integrate with AI assistants** like ChatGPT, Claude, etc.

Think of it as: **Offline Analysis → MCP Server → AI Enhancement → Smart Business Insights**

## 🎯 What You Get

**Before (Offline Only):**
- List of companies: "Microsoft Corporation", "Apple Inc", "Google LLC"
- Basic counts and frequencies

**After (With MCP + AI):**
- **Industry Classification**: "Microsoft → Technology", "Apple → Consumer Electronics"
- **Risk Assessment**: "Low risk - established tech companies"
- **Business Relationships**: "Microsoft & OpenAI partnership detected"
- **Market Insights**: "AI sector growth opportunities"
- **Strategic Recommendations**: "Diversify beyond tech sector"
- **Executive Summary**: Professional business report

## 📋 Step-by-Step Tutorial

### Step 1: Run Your Offline Analysis First
```bash
# Run your normal analysis (you've already done this)
python main.py your_file.csv

# This creates: companies_YYYYMMDD_HHMMSS.csv, .json, .txt files
```

### Step 2: Setup Environment for AI
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your_actual_api_key_here
# ANALYZER_ENABLE_AI=true
# ANALYZER_ENABLE_MCP=true
```

### Step 2.5: Test Your Setup (Recommended)
```bash
# Run the validation script to check everything is working
python test_mcp_ai.py

# This will check:
# ✅ Environment file exists and has API key
# ✅ Dependencies are installed
# ✅ OpenAI connection works
# ✅ MCP server components are available
# ✅ AI analysis can initialize
```

### Step 3: Start the MCP Server
```bash
# Start the server (runs in background)
python -m src.mcp.run_mcp_server

# Server runs at: http://localhost:8005
# API docs at: http://localhost:8005/docs
```

### Step 4: Use MCP to Enhance Your Results

#### Option A: API Endpoints (Direct HTTP)
```bash
# 1. Submit your CSV for AI analysis
curl -X POST "http://localhost:8005/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_file_path": "your_file.csv",
    "enable_ai_analysis": true
  }'

# 2. Get AI insights for specific companies
curl -X POST "http://localhost:8005/ai/insights" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": ["Microsoft Corporation", "Apple Inc"],
    "analysis_type": "comprehensive"
  }'
```

#### Option B: Python Integration (Recommended)
```python
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer

# Initialize with your existing CSV
analyzer = AIEnhancedCompanyAnalyzer(
    csv_file_path="your_file.csv",
    enable_ai=True
)

# Run analysis (includes AI enhancement)
analyzer.analyze()

# Get AI insights
print("=== AI INSIGHTS ===")
analyzer.print_ai_summary()

# Save AI results
ai_files = analyzer.save_ai_results()
print(f"AI results saved to: {ai_files}")
```

### Step 5: Explore AI Features

```python
# Get specific insights
industry_data = analyzer.get_industry_insights()
risk_assessment = analyzer.get_risk_assessment()
market_insights = analyzer.get_market_insights()
recommendations = analyzer.get_recommendations()

# Interactive AI exploration
analyzer.run_interactive_ai_search()
```

## 🛠️ Common Workflows

### Workflow 1: Enhance Existing Analysis
```bash
# 1. You already have: companies_20240714_111010.csv
# 2. Enhance with AI:
python -c "
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
analyzer = AIEnhancedCompanyAnalyzer('companies_20240714_111010.csv', enable_ai=True)
analyzer.analyze()
analyzer.print_ai_summary()
analyzer.save_ai_results()
"

# Or use any CSV file you have:
python -c "
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
analyzer = AIEnhancedCompanyAnalyzer('LPATech.csv', enable_ai=True)
analyzer.analyze()
analyzer.print_ai_summary()
analyzer.save_ai_results()
"
```

### Workflow 2: Full Pipeline (Offline → AI)
```bash
# 1. Run offline analysis
python main.py your_data.csv

# 2. Enhance with AI
python -c "
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
import glob
latest_csv = max(glob.glob('companies_*.csv'))
analyzer = AIEnhancedCompanyAnalyzer(latest_csv, enable_ai=True)
analyzer.analyze()
analyzer.save_ai_results()
"
```

### Workflow 3: MCP Server Integration
```bash
# Terminal 1: Start MCP server
python -m src.mcp.run_mcp_server --verbose

# Terminal 2: Submit analysis job
curl -X POST "http://localhost:8005/analyze" \
  -H "Content-Type: application/json" \
  -d '{"csv_file_path": "your_file.csv", "enable_ai_analysis": true}'
```

## 📊 Expected Output Examples

### Industry Classification
```json
{
  "industries": {
    "Technology": ["Microsoft Corporation", "Apple Inc", "Google LLC"],
    "Healthcare": ["Johnson & Johnson", "Pfizer Inc"],
    "Finance": ["JPMorgan Chase", "Bank of America"]
  },
  "industry_summary": {
    "most_common": "Technology",
    "diversity_score": 0.7,
    "total_industries": 8
  }
}
```

### Risk Assessment
```json
{
  "risk_summary": {
    "overall_risk_level": "medium",
    "key_concerns": ["technology_concentration", "regulatory_compliance"]
  },
  "company_risks": {
    "Microsoft Corporation": {
      "risk_level": "low",
      "risk_factors": ["market_dependency"],
      "recommendations": ["diversify_product_lines"]
    }
  }
}
```

### Executive Summary
```
EXECUTIVE SUMMARY - Company Analysis Report

Dataset Overview:
- Total Companies Analyzed: 156
- Primary Industries: Technology (45%), Healthcare (20%), Finance (15%)
- Geographic Distribution: US (60%), International (40%)

Key Findings:
1. Technology Sector Dominance: Heavy concentration in tech companies
2. Market Leaders Present: Microsoft, Apple, Google represent 30% of dataset
3. Diversification Opportunities: Underrepresented in energy and manufacturing

Strategic Recommendations:
1. HIGH PRIORITY: Diversify beyond technology sector
2. MEDIUM PRIORITY: Increase international presence
3. LOW PRIORITY: Monitor regulatory compliance requirements

Risk Assessment: MEDIUM
- Concentration risk in technology sector
- Regulatory exposure in healthcare companies
- Currency exposure in international holdings
```

## 🚨 Troubleshooting

### Common Issues:

1. **"No OpenAI API key"**
   ```bash
   # Check your .env file
   cat .env | grep OPENAI_API_KEY
   # Should show: OPENAI_API_KEY=sk-...
   ```

2. **"MCP server won't start"**
   ```bash
   # Check dependencies
   python -m src.mcp.run_mcp_server --check-deps
   
   # Check configuration
   python -m src.mcp.run_mcp_server --validate-config
   ```

3. **"AI analysis fails"**
   ```bash
   # Test OpenAI connection
   python -c "
   import openai
   import os
   from dotenv import load_dotenv
   load_dotenv()
   client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
   print('OpenAI connection:', client.models.list().data[0].id)
   "
   ```

## 🎉 Success Indicators

You know it's working when you see:
- ✅ Server starts: "Server running at http://localhost:8005"
- ✅ AI analysis: "AI analysis completed for 156 companies"
- ✅ Files created: `companies_*_ai_analysis.json`, `companies_*_executive_summary.txt`
- ✅ Industry insights: JSON with industry classifications
- ✅ Risk assessment: Risk levels and recommendations

## 🔄 Next Steps

1. **Start Simple**: Run one AI analysis on your existing CSV
2. **Explore Features**: Try different analysis types (industry, risk, market)
3. **Integrate**: Use MCP server for AI assistant integration
4. **Automate**: Create scripts for regular analysis workflows

The key is: **Offline analysis gives you data, MCP+AI gives you insights!** 