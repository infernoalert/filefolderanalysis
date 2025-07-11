import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    # Install packages from requirements.txt
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ All packages installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install packages from requirements.txt")
        
        # Try individual installation
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
    
    # Install spaCy model
    print("\nInstalling spaCy English model...")
    try:
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
        print("✓ spaCy model installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install spaCy model")
        print("You can install it manually with: python -m spacy download en_core_web_sm")

def check_file():
    """Check if LPATech.csv exists"""
    if os.path.exists('LPATech.csv'):
        print("✓ LPATech.csv found")
        
        # Get file size
        size = os.path.getsize('LPATech.csv')
        size_mb = size / (1024 * 1024)
        print(f"  File size: {size_mb:.1f} MB")
        
        # Count lines
        try:
            with open('LPATech.csv', 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            print(f"  Estimated rows: {lines-1:,} (excluding header)")
        except:
            print("  Could not count lines")
    else:
        print("⚠ LPATech.csv not found")
        print("  Please make sure the CSV file is in the same directory as this script")

def main():
    print("SharePoint Company Analyzer Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("⚠ Python 3.7 or higher is recommended")
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
    
    print("\n" + "-"*50)
    
    # Check for CSV file
    check_file()
    
    print("\n" + "-"*50)
    
    # Install requirements
    install_requirements()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print("To run the company analyzer:")
    print("1. Make sure LPATech.csv is in this directory")
    print("2. Run: python sharepoint_company_analyzer.py")
    print("\nThe analyzer will:")
    print("- Process ~120,000 rows from LPATech.csv")
    print("- Extract company names from folder names")
    print("- Generate detailed results in multiple formats")
    print("- Provide interactive search capabilities")
    
    print("\nOutput files will be created with timestamps:")
    print("- companies_YYYYMMDD_HHMMSS.json")
    print("- companies_detailed_YYYYMMDD_HHMMSS.json")
    print("- companies_YYYYMMDD_HHMMSS.csv")
    print("- companies_YYYYMMDD_HHMMSS.txt")

if __name__ == "__main__":
    main() 