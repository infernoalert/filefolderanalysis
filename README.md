# Company Analyzer

A powerful, AI-enhanced Python solution for extracting company names from CSV files with offline NLP capabilities and MCP server integration.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/company-analyzer.git
cd company-analyzer

# Install dependencies
pip install -r requirements.txt

# Setup NLP models
python scripts/setup.py
```

### Basic Usage (Offline Analysis)

```bash
# Analyze a CSV file
python main.py your_file.csv

# Quick preview mode
python main.py your_file.csv --quick-preview

# Interactive mode
python main.py your_file.csv --interactive
```

### 🤖 AI-Enhanced Analysis (New!)

Want to turn your basic company list into smart business insights? Use MCP + AI:

```bash
# 1. Setup AI (one-time)
cp .env.example .env
# Edit .env and add your OpenAI API key

# 2. Run AI-enhanced analysis
python -c "
from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
analyzer = AIEnhancedCompanyAnalyzer('your_file.csv', enable_ai=True)
analyzer.analyze()
analyzer.print_ai_summary()
analyzer.save_ai_results()
"

# 3. Or start MCP server for AI integration
python -m src.mcp.run_mcp_server
```

**What you get with AI:**
- 🏭 Industry classifications
- ⚠️ Risk assessments  
- 📈 Market insights
- 💡 Strategic recommendations
- 📋 Executive summaries

**📖 New to MCP/AI? Read:** [Simple MCP Guide](docs/MCP_SIMPLE_GUIDE.md)

## 📁 Project Structure

```
company-analyzer/
├── src/                           # Source code
│   ├── core/                      # Core analysis modules
│   │   ├── company_analyzer.py    # Main analyzer orchestrator
│   │   ├── company_detector.py    # Basic company detection
│   │   ├── enhanced_company_detector.py  # NLP-enhanced detection
│   │   ├── csv_processor.py       # CSV file processing
│   │   └── results_manager.py     # Results formatting and export
│   ├── ai/                        # AI integration modules
│   │   ├── ai_analyzer.py         # AI-powered analysis
│   │   ├── company_analyzer_ai.py # AI-enhanced analyzer
│   │   └── example_ai_usage.py    # Usage examples
│   ├── mcp/                       # MCP server integration
│   │   ├── mcp_server.py          # MCP server implementation
│   │   └── run_mcp_server.py      # Server runner
│   ├── config/                    # Configuration management
│   │   ├── config.py              # Main configuration
│   │   ├── config_example.json    # JSON config template
│   │   └── config_example.yaml    # YAML config template
│   └── utils/                     # Utility functions
├── tests/                         # Test files
├── docs/                          # Documentation
│   ├── README.md                  # Detailed documentation
│   ├── CONFIGURATION.md           # Configuration guide
│   ├── AI_MCP_INTEGRATION.md      # AI/MCP integration guide
│   └── MCP_AI_SUMMARY.md          # MCP AI summary
├── examples/                      # Usage examples
├── scripts/                       # Utility scripts
│   └── setup.py                   # Setup script
├── main.py                        # Main entry point
├── requirements.txt               # Python dependencies
└── setup.py                       # Package setup
```

## ✨ Features

### 🔍 Core Analysis Features
- **🧠 Enhanced NLP Detection**: Uses spaCy and NLTK for intelligent company identification
- **🎯 Superior Accuracy**: Filters out version numbers and technical references
- **🏗️ Modular Architecture**: Clean separation of concerns
- **⚡ Memory Efficient**: Processes large files in chunks
- **🔍 Intelligent Filtering**: Advanced pattern matching
- **📊 Multiple Output Formats**: JSON, CSV, and TXT results
- **🔎 Interactive Search**: Built-in search capabilities
- **💻 Offline Operation**: No API calls required

### 🤖 AI Enhancement Features (New!)
- **🏭 Industry Classification**: Automatically categorize companies by industry
- **⚠️ Risk Assessment**: AI-powered business risk analysis
- **🤝 Business Relationships**: Detect partnerships and competitors
- **📈 Market Insights**: Growth opportunities and trend analysis
- **💡 Strategic Recommendations**: Actionable business advice
- **📋 Executive Summaries**: Professional business reports
- **🔗 MCP Server**: Model Context Protocol for AI assistant integration
- **🚀 RESTful API**: Complete API with background processing

## 🛠️ Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_company_analyzer.py
```

### Code Style

```bash
# Format code
black src/
isort src/

# Run linting
flake8 src/
mypy src/
```

## 📚 Documentation

### 📖 Getting Started
- **[Simple MCP Guide](docs/MCP_SIMPLE_GUIDE.md)** - ⭐ **START HERE** for MCP/AI usage
- **[Main README](README.md)** - This file, basic usage

### 🔧 Configuration & Setup
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed configuration options
- **[AI/MCP Integration](docs/AI_MCP_INTEGRATION.md)** - Technical AI integration guide

### 📊 Reference Documentation
- **[API Reference](docs/README.md)** - Complete API documentation
- **[MCP AI Summary](docs/MCP_AI_SUMMARY.md)** - Feature overview and examples

### 🚀 Quick Links
- **New to MCP?** → [Simple MCP Guide](docs/MCP_SIMPLE_GUIDE.md)
- **Need AI setup?** → [AI Integration Guide](docs/AI_MCP_INTEGRATION.md)
- **Want examples?** → [MCP AI Summary](docs/MCP_AI_SUMMARY.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- Create an issue on GitHub
- Check the documentation in `docs/`
- Review examples in `examples/` 