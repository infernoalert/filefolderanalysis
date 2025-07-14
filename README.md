# Company Analyzer

A powerful, AI-enhanced Python solution for extracting company names from CSV files with offline NLP capabilities and MCP server integration. **Now with a beautiful web UI!**

## 🚀 Quick Start

### 🖥️ **Web UI (Recommended - No Command Line Required!)**

```bash
# One-command launch (handles all setup automatically)
python run_ui.py

# Or manually:
pip install -r requirements.txt
streamlit run app.py
```

**Then open:** `http://localhost:8501` in your browser

**Features:**
- 🎯 **Drag & drop CSV files** - No file paths needed
- ⚙️ **Upload JSON configurations** - Easy setup
- 📊 **Interactive results** - Charts and tables
- 🤖 **AI insights** - Business intelligence mode
- 📱 **Mobile-friendly** - Works on any device

**📖 Full UI Guide:** [UI_README.md](UI_README.md)

### 💻 **Command Line Interface (Advanced Users)**

```bash
# Clone the repository
git clone https://github.com/your-username/company-analyzer.git
cd company-analyzer

# Install dependencies
pip install -r requirements.txt

# Setup NLP models
python scripts/setup.py

# Basic analysis
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
├── app.py                         # 🌟 Streamlit Web UI
├── run_ui.py                      # 🚀 UI launcher script
├── demo_usage.py                  # 📖 Demo and usage examples
├── UI_README.md                   # 📱 UI documentation
├── main.py                        # Main CLI entry point
├── requirements.txt               # Python dependencies
└── setup.py                       # Package setup
```

## ✨ Features

### 🌟 **Web UI Features (New!)**
- **🎯 Drag & Drop Interface**: Upload CSV files and configurations easily
- **🔄 Two Analysis Modes**: Local (offline) and MCP (AI-enhanced) options
- **📊 Interactive Results**: Charts, tables, and visual data exploration
- **⚙️ Configuration Management**: Upload/download JSON configuration files
- **🚀 One-Click Launch**: Automatic setup with `run_ui.py`
- **📱 Mobile Responsive**: Works on desktop, tablet, and mobile devices
- **🔍 Real-time Preview**: See CSV data before analysis
- **💾 Template Downloads**: Get configuration templates instantly

### 🔍 **Core Analysis Features**
- **🧠 Enhanced NLP Detection**: Uses spaCy and NLTK for intelligent company identification
- **🎯 Superior Accuracy**: Filters out version numbers and technical references
- **🏗️ Modular Architecture**: Clean separation of concerns
- **⚡ Memory Efficient**: Processes large files in chunks
- **🔍 Intelligent Filtering**: Advanced pattern matching
- **📊 Multiple Output Formats**: JSON, CSV, and TXT results
- **🔎 Interactive Search**: Built-in search capabilities
- **💻 Offline Operation**: No API calls required

### 🤖 **AI Enhancement Features**
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

### 🌟 **Getting Started (Choose Your Path)**
- **[UI README](UI_README.md)** - ⭐ **START HERE** for web interface usage
- **[Demo Usage](demo_usage.py)** - Interactive examples and sample files
- **[Simple MCP Guide](docs/MCP_SIMPLE_GUIDE.md)** - MCP/AI usage guide
- **[Main README](README.md)** - This file, overview and CLI usage

### 🔧 **Configuration & Setup**
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed configuration options
- **[AI/MCP Integration](docs/AI_MCP_INTEGRATION.md)** - Technical AI integration guide

### 📊 **Reference Documentation**
- **[API Reference](docs/README.md)** - Complete API documentation
- **[MCP AI Summary](docs/MCP_AI_SUMMARY.md)** - Feature overview and examples

### 🚀 **Quick Links**
- **New user?** → [UI README](UI_README.md) (Web interface)
- **Need examples?** → Run `python demo_usage.py`
- **Want MCP/AI?** → [Simple MCP Guide](docs/MCP_SIMPLE_GUIDE.md)
- **CLI user?** → [Configuration Guide](docs/CONFIGURATION.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### 🌟 **Getting Help**

**For Web UI Issues:**
- Check [UI README](UI_README.md) for troubleshooting
- Run `python demo_usage.py` for examples
- Ensure Python 3.8+ is installed

**For General Support:**
- Create an issue on GitHub
- Check the documentation in `docs/`
- Review examples and demos

**Common Solutions:**
- **UI won't start**: Run `python run_ui.py` (handles setup automatically)
- **Enhanced detector failed**: Install spaCy model: `python -m spacy download en_core_web_sm`
- **AI features not working**: Check OpenAI API key and configuration
- **CSV validation failed**: Verify file format and column names

### 🚀 **Quick Start Options**
- **Easiest**: `python run_ui.py` → Open `http://localhost:8501`
- **CLI**: `python main.py your_file.csv`
- **Demo**: `python demo_usage.py` → Get sample files and examples

---

## 🎉 **Ready to Analyze Your Data!**

The **Web UI** is the recommended way to use this tool - it's user-friendly, requires no command-line experience, and provides beautiful visualizations of your results.

**Just run:** `python run_ui.py` **and start analyzing!** 🚀

Perfect for:
- 📁 **SharePoint exports** - Clean company data from document libraries
- 🏢 **Business intelligence** - AI-powered industry analysis and insights
- 📊 **Data cleaning** - Remove technical artifacts and extract real companies
- 🤖 **AI analysis** - Get executive summaries and strategic recommendations 