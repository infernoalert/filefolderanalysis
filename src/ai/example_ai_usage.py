#!/usr/bin/env python3
"""
Example: AI-Enhanced Company Analysis

This script demonstrates how to use the new AI and MCP integration features
for advanced company analysis with business insights.
"""

import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the enhanced analyzer
from company_analyzer_ai import AIEnhancedCompanyAnalyzer
from ai_analyzer import AICompanyAnalyzer
from collections import Counter


def example_basic_ai_analysis():
    """Example 1: Basic AI-enhanced analysis"""
    print("🤖 Example 1: Basic AI-Enhanced Analysis")
    print("=" * 50)
    
    # Check if OpenAI API key is configured
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
        return
    
    try:
        # Initialize AI-enhanced analyzer
        # Note: Replace 'LPATech.csv' with your actual CSV file
        analyzer = AIEnhancedCompanyAnalyzer(
            csv_file_path="LPATech.csv",  # Your CSV file
            enable_ai=True,
            filter_type="all"
        )
        
        print("✅ AI analyzer initialized")
        
        # Run complete analysis (includes AI analysis)
        print("🔍 Running analysis...")
        success = analyzer.analyze()
        
        if success:
            print("✅ Analysis completed successfully")
            
            # Print basic summary
            analyzer.print_summary()
            
            # Print AI-enhanced summary
            analyzer.print_ai_summary()
            
            # Get comprehensive statistics
            stats = analyzer.get_comprehensive_stats()
            print(f"\n📊 Analysis Statistics:")
            print(f"   AI Enabled: {stats.get('ai_enabled', False)}")
            print(f"   Companies Found: {stats.get('unique_companies', 0)}")
            print(f"   Detector Type: {stats.get('detector_type', 'unknown').upper()}")
            
            # Save results including AI analysis
            basic_files = analyzer.save_results()
            ai_files = analyzer.save_ai_results()
            
            print(f"\n💾 Results saved:")
            for file_path in basic_files + ai_files:
                print(f"   📄 {file_path}")
                
        else:
            print("❌ Analysis failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_specific_ai_insights():
    """Example 2: Get specific AI insights for known companies"""
    print("\n🎯 Example 2: Specific AI Insights")
    print("=" * 50)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not configured")
        return
    
    try:
        # Create sample company data
        companies = Counter({
            "Microsoft Corporation": 45,
            "Apple Inc": 32,
            "Amazon Web Services": 28,
            "Google LLC": 25,
            "Tesla Inc": 20
        })
        
        # Initialize AI analyzer directly
        ai_analyzer = AICompanyAnalyzer()
        
        print("🔍 Analyzing companies with AI...")
        
        # Run AI analysis
        ai_results = asyncio.run(
            ai_analyzer.analyze_companies(companies, {})
        )
        
        # Generate executive summary
        executive_summary = asyncio.run(
            ai_analyzer.generate_executive_summary(companies, ai_results)
        )
        
        print("✅ AI analysis completed")
        
        # Display results
        if "error" not in ai_results:
            print("\n📊 Industry Classification:")
            industry_data = ai_results.get("industry_classification", {})
            if "industries" in industry_data:
                for industry, companies_list in industry_data["industries"].items():
                    print(f"   {industry}: {', '.join(companies_list)}")
            
            print("\n⚠️ Risk Assessment:")
            risk_data = ai_results.get("risk_assessment", {})
            if "risk_summary" in risk_data:
                risk_summary = risk_data["risk_summary"]
                print(f"   Overall Risk Level: {risk_summary.get('overall_risk_level', 'Unknown').upper()}")
                print(f"   Key Concerns: {', '.join(risk_summary.get('key_concerns', []))}")
            
            print("\n📈 Market Insights:")
            market_data = ai_results.get("market_insights", {})
            trends = market_data.get("market_trends", [])
            if trends:
                for trend in trends[:3]:  # Show first 3 trends
                    print(f"   • {trend.get('trend', 'Unknown')}: {trend.get('impact', 'Unknown')} impact")
            
            print("\n💡 Recommendations:")
            rec_data = ai_results.get("recommendations", {})
            recommendations = rec_data.get("strategic_recommendations", [])
            for rec in recommendations[:3]:  # Show first 3 recommendations
                print(f"   • {rec.get('recommendation', 'N/A')} (Priority: {rec.get('priority', 'Unknown')})")
            
            print("\n📋 Executive Summary:")
            print("-" * 40)
            print(executive_summary)
            
        else:
            print(f"❌ AI analysis failed: {ai_results['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_mcp_export():
    """Example 3: Export data for MCP integration"""
    print("\n🔗 Example 3: MCP Export Format")
    print("=" * 50)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not configured - showing basic MCP export")
        
        # Basic analyzer without AI
        from company_analyzer import CompanyAnalyzer
        analyzer = CompanyAnalyzer("LPATech.csv")
        
        # Simulate some analysis results for demo
        analyzer.companies = Counter({
            "Microsoft Corporation": 45,
            "Apple Inc": 32,
            "Google LLC": 25
        })
        
        # Export basic MCP format
        mcp_data = analyzer.export_for_mcp()
        
    else:
        # AI-enhanced MCP export
        try:
            analyzer = AIEnhancedCompanyAnalyzer("LPATech.csv", enable_ai=True)
            
            # For demo, simulate analysis results
            analyzer.companies = Counter({
                "Microsoft Corporation": 45,
                "Apple Inc": 32,
                "Google LLC": 25
            })
            
            # Export enhanced MCP format
            mcp_data = analyzer.export_for_mcp_ai()
            
        except Exception as e:
            print(f"Error creating AI analyzer: {e}")
            return
    
    # Display MCP export structure
    print("📦 MCP Export Structure:")
    print("-" * 30)
    
    # Show metadata
    metadata = mcp_data.get("metadata", {})
    print(f"Timestamp: {metadata.get('timestamp', 'N/A')}")
    print(f"Total Companies: {metadata.get('total_companies', 0)}")
    print(f"AI Enhanced: {metadata.get('ai_enhanced', False)}")
    
    # Show top companies
    companies = mcp_data.get("companies", [])
    print(f"\nTop Companies ({len(companies)}):")
    for i, company_data in enumerate(companies[:5], 1):
        name = company_data.get("name", "Unknown")
        frequency = company_data.get("frequency", 0)
        print(f"   {i}. {name} ({frequency} entries)")
    
    # Show AI analysis if available
    if "ai_analysis" in mcp_data:
        print("\n🤖 AI Analysis Available:")
        ai_analysis = mcp_data["ai_analysis"]
        print(f"   Model Used: {ai_analysis.get('model_used', 'Unknown')}")
        print(f"   Companies Analyzed: {ai_analysis.get('companies_analyzed', 0)}")
        
        if "industry_classification" in ai_analysis:
            industries = ai_analysis["industry_classification"].get("industries", {})
            print(f"   Industries Identified: {len(industries)}")
    
    # Save MCP export for demonstration
    output_file = "mcp_export_example.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mcp_data, f, indent=2, default=str)
    
    print(f"\n💾 MCP export saved to: {output_file}")


def example_interactive_ai():
    """Example 4: Interactive AI analysis session"""
    print("\n🎮 Example 4: Interactive AI Session")
    print("=" * 50)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not configured - interactive AI features require API key")
        return
    
    try:
        # Initialize analyzer
        analyzer = AIEnhancedCompanyAnalyzer("LPATech.csv", enable_ai=True)
        
        # For demo purposes, simulate analysis results
        print("🔍 Simulating analysis...")
        analyzer.companies = Counter({
            "Microsoft Corporation": 45,
            "Apple Inc": 32,
            "Amazon Web Services": 28,
            "Google LLC": 25,
            "Tesla Inc": 20
        })
        
        # Simulate AI results structure
        analyzer.ai_results = {
            "industry_classification": {
                "industries": {
                    "Technology": ["Microsoft Corporation", "Apple Inc", "Google LLC"],
                    "E-commerce": ["Amazon Web Services"],
                    "Automotive": ["Tesla Inc"]
                }
            },
            "risk_assessment": {
                "risk_summary": {
                    "overall_risk_level": "medium",
                    "key_concerns": ["market_concentration", "technology_disruption"]
                }
            }
        }
        
        analyzer.executive_summary = """
        EXECUTIVE SUMMARY
        
        Key Findings:
        • Technology sector dominance with 60% of companies
        • Medium risk profile with concentration concerns
        • Strong market positions across analyzed companies
        
        Recommendations:
        • Monitor technology sector concentration
        • Diversify across additional industries
        • Continue tracking market leaders
        """
        
        print("✅ Analysis simulation complete")
        print("\n🎯 Available AI Commands:")
        print("   • analyzer.print_ai_summary()")
        print("   • analyzer.get_industry_insights()")
        print("   • analyzer.get_risk_assessment()")
        print("   • analyzer.get_recommendations()")
        
        # Demonstrate AI summary
        analyzer.print_ai_summary()
        
        print("\n💡 To run full interactive session, use:")
        print("   analyzer.run_interactive_ai_search()")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_configuration():
    """Example 5: Configuration and environment setup"""
    print("\n⚙️ Example 5: Configuration Guide")
    print("=" * 50)
    
    print("📋 Required Environment Variables:")
    print("-" * 35)
    
    # Check configuration
    required_vars = [
        ("OPENAI_API_KEY", "OpenAI API key for AI analysis"),
        ("ANALYZER_ENABLE_AI", "Enable AI analysis features"),
        ("OPENAI_MODEL", "OpenAI model to use (optional)"),
        ("ANALYZER_ENABLE_MCP", "Enable MCP server (optional)")
    ]
    
    for var_name, description in required_vars:
        value = os.getenv(var_name)
        status = "✅ Set" if value else "❌ Not set"
        print(f"   {var_name}: {status}")
        print(f"      {description}")
        if value and var_name != "OPENAI_API_KEY":  # Don't show API key
            print(f"      Current value: {value}")
        print()
    
    print("🚀 Quick Setup Guide:")
    print("-" * 20)
    print("1. Copy .env.example to .env")
    print("2. Add your OpenAI API key")
    print("3. Set ANALYZER_ENABLE_AI=true")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Run analysis with AI features enabled")
    
    print("\n📖 For full configuration options, see:")
    print("   • .env.example - All available settings")
    print("   • AI_MCP_INTEGRATION.md - Complete integration guide")


def main():
    """Run all examples"""
    print("🏢 AI-Enhanced Company Analyzer Examples")
    print("=" * 60)
    
    # Check if CSV file exists for examples
    csv_file = "LPATech.csv"
    if not Path(csv_file).exists():
        print(f"⚠️  Note: Example CSV file '{csv_file}' not found.")
        print("Replace 'LPATech.csv' with your actual CSV file path in the examples.")
        print()
    
    # Run examples
    try:
        example_configuration()
        example_basic_ai_analysis()
        example_specific_ai_insights()
        example_mcp_export()
        example_interactive_ai()
        
        print("\n🎉 Examples completed!")
        print("\nNext steps:")
        print("• Configure your OpenAI API key")
        print("• Try the MCP server: python run_mcp_server.py")
        print("• Read the full guide: AI_MCP_INTEGRATION.md")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Examples failed: {e}")


if __name__ == "__main__":
    main() 