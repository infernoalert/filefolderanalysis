import pandas as pd
import re
from collections import Counter

def quick_company_preview():
    """Quick preview of companies in LPATech.csv without full NLP processing"""
    
    print("Quick Company Preview - LPATech.csv")
    print("=" * 50)
    
    try:
        # Read just the first chunk to get a quick preview
        df = pd.read_csv('LPATech.csv', nrows=10000)
        print(f"✓ Loaded first 10,000 rows for preview")
        
        # Extract potential company names from 'Name' column
        companies = []
        
        for name in df['Name'].dropna():
            name = str(name).strip()
            
            # Skip obvious non-company entries
            if any(skip in name.lower() for skip in ['_', 'archive', 'migration', 'opportunities', 'projects', 'managed services', 'template', 'folder']):
                continue
            
            # Look for company patterns
            # Check if it looks like a company name (proper nouns, company suffixes, etc.)
            if (len(name) > 3 and 
                name[0].isupper() and 
                not name.isdigit() and
                len(name.split()) <= 5):  # Reasonable company name length
                companies.append(name)
        
        # Count and display top companies
        company_counts = Counter(companies)
        
        print(f"\nFound {len(company_counts)} unique potential company names")
        print(f"Total folder entries: {len(companies)}")
        
        print(f"\nTop 30 Most Frequent Company Names:")
        print("-" * 50)
        
        for i, (company, count) in enumerate(company_counts.most_common(30), 1):
            print(f"{i:2d}. {company:<35} ({count:2d} folders)")
        
        print(f"\nSample of all company names found:")
        print("-" * 50)
        all_companies = sorted(company_counts.keys())
        for i, company in enumerate(all_companies[:50], 1):
            print(f"{i:2d}. {company}")
        
        if len(all_companies) > 50:
            print(f"... and {len(all_companies) - 50} more companies")
        
        print(f"\nNote: This is a quick preview using only the first 10,000 rows.")
        print("Run 'python sharepoint_company_analyzer.py' for full analysis.")
        
    except FileNotFoundError:
        print("✗ LPATech.csv not found in current directory")
        print("Please make sure the file is in the same directory as this script")
    except Exception as e:
        print(f"✗ Error reading CSV: {str(e)}")

if __name__ == "__main__":
    quick_company_preview() 