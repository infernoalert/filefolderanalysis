#!/usr/bin/env python3
"""
Main script for the Company Analyzer

This script provides a command-line interface for analyzing CSV files
and extracting company names. It uses the improved modular architecture
for better organization and maintainability.

Usage:
    python main.py [csv_file] [options]

Example:
    python main.py LPATech.csv
    python main.py data.csv --chunk-size 1000
    python main.py --help
"""

import argparse
import sys
import os
import logging
from pathlib import Path
from typing import Optional

from company_analyzer import CompanyAnalyzer
from config import config


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('company_analyzer.log')
        ]
    )


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Analyze CSV files to extract company names',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py LPATech.csv                    # Analyze LPATech.csv
  python main.py data.csv --chunk-size 1000    # Use custom chunk size
  python main.py --quick-preview               # Quick preview mode
  python main.py --validate-setup              # Validate setup
  python main.py --csv-info data.csv           # Show CSV file info
        """
    )
    
    parser.add_argument(
        'csv_file',
        nargs='?',
        default=config.default_csv_file,
        help=f'CSV file to analyze (default: {config.default_csv_file})'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=config.chunk_size,
        help=f'Chunk size for processing (default: {config.chunk_size})'
    )
    
    parser.add_argument(
        '--output-formats',
        nargs='+',
        choices=['json', 'csv', 'txt'],
        default=config.output_formats,
        help='Output formats to generate (default: all)'
    )
    
    parser.add_argument(
        '--quick-preview',
        action='store_true',
        help='Run quick preview mode (first 10,000 rows)'
    )
    
    parser.add_argument(
        '--validate-setup',
        action='store_true',
        help='Validate the analyzer setup'
    )
    
    parser.add_argument(
        '--csv-info',
        action='store_true',
        help='Show CSV file structure information'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run interactive search after analysis'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--column-mappings',
        nargs='+',
        help='Custom column mappings (format: internal_name=csv_column)'
    )
    
    return parser.parse_args()


def validate_csv_file(csv_file: str) -> bool:
    """Validate that the CSV file exists and is readable"""
    if not os.path.exists(csv_file):
        print(f"❌ Error: CSV file '{csv_file}' not found")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Please make sure the file exists and try again.")
        return False
    
    if not os.path.isfile(csv_file):
        print(f"❌ Error: '{csv_file}' is not a file")
        return False
    
    print(f"✅ CSV file found: {csv_file}")
    return True


def parse_column_mappings(mappings_list: list) -> dict:
    """Parse column mappings from command line arguments"""
    mappings = {}
    for mapping in mappings_list:
        if '=' in mapping:
            internal_name, csv_column = mapping.split('=', 1)
            mappings[internal_name] = csv_column
        else:
            print(f"⚠️  Warning: Invalid column mapping format: {mapping}")
    return mappings


def run_quick_preview(csv_file: str):
    """Run a quick preview analysis"""
    print("🔍 Quick Preview Mode")
    print("=" * 50)
    
    try:
        import pandas as pd
        from collections import Counter
        
        # Read first 10,000 rows
        df = pd.read_csv(csv_file, nrows=10000)
        print(f"✅ Loaded first 10,000 rows for preview")
        
        # Basic company detection
        companies = []
        for name in df['Name'].dropna():
            name = str(name).strip()
            
            # Skip obvious non-company entries
            if any(skip in name.lower() for skip in ['_', 'archive', 'migration', 'opportunities', 'projects']):
                continue
            
            # Basic company pattern matching
            if (len(name) > 3 and 
                name[0].isupper() and 
                not name.isdigit() and
                len(name.split()) <= 5):
                companies.append(name)
        
        # Show results
        company_counts = Counter(companies)
        print(f"\nFound {len(company_counts)} unique potential company names")
        print(f"Total entries: {len(companies)}")
        
        print(f"\nTop 20 Companies:")
        print("-" * 40)
        for i, (company, count) in enumerate(company_counts.most_common(20), 1):
            print(f"{i:2d}. {company:<30} ({count:2d} entries)")
        
        print(f"\nNote: This is a quick preview using only the first 10,000 rows.")
        print("Use the full analysis for complete results.")
        
    except Exception as e:
        print(f"❌ Error during quick preview: {str(e)}")


def main():
    """Main function"""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    print("🏢 Company Analyzer")
    print("=" * 50)
    
    # Validate setup if requested
    if args.validate_setup:
        print("🔧 Validating setup...")
        analyzer = CompanyAnalyzer(args.csv_file, args.chunk_size)
        validation = analyzer.validate_setup()
        
        for check, result in validation.items():
            status = "✅" if result else "❌"
            print(f"{status} {check}: {result}")
        
        if not all(validation.values()):
            print("\n❌ Setup validation failed. Please fix the issues above.")
            return 1
        else:
            print("\n✅ Setup validation passed!")
        return 0
    
    # Show CSV info if requested
    if args.csv_info:
        print(f"📊 CSV File Information: {args.csv_file}")
        print("-" * 40)
        
        analyzer = CompanyAnalyzer(args.csv_file, args.chunk_size)
        csv_info = analyzer.get_csv_structure_info()
        
        if csv_info:
            print(f"Columns: {csv_info['columns']}")
            print(f"Data types: {csv_info['data_types']}")
            if csv_info['suggested_mappings']:
                print(f"Suggested mappings: {csv_info['suggested_mappings']}")
        
        return 0
    
    # Quick preview mode
    if args.quick_preview:
        if not validate_csv_file(args.csv_file):
            return 1
        run_quick_preview(args.csv_file)
        return 0
    
    # Main analysis
    if not validate_csv_file(args.csv_file):
        return 1
    
    try:
        # Initialize analyzer
        analyzer = CompanyAnalyzer(args.csv_file, args.chunk_size)
        
        # Configure column mappings if provided
        if args.column_mappings:
            mappings = parse_column_mappings(args.column_mappings)
            if mappings:
                analyzer.configure_csv_columns(mappings)
                print(f"✅ Applied column mappings: {mappings}")
        
        # Run analysis
        print(f"🔍 Analyzing: {args.csv_file}")
        print(f"📊 Chunk size: {args.chunk_size:,}")
        print()
        
        success = analyzer.analyze()
        
        if not success:
            print("❌ Analysis failed")
            return 1
        
        # Print summary
        analyzer.print_summary()
        
        # Save results
        print("\n💾 Saving results...")
        created_files = analyzer.save_results(args.output_formats)
        
        if created_files:
            print("✅ Results saved to:")
            for file_path in created_files:
                print(f"   📄 {file_path}")
        
        # Show statistics
        stats = analyzer.get_analysis_stats()
        print(f"\n📈 Analysis Statistics:")
        print(f"   Detector type: {stats.get('detector_type', 'unknown').upper()}")
        print(f"   Total rows processed: {stats['total_rows_processed']:,}")
        print(f"   Technical files filtered: {stats['technical_files_filtered']:,}")
        print(f"   Unique companies found: {stats['unique_companies']:,}")
        print(f"   Total company entries: {stats['total_company_entries']:,}")
        
        # Show enhanced analysis if available
        if 'enhanced_analysis' in stats:
            enhanced = stats['enhanced_analysis']
            print(f"\n🚀 Enhanced Analysis:")
            print(f"   Companies detected: {enhanced.get('companies_found', 0)}")
            print(f"   Non-companies filtered: {enhanced.get('non_companies', 0)}")
            print(f"   Detection accuracy: {enhanced.get('company_percentage', 0):.1f}%")
            print(f"   Average confidence: {enhanced.get('average_confidence', 0):.2f}")
            
            # Show top reasons for company detection
            if 'company_reasons' in enhanced:
                print(f"   Top company indicators: {', '.join(list(enhanced['company_reasons'].keys())[:3])}")
            if 'non_company_reasons' in enhanced:
                print(f"   Top exclusion reasons: {', '.join(list(enhanced['non_company_reasons'].keys())[:3])}")
        
        # Interactive search if requested
        if args.interactive:
            analyzer.run_interactive_search()
        
        print("\n🎉 Analysis complete!")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 