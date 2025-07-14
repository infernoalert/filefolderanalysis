#!/usr/bin/env python3
"""
Launch script for the File Folder Analysis Tool UI

This script launches the Streamlit web interface for the file folder analysis tool.
It provides easy setup and launch commands for users.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_streamlit_installed():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
        return True
    except ImportError:
        print("❌ Streamlit not found")
        return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

def check_spacy_model():
    """Check if spaCy model is available"""
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model 'en_core_web_sm' available")
        except OSError:
            print("📦 Installing spaCy model...")
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], 
                          check=True)
            print("✅ spaCy model installed")
    except ImportError:
        print("⚠️  spaCy not available - enhanced detection may not work")

def setup_nltk():
    """Setup NLTK data"""
    try:
        import nltk
        print("📦 Setting up NLTK data...")
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        print("✅ NLTK data ready")
    except ImportError:
        print("⚠️  NLTK not available - enhanced detection may not work")

def create_sample_config():
    """Create sample configuration files"""
    # Create config directory if it doesn't exist
    config_dir = Path("config_samples")
    config_dir.mkdir(exist_ok=True)
    
    # Local configuration sample
    local_config = {
        "chunk_size": 5000,
        "filter_type": "all",
        "confidence_threshold": 0.3,
        "enable_enhanced_detection": True,
        "enable_caching": True,
        "log_level": "INFO",
        "output_formats": ["json", "csv", "txt"],
        "max_search_results": 10,
        "max_summary_companies": 50,
        "min_company_name_length": 2,
        "max_company_name_length": 50,
        "spacy_model": "en_core_web_sm",
        "known_companies": [
            "Microsoft Corporation",
            "Apple Inc",
            "Google LLC",
            "Amazon Web Services"
        ],
        "csv_columns": {
            "name": "Name",
            "path": "Path",
            "modified_by": "Modified By",
            "item_type": "Item Type",
            "file_size": "File Size",
            "modified": "Modified"
        }
    }
    
    # MCP configuration sample
    mcp_config = {
        "chunk_size": 5000,
        "filter_type": "all",
        "confidence_threshold": 0.3,
        "enable_enhanced_detection": True,
        "enable_ai_analysis": True,
        "enable_mcp_server": True,
        "openai_model": "gpt-3.5-turbo",
        "openai_max_tokens": 2000,
        "openai_temperature": 0.3,
        "ai_max_companies_batch": 20,
        "mcp_server_host": "0.0.0.0",
        "mcp_server_port": 8005,
        "mcp_enable_cors": True,
        "log_level": "INFO",
        "output_formats": ["json", "csv", "txt"],
        "max_search_results": 10,
        "max_summary_companies": 50,
        "known_companies": [
            "Microsoft Corporation",
            "Apple Inc",
            "Google LLC",
            "Amazon Web Services"
        ],
        "csv_columns": {
            "name": "Name",
            "path": "Path",
            "modified_by": "Modified By",
            "item_type": "Item Type",
            "file_size": "File Size",
            "modified": "Modified"
        }
    }
    
    # Save sample configurations
    import json
    with open(config_dir / "local_config_sample.json", "w") as f:
        json.dump(local_config, f, indent=2)
    
    with open(config_dir / "mcp_config_sample.json", "w") as f:
        json.dump(mcp_config, f, indent=2)
    
    print(f"✅ Sample configuration files created in {config_dir}/")

def launch_streamlit():
    """Launch the Streamlit application"""
    print("🚀 Launching File Folder Analysis Tool UI...")
    print("📱 The app will open in your default web browser")
    print("🔄 Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    """Main function"""
    print("🏢 File Folder Analysis Tool - UI Launcher")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check if app.py exists
    if not Path("app.py").exists():
        print("❌ app.py not found in current directory")
        sys.exit(1)
    
    # Check if Streamlit is installed
    if not check_streamlit_installed():
        print("📦 Installing dependencies...")
        install_requirements()
    
    # Setup NLP models
    check_spacy_model()
    setup_nltk()
    
    # Create sample configurations
    create_sample_config()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete! Ready to launch the UI")
    print("=" * 50)
    
    # Launch the application
    launch_streamlit()

if __name__ == "__main__":
    main() 