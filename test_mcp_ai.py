#!/usr/bin/env python3
"""
Quick Test Script for MCP + AI Setup

This script helps you validate your MCP and AI setup step by step.
Run this before using the full MCP/AI features.
"""

import os
import sys
from pathlib import Path
import glob

def print_step(step_num, description):
    print(f"\n{'='*50}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*50}")

def check_environment():
    """Check if .env file exists and has required variables"""
    print_step(1, "Checking Environment Setup")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your OpenAI API key")
        return False
    
    print("✅ .env file found")
    
    # Check for OpenAI API key
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=your_openai_api_key_here' in content:
            print("❌ OpenAI API key not configured")
            print("   Edit .env and replace 'your_openai_api_key_here' with your actual API key")
            return False
        elif 'OPENAI_API_KEY=' in content:
            print("✅ OpenAI API key configured")
            return True
    
    print("❌ OPENAI_API_KEY not found in .env")
    return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print_step(2, "Checking Dependencies")
    
    required_packages = [
        ('openai', 'OpenAI API client'),
        ('fastapi', 'FastAPI for MCP server'),
        ('uvicorn', 'ASGI server for FastAPI'),
        ('dotenv', 'Environment variable loading'),  # Import name is 'dotenv' not 'python-dotenv'
    ]
    
    missing = []
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} ({description})")
        except ImportError:
            print(f"❌ {package} ({description})")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_openai_connection():
    """Test OpenAI API connection"""
    print_step(3, "Testing OpenAI Connection")
    
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No OpenAI API key found")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        models = client.models.list()
        print(f"✅ OpenAI connection successful")
        print(f"   Available models: {len(models.data)} models")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def check_mcp_server():
    """Test MCP server startup"""
    print_step(4, "Testing MCP Server")
    
    try:
        # Import MCP components
        from src.mcp.run_mcp_server import check_dependencies
        from src.config import AnalyzerConfig
        
        # Test dependency check
        if not check_dependencies():
            print("❌ MCP server dependencies not met")
            return False
            
        print("✅ MCP server components available")
        return True
        
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        return False

def find_csv_files():
    """Find available CSV files for testing"""
    print_step(5, "Finding CSV Files for Testing")
    
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("❌ No CSV files found in current directory")
        print("   Need a CSV file to test analysis")
        return None
    
    print(f"✅ Found {len(csv_files)} CSV files:")
    for i, file in enumerate(csv_files, 1):
        size = os.path.getsize(file) / 1024 / 1024  # MB
        print(f"   {i}. {file} ({size:.1f} MB)")
    
    return csv_files[0]  # Return first file for testing

def test_ai_analysis(csv_file):
    """Test AI analysis on a CSV file"""
    print_step(6, f"Testing AI Analysis on {csv_file}")
    
    try:
        from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer
        
        print(f"   Initializing analyzer with {csv_file}...")
        analyzer = AIEnhancedCompanyAnalyzer(csv_file, enable_ai=True)
        
        print("   Testing AI analyzer initialization...")
        if analyzer.ai_analyzer is None:
            print("❌ AI analyzer not initialized")
            return False
        
        print("✅ AI analyzer initialized successfully")
        print("   Ready for full analysis!")
        return True
        
    except Exception as e:
        print(f"❌ AI analysis test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 MCP + AI Setup Validation")
    print("This script will check if your MCP and AI setup is ready to use.")
    
    # Run all checks
    checks = [
        check_environment(),
        check_dependencies(),
        check_openai_connection(),
        check_mcp_server(),
    ]
    
    if all(checks):
        print("\n🎉 All basic checks passed!")
        
        # Test with actual CSV file
        csv_file = find_csv_files()
        if csv_file:
            if test_ai_analysis(csv_file):
                print("\n✅ SETUP COMPLETE!")
                print("Your MCP + AI setup is ready to use.")
                print("\nNext steps:")
                print("1. Run AI analysis:")
                print(f"   python -c \"from src.ai.company_analyzer_ai import AIEnhancedCompanyAnalyzer; analyzer = AIEnhancedCompanyAnalyzer('{csv_file}', enable_ai=True); analyzer.analyze(); analyzer.print_ai_summary()\"")
                print("2. Start MCP server:")
                print("   python -m src.mcp.run_mcp_server")
                print("3. Read the guide: docs/MCP_SIMPLE_GUIDE.md")
            else:
                print("\n⚠️ Basic setup OK, but AI analysis test failed")
        else:
            print("\n⚠️ Basic setup OK, but no CSV files found for testing")
    else:
        print("\n❌ Setup incomplete - please fix the issues above")
        
    print("\n" + "="*50)

if __name__ == "__main__":
    main() 