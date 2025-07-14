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

### Basic Usage

```bash
# Analyze a CSV file
python main.py your_file.csv

# Quick preview mode
python main.py your_file.csv --quick-preview

# Interactive mode
python main.py your_file.csv --interactive
```

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

- **🧠 Enhanced NLP Detection**: Uses spaCy and NLTK for intelligent company identification
- **🎯 Superior Accuracy**: Filters out version numbers and technical references
- **🏗️ Modular Architecture**: Clean separation of concerns
- **⚡ Memory Efficient**: Processes large files in chunks
- **🔍 Intelligent Filtering**: Advanced pattern matching
- **📊 Multiple Output Formats**: JSON, CSV, and TXT results
- **🔎 Interactive Search**: Built-in search capabilities
- **🔧 Configurable**: Easy-to-modify configuration
- **🚀 MCP-Ready**: Model Context Protocol integration
- **💻 Offline Operation**: No API calls required

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

See the `docs/` directory for comprehensive documentation:

- [Configuration Guide](docs/CONFIGURATION.md)
- [AI/MCP Integration](docs/AI_MCP_INTEGRATION.md)
- [API Reference](docs/README.md)

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