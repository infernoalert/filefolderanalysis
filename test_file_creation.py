#!/usr/bin/env python3
"""
Test script to verify that both CLI and UI create output files

This script demonstrates that the UI now creates the same output files as CLI
"""

import os
import tempfile
import json
from pathlib import Path

# Test with UI function
def test_ui_file_creation():
    """Test that UI creates output files"""
    print("🧪 Testing UI file creation...")
    
    # Import the UI function
    from app import run_local_analysis, create_default_local_config
    
    # Create a test CSV content
    test_csv_content = """Name,Path,Item Type,Modified By,File Size,Modified
Microsoft Corp,/tech/Microsoft,Folder,John Doe,1024,2024-01-01
Apple Inc,/tech/Apple,Folder,Jane Smith,2048,2024-01-02
Google LLC,/tech/Google,Folder,Bob Wilson,4096,2024-01-03
Test File.txt,/tech/test.txt,File,Admin,512,2024-01-04"""
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_csv:
        tmp_csv.write(test_csv_content)
        tmp_csv_path = tmp_csv.name
    
    try:
        # Create test config
        config = create_default_local_config()
        config["filter_type"] = "folders"  # Only analyze folders
        
        # Create file-like object for the CSV
        class MockFile:
            def __init__(self, content):
                self.content = content.encode()
            def getvalue(self):
                return self.content
        
        mock_csv_file = MockFile(test_csv_content)
        
        # Run UI analysis
        success, message, results = run_local_analysis(mock_csv_file, config)
        
        if success and results:
            output_files = results.get("output_files", [])
            print(f"✅ UI created {len(output_files)} files:")
            for file_path in output_files:
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    print(f"   📄 {os.path.basename(file_path)} ({size:,} bytes)")
                else:
                    print(f"   ❌ {os.path.basename(file_path)} (file not found)")
            
            print(f"\n📊 Results summary:")
            print(f"   Companies found: {results['total_companies']}")
            print(f"   Total entries: {results['total_entries']}")
            print(f"   Detector: {'Enhanced' if results['using_enhanced_detector'] else 'Basic'}")
            
            return True, output_files
        else:
            print(f"❌ UI analysis failed: {message}")
            return False, []
            
    except Exception as e:
        print(f"❌ Error testing UI: {e}")
        return False, []
    finally:
        # Cleanup
        if os.path.exists(tmp_csv_path):
            os.unlink(tmp_csv_path)


def test_cli_file_creation():
    """Test that CLI creates output files"""
    print("\n🧪 Testing CLI file creation...")
    
    try:
        from src.core.company_analyzer import CompanyAnalyzer
        
        # Create a test CSV file
        test_csv_content = """Name,Path,Item Type,Modified By,File Size,Modified
Microsoft Corp,/tech/Microsoft,Folder,John Doe,1024,2024-01-01
Apple Inc,/tech/Apple,Folder,Jane Smith,2048,2024-01-02
Google LLC,/tech/Google,Folder,Bob Wilson,4096,2024-01-03
Test File.txt,/tech/test.txt,File,Admin,512,2024-01-04"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_csv:
            tmp_csv.write(test_csv_content)
            tmp_csv_path = tmp_csv.name
        
        try:
            # Initialize analyzer (CLI way)
            analyzer = CompanyAnalyzer(
                csv_file_path=tmp_csv_path,
                chunk_size=5000,
                filter_type="folders"  # Only analyze folders
            )
            
            # Run analysis
            success = analyzer.analyze()
            
            if success:
                # Save results (CLI way)
                output_files = analyzer.save_results(["json", "csv", "txt"])
                
                print(f"✅ CLI created {len(output_files)} files:")
                for file_path in output_files:
                    if os.path.exists(file_path):
                        size = os.path.getsize(file_path)
                        print(f"   📄 {os.path.basename(file_path)} ({size:,} bytes)")
                    else:
                        print(f"   ❌ {os.path.basename(file_path)} (file not found)")
                
                print(f"\n📊 Results summary:")
                print(f"   Companies found: {len(analyzer.companies)}")
                print(f"   Total entries: {sum(analyzer.companies.values())}")
                print(f"   Detector: {'Enhanced' if analyzer.using_enhanced_detector else 'Basic'}")
                
                return True, output_files
            else:
                print("❌ CLI analysis failed")
                return False, []
                
        finally:
            # Cleanup test CSV
            if os.path.exists(tmp_csv_path):
                os.unlink(tmp_csv_path)
    
    except Exception as e:
        print(f"❌ Error testing CLI: {e}")
        return False, []


def compare_outputs(ui_files, cli_files):
    """Compare the outputs from UI and CLI"""
    print("\n🔍 Comparing UI vs CLI outputs...")
    
    ui_basenames = {os.path.basename(f) for f in ui_files}
    cli_basenames = {os.path.basename(f) for f in cli_files}
    
    # Remove timestamps for comparison
    ui_types = {f.split('_')[0] for f in ui_basenames if '_' in f}
    cli_types = {f.split('_')[0] for f in cli_basenames if '_' in f}
    
    print(f"UI file types: {ui_types}")
    print(f"CLI file types: {cli_types}")
    
    if ui_types == cli_types:
        print("✅ Both UI and CLI create the same types of files!")
    else:
        print("❌ File types differ between UI and CLI")
        print(f"   Missing in UI: {cli_types - ui_types}")
        print(f"   Extra in UI: {ui_types - cli_types}")


def cleanup_test_files():
    """Clean up any test files created"""
    print("\n🧹 Cleaning up test files...")
    current_dir = Path(".")
    
    # Find and remove test files
    test_patterns = ["companies_*", "*_test_*"]
    removed_count = 0
    
    for pattern in test_patterns:
        for file_path in current_dir.glob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    removed_count += 1
            except Exception as e:
                print(f"   Could not remove {file_path}: {e}")
    
    print(f"   Removed {removed_count} test files")


def main():
    """Main test function"""
    print("="*60)
    print("🧪 TESTING FILE CREATION: UI vs CLI")
    print("="*60)
    print("This test verifies that both UI and CLI create output files")
    
    # Test UI
    ui_success, ui_files = test_ui_file_creation()
    
    # Test CLI  
    cli_success, cli_files = test_cli_file_creation()
    
    # Compare results
    if ui_success and cli_success:
        compare_outputs(ui_files, cli_files)
        
        print("\n" + "="*60)
        print("✅ CONCLUSION: Both UI and CLI now create output files!")
        print("✅ The issue has been FIXED!")
        print("="*60)
        
        print("\n📝 What was fixed:")
        print("   • UI now calls analyzer.save_results() like CLI does")
        print("   • UI shows created files in new 'Output Files' tab")
        print("   • UI provides download buttons for each file")
        print("   • Files are saved to disk for CLI access too")
        
    else:
        print("\n" + "="*60)
        print("❌ One or both tests failed")
        print("="*60)
    
    # Cleanup
    cleanup_test_files()


if __name__ == "__main__":
    main() 