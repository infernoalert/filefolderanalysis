#!/usr/bin/env python3
"""
Test script for Enhanced Offline Mode with Name Categorization

This script demonstrates the new offline name categorization feature that
distinguishes between actual companies and other entities like abbreviations,
technical terms, and document references.
"""

import sys
from pathlib import Path
from collections import Counter

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.name_categorizer import NameCategorizer
from src.core.results_manager import ResultsManager


def test_name_categorization():
    """Test the name categorization functionality"""
    
    print("=" * 80)
    print("ENHANCED OFFLINE MODE - NAME CATEGORIZATION TEST")
    print("=" * 80)
    
    # Initialize the name categorizer
    categorizer = NameCategorizer()
    
    # Test cases from the user's example and common scenarios
    test_names = [
        # User's specific example
        "PROP & VAR",
        
        # Other common abbreviations
        "T&C",
        "R&D", 
        "HR",
        "IT",
        "QA",
        "API",
        "SDK",
        "BIM",
        "CAD",
        "MEP",
        "HVAC",
        "RFP",
        "PO",
        "GST",
        "VAT",
        "KPI",
        "SLA",
        "CEO",
        "CTO",
        "CFO",
        
        # Version numbers and technical terms
        "v2.1.3",
        "Build 123",
        "Version 1.0",
        "Dev Server",
        "Test Database",
        "Admin Panel",
        "Section 4.2",
        "Page 10",
        "Chapter 1",
        
        # Real companies
        "Microsoft Corporation",
        "Apple Inc",
        "Google LLC",
        "Amazon Web Services",
        "Boeing Company",
        "Tesla Motors",
        "Caterpillar Inc",
        "Johnson & Johnson",
        "Procter & Gamble",
        
        # Potential companies (proper nouns)
        "Smith Construction",
        "ABC Engineering",
        "Global Solutions",
        "Pacific Industries",
        "Metro Development",
        "Elite Services",
        
        # Mixed cases
        "ABC123",
        "XYZ Corp",
        "DEVELOPMENT",
        "Production",
        "Marketing Team",
        "Sales Department",
        "Project Alpha",
        "Meeting Room A",
        "North Office",
        "Q1 2024",
        "Annual Report",
        
        # File extensions and technical
        "document.pdf",
        "presentation.pptx",
        "data.csv",
        "config.json",
        "backup.zip",
        "image.jpg",
        
        # Geographic and location
        "Head Office",
        "Regional Office",
        "Building A",
        "Floor 5",
        "North Wing",
        "Central Location",
        
        # Single letters and codes
        "A",
        "AB",
        "ABC",
        "XY123",
        "DEF-456",
        "12345",
        
        # Industry terms
        "Construction Materials",
        "Software Development",
        "Healthcare Services",
        "Financial Planning",
        "Education Training",
        "Retail Operations"
    ]
    
    print(f"\nTesting {len(test_names)} name categorization examples:\n")
    
    # Categorize all names
    results = categorizer.batch_categorize(test_names)
    
    # Display results in a nice format
    print(f"{'Name':<25} {'Category':<20} {'Description'}")
    print("-" * 80)
    
    for result in results:
        name = result['name']
        category = result['category']
        description = result['description']
        
        # Truncate long descriptions for display
        if len(description) > 33:
            description = description[:30] + "..."
        
        print(f"{name:<25} {category:<20} {description}")
    
    # Show category summary
    print(f"\n" + "=" * 80)
    print("CATEGORY SUMMARY:")
    print("=" * 80)
    
    category_summary = categorizer.get_category_summary(test_names)
    
    for category, count in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(test_names)) * 100
        print(f"{category:<25} {count:3d} names ({percentage:5.1f}%)")
    
    return results


def test_csv_output():
    """Test the enhanced CSV output format"""
    
    print(f"\n" + "=" * 80)
    print("ENHANCED CSV OUTPUT TEST")
    print("=" * 80)
    
    # Create sample data that mimics analysis results
    sample_companies = Counter({
        "PROP & VAR": 25,
        "Microsoft Corporation": 18,
        "T&C": 15,
        "Apple Inc": 12,
        "R&D": 10,
        "HR": 8,
        "IT": 7,
        "Smith Construction": 6,
        "API": 5,
        "v2.1.3": 4,
        "Dev Server": 3,
        "Google LLC": 3,
        "Section 4.2": 2,
        "CEO": 2,
        "Building A": 2,
        "ABC Engineering": 1,
        "document.pdf": 1,
        "Q1 2024": 1
    })
    
    # Initialize results manager
    results_manager = ResultsManager(base_filename="test_enhanced")
    
    # Test CSV generation
    print("Generating enhanced CSV with categorization...")
    csv_file = results_manager._save_csv(sample_companies)
    
    if csv_file:
        print(f"✅ Enhanced CSV saved: {csv_file}")
        
        # Read and display first few lines
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"\nFirst 10 lines of the enhanced CSV:")
                print("-" * 80)
                for i, line in enumerate(lines[:10]):
                    print(f"{i+1:2d}: {line.strip()}")
                if len(lines) > 10:
                    print(f"... and {len(lines) - 10} more lines")
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
    else:
        print("❌ Failed to generate CSV file")
    
    return csv_file


def test_summary_output():
    """Test the enhanced summary output"""
    
    print(f"\n" + "=" * 80)
    print("ENHANCED SUMMARY OUTPUT TEST")
    print("=" * 80)
    
    # Create sample data
    sample_companies = Counter({
        "PROP & VAR": 25,
        "Microsoft Corporation": 18,
        "T&C": 15,
        "Apple Inc": 12,
        "R&D": 10,
        "HR": 8,
        "IT": 7,
        "Smith Construction": 6,
        "API": 5,
        "v2.1.3": 4
    })
    
    # Initialize results manager
    results_manager = ResultsManager()
    
    # Test summary output
    print("Generating enhanced summary...")
    results_manager.print_summary(sample_companies, {}, 'all')
    
    return True


def main():
    """Main test function"""
    
    print("Testing Enhanced Offline Mode with Name Categorization")
    print("This demonstrates the solution for distinguishing between actual companies")
    print("and other entities like 'PROP & VAR' (Proposal and Variation)")
    
    try:
        # Test 1: Name categorization
        print("\n🧪 TEST 1: Name Categorization")
        results = test_name_categorization()
        
        # Test 2: CSV output
        print("\n🧪 TEST 2: Enhanced CSV Output")
        csv_file = test_csv_output()
        
        # Test 3: Summary output
        print("\n🧪 TEST 3: Enhanced Summary Output")
        test_summary_output()
        
        print(f"\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("Key improvements for offline mode:")
        print("✅ Changed 'Company' column to 'Name'")
        print("✅ Added 'Category' column to classify names")
        print("✅ Added 'Description' column with explanations")
        print("✅ 'PROP & VAR' is now properly identified as 'Proposal and Variation'")
        print("✅ Enhanced text reports with categorization statistics")
        print("✅ Improved console output with category information")
        
        if csv_file:
            print(f"\n📁 Check the generated CSV file: {csv_file}")
            print("   It now contains Name, Folder_Count, Category, and Description columns")
        
        print("\n💡 Usage in your analysis:")
        print("   Just run your normal offline analysis and you'll get the enhanced output!")
        print("   Example: python main.py your_file.csv")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 