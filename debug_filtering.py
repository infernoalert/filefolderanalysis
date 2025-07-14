#!/usr/bin/env python3
"""
Debug script to understand why entries are being filtered as technical files

This script will show you exactly what's in your CSV and why each entry
is being filtered out, helping you troubleshoot the company detection.
"""

import pandas as pd
import sys
from pathlib import Path
from src.core.company_detector import CompanyDetector
from src.core.enhanced_company_detector import EnhancedCompanyDetector
from src.config.config import AnalyzerConfig

def debug_filtering(csv_file_path: str, max_entries: int = 20):
    """
    Debug what entries are being filtered and why
    
    Args:
        csv_file_path: Path to your CSV file
        max_entries: Maximum number of entries to show (default: 20)
    """
    print(f"🔍 DEBUGGING COMPANY DETECTION FOR: {csv_file_path}")
    print("=" * 80)
    
    # Check if file exists
    if not Path(csv_file_path).exists():
        print(f"❌ ERROR: File '{csv_file_path}' not found!")
        print("Available files in current directory:")
        for file in Path(".").glob("*.csv"):
            print(f"  - {file}")
        return
    
    # Load configuration
    config = AnalyzerConfig()
    
    # Initialize detectors
    try:
        enhanced_detector = EnhancedCompanyDetector()
        basic_detector = CompanyDetector()
        print("✅ Both Enhanced and Basic detectors loaded successfully")
    except Exception as e:
        print(f"⚠️  Enhanced detector failed: {e}")
        print("Using basic detector only")
        enhanced_detector = None
        basic_detector = CompanyDetector()
    
    # Load CSV
    try:
        df = pd.read_csv(csv_file_path)
        print(f"✅ CSV loaded successfully: {len(df)} rows")
    except Exception as e:
        print(f"❌ ERROR loading CSV: {e}")
        return
    
    # Check column structure
    print(f"\n📊 CSV STRUCTURE:")
    print(f"Columns: {list(df.columns)}")
    print(f"Expected 'Name' column: {'Name' in df.columns}")
    
    # Use the first column if 'Name' doesn't exist
    name_column = 'Name' if 'Name' in df.columns else df.columns[0]
    print(f"Using column: '{name_column}'")
    
    # Analyze entries
    print(f"\n🔍 ANALYZING FIRST {max_entries} ENTRIES:")
    print("-" * 80)
    
    technical_count = 0
    company_count = 0
    
    for idx, (i, row) in enumerate(df.head(max_entries).iterrows()):
        name = str(row[name_column]).strip()
        
        # Test with basic detector
        is_technical_basic = basic_detector.is_technical_file(name)
        is_company_basic = basic_detector.is_likely_company(name)
        
        # Test with enhanced detector if available
        if enhanced_detector:
            is_technical_enhanced = enhanced_detector.is_technical_file(name)
            is_company_enhanced = enhanced_detector.is_likely_company(name)
            
            # Get detailed analysis
            analysis = enhanced_detector.enhanced_company_detection(name)
            
            print(f"\n{idx+1:2d}. '{name}'")
            print(f"    Basic:    Technical={is_technical_basic}, Company={is_company_basic}")
            print(f"    Enhanced: Technical={is_technical_enhanced}, Company={is_company_enhanced}")
            print(f"    Analysis: {analysis['is_company']} (confidence: {analysis['confidence']:.2f})")
            print(f"    Reasons:  {', '.join(analysis['reasons'])}")
            
            if is_technical_enhanced:
                technical_count += 1
            elif is_company_enhanced:
                company_count += 1
        else:
            print(f"\n{idx+1:2d}. '{name}'")
            print(f"    Basic: Technical={is_technical_basic}, Company={is_company_basic}")
            
            if is_technical_basic:
                technical_count += 1
            elif is_company_basic:
                company_count += 1
    
    # Summary
    print(f"\n📈 SAMPLE SUMMARY (first {max_entries} entries):")
    print(f"Technical files: {technical_count}")
    print(f"Likely companies: {company_count}")
    print(f"Other: {max_entries - technical_count - company_count}")
    
    # Show filtering patterns
    print(f"\n⚙️  ACTIVE FILTERING PATTERNS:")
    print("These patterns will cause entries to be filtered as technical files:")
    
    patterns = config.exclude_patterns
    for i, pattern in enumerate(patterns[:10], 1):  # Show first 10 patterns
        print(f"  {i:2d}. {pattern}")
    
    if len(patterns) > 10:
        print(f"  ... and {len(patterns) - 10} more patterns")
    
    print(f"\n💡 SOLUTIONS:")
    print("If legitimate companies are being filtered out, you can:")
    print("1. Add them to known_companies in config")
    print("2. Modify exclude_patterns to be less restrictive")
    print("3. Use a different CSV with cleaner company names")
    print("4. Manually clean your data before analysis")
    
    # Show some examples of what would pass
    print(f"\n✅ EXAMPLES THAT WOULD PASS:")
    test_companies = [
        "Microsoft Corporation",
        "Apple Inc",
        "Google LLC",
        "Amazon Web Services",
        "Acme Company",
        "Johnson & Johnson",
        "General Electric"
    ]
    
    detector = enhanced_detector if enhanced_detector else basic_detector
    
    for company in test_companies:
        is_company = detector.is_likely_company(company)
        print(f"  '{company}' → {'✅ PASS' if is_company else '❌ FAIL'}")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python debug_filtering.py <csv_file_path>")
        print("Example: python debug_filtering.py LPATech.csv")
        return
    
    csv_file = sys.argv[1]
    debug_filtering(csv_file)

if __name__ == "__main__":
    main() 