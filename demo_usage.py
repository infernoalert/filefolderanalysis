#!/usr/bin/env python3
"""
Demonstration of File Folder Analysis Tool UI Usage

This script shows how to use the UI application and provides 
sample usage examples for different scenarios.
"""

import json
import os
from pathlib import Path

def create_demo_files():
    """Create demo files for testing the UI"""
    
    print("🎯 Creating demo files for UI testing...")
    
    # Create demo directory
    demo_dir = Path("demo")
    demo_dir.mkdir(exist_ok=True)
    
    # Create sample CSV data
    csv_content = """Name,Path,Modified By,Item Type,File Size,Modified
Microsoft Corporation,/Documents/Companies/Microsoft Corporation,john.doe,Folder,0,2023-01-15
Apple Inc,/Documents/Companies/Apple Inc,jane.smith,Folder,0,2023-01-20
Google LLC,/Documents/Companies/Google LLC,bob.johnson,Folder,0,2023-01-25
Amazon Web Services,/Documents/Companies/Amazon Web Services,alice.brown,Folder,0,2023-02-01
Tesla Inc,/Documents/Companies/Tesla Inc,charlie.davis,Folder,0,2023-02-05
Meta Platforms,/Documents/Companies/Meta Platforms,diana.wilson,Folder,0,2023-02-10
Netflix Inc,/Documents/Companies/Netflix Inc,frank.miller,Folder,0,2023-02-15
Salesforce,/Documents/Companies/Salesforce,grace.taylor,Folder,0,2023-02-20
Intel Corporation,/Documents/Companies/Intel Corporation,henry.clark,Folder,0,2023-02-25
Adobe Inc,/Documents/Companies/Adobe Inc,iris.martinez,Folder,0,2023-03-01
Microsoft Word Document,/Documents/Microsoft Word Document.docx,john.doe,File,245760,2023-01-15
Apple Marketing Material,/Documents/Apple Marketing Material.pdf,jane.smith,File,1048576,2023-01-20
Google Analytics Report,/Documents/Google Analytics Report.xlsx,bob.johnson,File,512000,2023-01-25
Amazon Invoice,/Documents/Amazon Invoice.pdf,alice.brown,File,204800,2023-02-01
Tesla Presentation,/Documents/Tesla Presentation.pptx,charlie.davis,File,2097152,2023-02-05"""
    
    with open(demo_dir / "sample_companies.csv", "w") as f:
        f.write(csv_content)
    
    # Create local configuration
    local_config = {
        "chunk_size": 1000,
        "filter_type": "all",
        "confidence_threshold": 0.3,
        "enable_enhanced_detection": True,
        "enable_caching": True,
        "log_level": "INFO",
        "output_formats": ["json", "csv", "txt"],
        "max_search_results": 20,
        "max_summary_companies": 100,
        "min_company_name_length": 2,
        "max_company_name_length": 50,
        "spacy_model": "en_core_web_sm",
        "known_companies": [
            "Microsoft Corporation",
            "Apple Inc",
            "Google LLC",
            "Amazon Web Services",
            "Tesla Inc",
            "Meta Platforms",
            "Netflix Inc"
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
    
    with open(demo_dir / "demo_local_config.json", "w") as f:
        json.dump(local_config, f, indent=2)
    
    # Create MCP configuration
    mcp_config = {
        "chunk_size": 1000,
        "filter_type": "all",
        "confidence_threshold": 0.3,
        "enable_enhanced_detection": True,
        "enable_ai_analysis": True,
        "enable_mcp_server": True,
        "openai_model": "gpt-3.5-turbo",
        "openai_max_tokens": 2000,
        "openai_temperature": 0.3,
        "ai_max_companies_batch": 10,
        "mcp_server_host": "0.0.0.0",
        "mcp_server_port": 8005,
        "mcp_enable_cors": True,
        "log_level": "INFO",
        "output_formats": ["json", "csv", "txt"],
        "max_search_results": 20,
        "max_summary_companies": 100,
        "known_companies": [
            "Microsoft Corporation",
            "Apple Inc",
            "Google LLC",
            "Amazon Web Services",
            "Tesla Inc",
            "Meta Platforms",
            "Netflix Inc"
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
    
    with open(demo_dir / "demo_mcp_config.json", "w") as f:
        json.dump(mcp_config, f, indent=2)
    
    print(f"✅ Demo files created in {demo_dir}/")
    print(f"   - sample_companies.csv (test data)")
    print(f"   - demo_local_config.json (local analysis config)")
    print(f"   - demo_mcp_config.json (MCP analysis config)")

def show_usage_examples():
    """Show usage examples for the UI"""
    
    print("\n" + "="*60)
    print("🎯 FILE FOLDER ANALYSIS TOOL - UI USAGE EXAMPLES")
    print("="*60)
    
    print("\n📋 STEP-BY-STEP USAGE:")
    print("-" * 40)
    
    print("\n1️⃣ LAUNCH THE APPLICATION:")
    print("   python run_ui.py")
    print("   # OR")
    print("   streamlit run app.py")
    
    print("\n2️⃣ OPEN IN BROWSER:")
    print("   http://localhost:8501")
    
    print("\n3️⃣ CHOOSE ANALYSIS MODE:")
    print("   📍 Local (Offline) - Fast, no internet needed")
    print("   📍 MCP (Online with AI) - AI-enhanced insights")
    
    print("\n4️⃣ UPLOAD YOUR CSV FILE:")
    print("   📂 Click 'Upload CSV File'")
    print("   📂 Select your data file (try demo/sample_companies.csv)")
    print("   📂 Preview shows automatically")
    
    print("\n5️⃣ CONFIGURE ANALYSIS:")
    print("   🔧 Option A: Upload JSON config file")
    print("   🔧 Option B: Use default settings")
    print("   🔧 Option C: Download template and customize")
    
    print("\n6️⃣ FOR MCP MODE:")
    print("   🔑 Enter OpenAI API key")
    print("   🔑 Get key from: https://platform.openai.com/")
    
    print("\n7️⃣ RUN ANALYSIS:")
    print("   ▶️  Click 'Start Analysis'")
    print("   ⏳ Wait for processing")
    print("   📊 View results in tabs")
    
    print("\n" + "="*60)
    print("🎯 CONFIGURATION FILE EXAMPLES")
    print("="*60)
    
    print("\n📄 LOCAL ANALYSIS CONFIG:")
    print("""
{
  "chunk_size": 5000,
  "filter_type": "all",
  "confidence_threshold": 0.3,
  "enable_enhanced_detection": true,
  "known_companies": [
    "Microsoft Corporation",
    "Apple Inc",
    "Google LLC"
  ]
}
""")
    
    print("\n📄 MCP ANALYSIS CONFIG:")
    print("""
{
  "chunk_size": 5000,
  "filter_type": "all",
  "confidence_threshold": 0.3,
  "enable_enhanced_detection": true,
  "enable_ai_analysis": true,
  "openai_model": "gpt-3.5-turbo",
  "openai_max_tokens": 2000,
  "ai_max_companies_batch": 20
}
""")
    
    print("\n" + "="*60)
    print("🎯 TYPICAL WORKFLOW SCENARIOS")
    print("="*60)
    
    print("\n📁 SCENARIO 1: Quick SharePoint Analysis")
    print("   1. Export SharePoint library to CSV")
    print("   2. Launch UI: python run_ui.py")
    print("   3. Upload CSV file")
    print("   4. Select 'Local (Offline)' mode")
    print("   5. Use default configuration")
    print("   6. Click 'Start Analysis'")
    print("   7. View company list in results")
    
    print("\n🤖 SCENARIO 2: AI-Enhanced Business Intelligence")
    print("   1. Prepare CSV data with company information")
    print("   2. Launch UI: python run_ui.py")
    print("   3. Upload CSV file")
    print("   4. Select 'MCP (Online with AI)' mode")
    print("   5. Enter OpenAI API key")
    print("   6. Upload or use default MCP configuration")
    print("   7. Click 'Start Analysis'")
    print("   8. Review AI executive summary")
    print("   9. Explore industry classifications")
    print("   10. Read strategic recommendations")
    
    print("\n🔧 SCENARIO 3: Custom Configuration")
    print("   1. Download configuration template")
    print("   2. Modify settings (chunk_size, known_companies, etc.)")
    print("   3. Save as custom_config.json")
    print("   4. Launch UI and upload custom config")
    print("   5. Upload CSV file")
    print("   6. Run analysis with custom settings")
    
    print("\n" + "="*60)
    print("📊 UNDERSTANDING RESULTS")
    print("="*60)
    
    print("\n📈 SUMMARY TAB:")
    print("   • Total Companies: Unique companies found")
    print("   • Total Entries: All mentions across files")
    print("   • Detector Type: NLP-enhanced or basic")
    print("   • AI Summary: Business insights (MCP mode)")
    
    print("\n🏢 COMPANIES TAB:")
    print("   • Company List: All detected companies")
    print("   • Count Column: Number of mentions")
    print("   • Interactive Chart: Visual representation")
    print("   • Sortable: Click columns to sort")
    
    print("\n📋 DETAILS TAB:")
    print("   • Technical Stats: Processing performance")
    print("   • AI Analysis: Industry data (MCP mode)")
    print("   • Configuration: Settings used")
    
    print("\n" + "="*60)
    print("🛠️ TROUBLESHOOTING TIPS")
    print("="*60)
    
    print("\n❌ Common Issues:")
    print("   • CSV validation failed → Check file format")
    print("   • Enhanced detector failed → Install spaCy model")
    print("   • API key required → Get OpenAI key")
    print("   • Analysis failed → Check configuration")
    
    print("\n✅ Performance Tips:")
    print("   • Large files → Reduce chunk_size")
    print("   • Faster processing → Use filter_type: 'folders'")
    print("   • Better accuracy → Enable enhanced_detection")
    print("   • Repeat analysis → Enable caching")
    
    print("\n" + "="*60)
    print("🚀 READY TO START!")
    print("="*60)
    print("Run: python run_ui.py")
    print("Then open: http://localhost:8501")
    print("Have fun analyzing your data! 🎉")

def main():
    """Main demonstration function"""
    create_demo_files()
    show_usage_examples()

if __name__ == "__main__":
    main() 