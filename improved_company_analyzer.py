import pandas as pd
import numpy as np
import re
from collections import Counter, defaultdict
import json
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

class ImprovedCompanyAnalyzer:
    def __init__(self, csv_file_path="LPATech.csv", chunk_size=5000):
        """
        Improved Company Analyzer specifically designed for LPATech.csv
        Better filtering and company name extraction
        """
        self.csv_file_path = csv_file_path
        self.chunk_size = chunk_size
        self.companies = Counter()
        self.company_details = defaultdict(lambda: {
            'folders': set(),
            'paths': set(),
            'modified_by': set(),
            'count': 0,
            'file_types': set()
        })
        
        # Define patterns to exclude (technical files, reports, etc.)
        self.exclude_patterns = [
            r'^NEM1[23]#.*',  # NEM12, NEM13 energy files
            r'^EL\d{4}EP[VA]\d\.csv$',  # Energy meter files
            r'^BR\d+\.csv$',  # BR numbered files
            r'^RC\d{4}VT[A-Z]\d+#.*',  # Technical reference files
            r'.*\.(csv|xlsx|xls|docx|doc|pptx|ppt|pdf|zip|log|msg|ods|xlsb)$',  # Files with extensions
            r'^_.*',  # Underscore prefixed
            r'^\d{4}.*',  # Year prefixed
            r'^[A-Z]{2,3}\d+.*',  # Technical codes
            r'.*[#@].*',  # Files with special characters
            r'^(Archive|Migration|Opportunities|Projects|Managed Services|Template|Folder|Reports|Data|Files|Documents)$',  # Common folder names
            r'.*Timesheet.*',  # Timesheet files
            r'.*Reconciliation.*',  # Reconciliation files
            r'.*Invoice.*',  # Invoice files
            r'.*Sample.*',  # Sample files
            r'.*Report.*',  # Report files
            r'.*How to.*',  # How-to files
            r'.*Meeting.*',  # Meeting files
            r'.*Implementation.*',  # Implementation files
            r'.*Acc\d+.*',  # Account numbers
            r'.*FY\d{2}.*',  # Financial year references
            r'.*\d{4}-\d{2}-\d{2}.*',  # Date patterns
            r'.*\d{8}.*',  # Date stamps
        ]
        
        # Define company indicators
        self.company_indicators = [
            r'\b(inc|incorporated|llc|corp|corporation|company|co|ltd|limited|pty|plc)\b',
            r'\b(group|holdings|partners|associates|solutions|services|technologies|systems)\b',
            r'\b(consulting|enterprises|international|global|worldwide)\b',
            r'\b(bank|financial|properties|realty|capital|investments|fund|trust)\b',
            r'\b(insurance|healthcare|medical|pharmaceuticals|biotech)\b',
            r'\b(energy|oil|gas|utilities|mining|construction|manufacturing)\b',
            r'\b(retail|hospitality|restaurants|hotels|airlines|logistics|transport)\b',
            r'\b(communications|media|entertainment|software|tech|technology)\b',
            r'\b(university|college|school|hospital|clinic|care|legal|law)\b',
            r'\b(accounting|advisory|management|consulting|professional)\b'
        ]
        
        # Known company names from quick preview
        self.known_companies = {
            'Accent Group', 'AGL', 'BXP', 'Altogether', 'Cleanpeak', 'Cotton On',
            'Digital Realty', 'EnerConnex', 'GCG', 'Jewish Care', 'Berkshire Bank',
            'Boston Properties', 'Bright and Duggan'
        }
    
    def _is_technical_file(self, name):
        """Check if the name is a technical file that should be excluded"""
        if not name:
            return True
        
        name = str(name).strip()
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if re.match(pattern, name, re.IGNORECASE):
                return True
        
        return False
    
    def _is_likely_company(self, name):
        """Determine if a name is likely a company name with improved logic"""
        if not name or len(name) < 2:
            return False
        
        name = str(name).strip()
        
        # Skip if it's a technical file
        if self._is_technical_file(name):
            return False
        
        # Check if it's a known company
        if name in self.known_companies:
            return True
        
        # Check for company indicators
        for indicator in self.company_indicators:
            if re.search(indicator, name, re.IGNORECASE):
                return True
        
        # Check for proper noun patterns (capitalized words)
        words = name.split()
        if len(words) >= 2:
            # Multiple capitalized words
            capitalized_words = [w for w in words if w and w[0].isupper() and w.isalpha()]
            if len(capitalized_words) >= 2 and len(capitalized_words) == len(words):
                return True
        
        # Single word companies (brand names)
        elif len(words) == 1:
            word = words[0]
            # Must be capitalized, alphabetic, and reasonable length
            if (word[0].isupper() and 
                word.isalpha() and 
                3 <= len(word) <= 15 and
                word not in ['Archive', 'Migration', 'Projects', 'Documents', 'Files', 'Folders', 'Templates', 'Forms', 'Reports', 'Data', 'Information', 'Resources', 'Tools', 'Utilities', 'Settings', 'Configuration', 'Administration', 'Management', 'Operations', 'Support', 'Help', 'Training', 'Education', 'Research', 'Development', 'Testing', 'Production', 'Staging', 'Backup', 'Recovery', 'Security', 'Privacy', 'Compliance', 'Audit', 'Finance', 'Accounting', 'Legal', 'Human', 'Resources', 'Marketing', 'Sales', 'Customer', 'Service', 'Quality', 'Agreements', 'Contracts', 'Thermal', 'Active', 'Apportionment', 'Accuracy', 'April', 'March']):
                return True
        
        return False
    
    def _clean_company_name(self, name):
        """Clean and standardize company names"""
        if not name:
            return ""
        
        name = str(name).strip()
        
        # Remove common prefixes that aren't part of company names
        name = re.sub(r'^\d{4}\s+', '', name)  # Remove year prefixes
        name = re.sub(r'^(AU|US|UK|NZ)\s+', '', name)  # Remove country prefixes
        
        # Clean up spacing
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def analyze_csv(self):
        """Analyze the LPATech.csv file and extract company names"""
        print(f"Improved Company Analysis of {self.csv_file_path}")
        print(f"Processing in chunks of {self.chunk_size} rows")
        
        try:
            # Get basic info about the CSV
            try:
                total_rows = sum(1 for _ in open(self.csv_file_path, encoding='utf-8')) - 1
            except UnicodeDecodeError:
                total_rows = sum(1 for _ in open(self.csv_file_path, encoding='utf-8-sig')) - 1
            
            print(f"Total rows to process: {total_rows:,}")
            
            # Process CSV in chunks
            try:
                chunk_iter = pd.read_csv(self.csv_file_path, chunksize=self.chunk_size, encoding='utf-8')
            except UnicodeDecodeError:
                chunk_iter = pd.read_csv(self.csv_file_path, chunksize=self.chunk_size, encoding='utf-8-sig')
            
            all_companies = []
            technical_files_count = 0
            processed_rows = 0
            
            for chunk_num, chunk in enumerate(tqdm(chunk_iter, desc="Processing chunks")):
                for _, row in chunk.iterrows():
                    processed_rows += 1
                    name = row.get('Name', '')
                    
                    if self._is_technical_file(name):
                        technical_files_count += 1
                        continue
                    
                    # Clean the name
                    clean_name = self._clean_company_name(name)
                    
                    # Check if it's likely a company
                    if self._is_likely_company(clean_name):
                        # Store detailed information
                        self.company_details[clean_name]['folders'].add(name)
                        self.company_details[clean_name]['paths'].add(row.get('Path', ''))
                        self.company_details[clean_name]['modified_by'].add(row.get('Modified By', ''))
                        self.company_details[clean_name]['count'] += 1
                        
                        # Determine file type
                        item_type = row.get('Item Type', '')
                        if item_type:
                            self.company_details[clean_name]['file_types'].add(item_type)
                        
                        all_companies.append(clean_name)
            
            # Process results
            self.companies = Counter(all_companies)
            
            print(f"\n✓ Analysis complete!")
            print(f"Processed {processed_rows:,} rows")
            print(f"Filtered out {technical_files_count:,} technical files")
            print(f"Found {len(self.companies)} unique company names")
            print(f"Total company folder entries: {sum(self.companies.values())}")
            
            return self.companies
            
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
            return Counter()
    
    def get_company_details(self, company_name):
        """Get detailed information about a specific company"""
        if company_name not in self.company_details:
            return {
                'company_name': company_name,
                'folder_count': 0,
                'folders': [],
                'paths': [],
                'modified_by': [],
                'file_types': []
            }
        
        details = self.company_details[company_name]
        return {
            'company_name': company_name,
            'folder_count': int(details['count']),
            'folders': sorted(list(details['folders'])),
            'paths': sorted(list(details['paths'])),
            'modified_by': sorted(list(details['modified_by'])),
            'file_types': sorted(list(details['file_types']))
        }
    
    def save_results(self, output_format='all'):
        """Save results with improved formatting"""
        if not self.companies:
            print("No companies to save.")
            return
        
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format in ['json', 'all']:
            # Basic results
            output_file = f'companies_improved_{timestamp}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.companies), f, indent=2, ensure_ascii=False)
            print(f"✓ Results saved to {output_file}")
            
            # Detailed results
            detailed_file = f'companies_detailed_improved_{timestamp}.json'
            detailed_data = {}
            for company in self.companies.keys():
                detailed_data[company] = self.get_company_details(company)
            
            with open(detailed_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"✓ Detailed results saved to {detailed_file}")
        
        if output_format in ['csv', 'all']:
            output_file = f'companies_improved_{timestamp}.csv'
            df = pd.DataFrame([
                {'Company': company, 'Folder_Count': count}
                for company, count in self.companies.most_common()
            ])
            df.to_csv(output_file, index=False)
            print(f"✓ CSV results saved to {output_file}")
        
        if output_format in ['txt', 'all']:
            output_file = f'companies_improved_{timestamp}.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("IMPROVED COMPANY ANALYSIS - LPATECH.CSV\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Total companies found: {len(self.companies)}\n")
                f.write(f"Total folder entries: {sum(self.companies.values())}\n\n")
                
                f.write("TOP COMPANIES BY FOLDER COUNT:\n")
                f.write("-" * 40 + "\n")
                
                for i, (company, count) in enumerate(self.companies.most_common(100), 1):
                    f.write(f"{i:3d}. {company:<40} ({count:3d} folders)\n")
                
                f.write("\nCOMPANY DETAILS:\n")
                f.write("-" * 40 + "\n")
                
                for company in sorted(self.companies.keys()):
                    details = self.get_company_details(company)
                    f.write(f"\n{company}:\n")
                    f.write(f"  Folders: {details['folder_count']}\n")
                    f.write(f"  Paths: {len(details['paths'])}\n")
                    f.write(f"  Modified by: {len(details['modified_by'])} people\n")
                    if details['file_types']:
                        f.write(f"  Types: {', '.join(details['file_types'])}\n")
            
            print(f"✓ Detailed text results saved to {output_file}")
    
    def print_summary(self):
        """Print improved summary"""
        if not self.companies:
            print("No analysis results available.")
            return
        
        print("\n" + "="*80)
        print("IMPROVED COMPANY ANALYSIS SUMMARY - LPATECH.CSV")
        print("="*80)
        print(f"Total unique companies found: {len(self.companies)}")
        print(f"Total company folder entries: {sum(self.companies.values())}")
        
        print(f"\nTop 50 Companies by Folder Count:")
        print("-" * 60)
        for i, (company, count) in enumerate(self.companies.most_common(50), 1):
            print(f"{i:2d}. {company:<45} ({count:3d} folders)")
        
        # Statistics
        counts = list(self.companies.values())
        print(f"\nDistribution Analysis:")
        print("-" * 30)
        print(f"Companies with 1 folder:      {sum(1 for c in counts if c == 1):3d}")
        print(f"Companies with 2-5 folders:   {sum(1 for c in counts if 2 <= c <= 5):3d}")
        print(f"Companies with 6-10 folders:  {sum(1 for c in counts if 6 <= c <= 10):3d}")
        print(f"Companies with 11-20 folders: {sum(1 for c in counts if 11 <= c <= 20):3d}")
        print(f"Companies with 21+ folders:   {sum(1 for c in counts if c > 20):3d}")
        
        print(f"\nNote: Technical files and data files have been filtered out.")
        print("Results focus on actual company/organization names.")
    
    def search_companies(self, query):
        """Search for companies matching a query"""
        if not self.companies:
            return []
        
        query_lower = query.lower()
        matches = []
        
        for company, count in self.companies.items():
            if query_lower in company.lower():
                matches.append((company, count))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

def main():
    """Main function"""
    print("Improved SharePoint Company Analyzer")
    print("=" * 60)
    
    import os
    if not os.path.exists('LPATech.csv'):
        print("Error: LPATech.csv not found.")
        return
    
    # Initialize analyzer
    analyzer = ImprovedCompanyAnalyzer()
    
    # Run analysis
    companies = analyzer.analyze_csv()
    
    if companies:
        # Print summary
        analyzer.print_summary()
        
        # Save results
        print("\nSaving results...")
        analyzer.save_results('all')
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print("Files created:")
        print("- companies_improved_YYYYMMDD_HHMMSS.json")
        print("- companies_detailed_improved_YYYYMMDD_HHMMSS.json")
        print("- companies_improved_YYYYMMDD_HHMMSS.csv")
        print("- companies_improved_YYYYMMDD_HHMMSS.txt")
        
        # Interactive search
        print("\nInteractive Search (type 'quit' to exit):")
        while True:
            query = input("Search companies > ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            if query:
                matches = analyzer.search_companies(query)
                if matches:
                    print(f"Found {len(matches)} matches:")
                    for company, count in matches[:10]:
                        print(f"  {company} ({count} folders)")
                else:
                    print("No matches found.")
    else:
        print("No companies found.")

if __name__ == "__main__":
    main() 