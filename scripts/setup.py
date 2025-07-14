#!/usr/bin/env python3
"""
Setup script for Company Analyzer

This script sets up the environment for the company analyzer including:
- Installing required packages
- Downloading NLP models
- Validating the setup
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    # Go to project root directory
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / "requirements.txt"
    
    # Install packages from requirements.txt
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)])
        print("✓ All packages installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install packages from requirements.txt")
        
        # Try individual installation of core packages
        packages = [
            'pandas>=1.5.0',
            'numpy>=1.21.0', 
            'spacy>=3.4.0',
            'nltk>=3.8',
            'regex>=2022.7.9',
            'tqdm>=4.64.0',
            'openpyxl>=3.0.10',
            'xlrd>=2.0.1',
            'textblob>=0.17.1'
        ]
        
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")

def setup_nlp_models():
    """Setup NLP models"""
    print("\nSetting up NLP models...")
    
    # Install spaCy model
    print("Installing spaCy English model...")
    try:
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
        print("✓ spaCy model installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install spaCy model")
        print("You can install it manually with: python -m spacy download en_core_web_sm")

    # Download NLTK data
    print("Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        print("✓ NLTK data downloaded successfully")
    except Exception as e:
        print(f"✗ Failed to download NLTK data: {e}")

def check_file():
    """Check if LPATech.csv exists"""
    project_root = Path(__file__).parent.parent
    csv_file = project_root / "LPATech.csv"
    
    if csv_file.exists():
        print("✓ LPATech.csv found")
        
        # Get file size
        size = csv_file.stat().st_size
        size_mb = size / (1024 * 1024)
        print(f"  File size: {size_mb:.1f} MB")
        
        # Count lines
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            print(f"  Estimated rows: {lines-1:,} (excluding header)")
        except:
            print("  Could not count lines")
    else:
        print("⚠ LPATech.csv not found")
        print("  Please make sure the CSV file is in the project root directory")

def validate_setup():
    """Validate the setup"""
    print("\nValidating setup...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("⚠ Python 3.8 or higher is recommended")
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
    else:
        print("⚠ Not in a virtual environment. Consider creating one:")
        print("  python -m venv venv")
        print("  venv\\Scripts\\activate  (Windows)")
        print("  source venv/bin/activate  (Mac/Linux)")
    
    # Test imports
    try:
        import pandas
        print("✓ pandas available")
    except ImportError:
        print("✗ pandas not available")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✓ spaCy model available")
    except (ImportError, OSError):
        print("✗ spaCy model not available")
    
    try:
        import nltk
        print("✓ NLTK available")
    except ImportError:
        print("✗ NLTK not available")

def main():
    print("Company Analyzer Setup")
    print("=" * 50)
    
    # Validate setup
    validate_setup()
    
    print("\n" + "-"*50)
    
    # Check for CSV file
    check_file()
    
    print("\n" + "-"*50)
    
    # Install requirements
    install_requirements()
    
    # Setup NLP models
    setup_nlp_models()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print("To run the company analyzer:")
    print("1. Make sure your CSV file is in the project root")
    print("2. Run: python main.py [your_file.csv]")
    print("\nThe analyzer will:")
    print("- Process CSV files with enhanced NLP detection")
    print("- Extract company names from folder/file names")
    print("- Generate detailed results in multiple formats")
    print("- Provide interactive search capabilities")
    
    print("\nOutput files will be created with timestamps:")
    print("- companies_improved_YYYYMMDD_HHMMSS.json")
    print("- companies_detailed_improved_YYYYMMDD_HHMMSS.json")
    print("- companies_improved_YYYYMMDD_HHMMSS.csv")
    print("- companies_improved_YYYYMMDD_HHMMSS.txt")

if __name__ == "__main__":
    main() 