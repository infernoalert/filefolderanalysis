"""
AI-Enhanced Company Analyzer

This module extends the basic CompanyAnalyzer with AI capabilities
for advanced business insights and analysis using OpenAI ChatGPT.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter
import os

from ..core.company_analyzer import CompanyAnalyzer
from .ai_analyzer import AICompanyAnalyzer
from ..config.config import config


class AIEnhancedCompanyAnalyzer(CompanyAnalyzer):
    """Company analyzer with AI-enhanced analysis capabilities"""
    
    def __init__(self, csv_file_path: Optional[str] = None, chunk_size: Optional[int] = None, 
                 filter_type: Optional[str] = None, enable_ai: Optional[bool] = None):
        """
        Initialize AI-enhanced company analyzer
        
        Args:
            csv_file_path: Path to the CSV file to analyze
            chunk_size: Size of chunks for processing
            filter_type: Type of items to analyze ('all', 'folders', 'files')
            enable_ai: Enable AI analysis (default from config)
        """
        # Initialize base analyzer
        super().__init__(csv_file_path, chunk_size, filter_type)
        
        # AI settings
        self.enable_ai = enable_ai if enable_ai is not None else config.enable_ai_analysis
        self.ai_analyzer = None
        self.ai_results = None
        self.executive_summary = None
        
        # Initialize AI analyzer if enabled and API key available
        if self.enable_ai and config.openai_api_key:
            try:
                self.ai_analyzer = AICompanyAnalyzer(config.openai_api_key)
                self.logger.info("AI analyzer initialized - AI analysis enabled")
            except Exception as e:
                self.logger.warning(f"AI analyzer initialization failed: {e}")
                self.enable_ai = False
        elif self.enable_ai and not config.openai_api_key:
            self.logger.warning("AI analysis requested but OpenAI API key not configured")
            self.enable_ai = False
        else:
            self.logger.info("AI analysis disabled")
    
    def analyze(self) -> bool:
        """
        Run the complete analysis process including AI analysis
        
        Returns:
            bool: True if analysis completed successfully, False otherwise
        """
        # Run basic analysis first
        success = super().analyze()
        
        if not success:
            return False
        
        # Run AI analysis if enabled
        if self.enable_ai and self.ai_analyzer:
            try:
                self.logger.info("Starting AI-enhanced analysis...")
                
                # Run AI analysis asynchronously
                self.ai_results = asyncio.run(
                    self.ai_analyzer.analyze_companies(self.companies, self.company_details)
                )
                
                # Generate executive summary
                self.executive_summary = asyncio.run(
                    self.ai_analyzer.generate_executive_summary(self.companies, self.ai_results)
                )
                
                self.logger.info("AI analysis completed successfully")
                
            except Exception as e:
                self.logger.error(f"AI analysis failed: {e}")
                self.ai_results = {"error": str(e)}
                self.executive_summary = f"AI analysis failed: {str(e)}"
        
        return True
    
    def get_ai_analysis_stats(self) -> Dict[str, Any]:
        """
        Get AI analysis statistics
        
        Returns:
            Dictionary with AI analysis statistics
        """
        if not self.ai_analyzer:
            return {"ai_enabled": False, "reason": "AI analyzer not initialized"}
        
        return {
            "ai_enabled": True,
            "ai_stats": self.ai_analyzer.get_analysis_stats(),
            "analysis_completed": self.ai_results is not None,
            "summary_generated": self.executive_summary is not None
        }
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis statistics including AI insights
        
        Returns:
            Dictionary with complete analysis statistics
        """
        # Get base stats
        stats = super().get_analysis_stats()
        
        # Add AI stats
        ai_stats = self.get_ai_analysis_stats()
        stats.update(ai_stats)
        
        # Add AI results summary if available
        if self.ai_results and "error" not in self.ai_results:
            stats["ai_insights_summary"] = {
                "industries_analyzed": len(self.ai_results.get("industry_classification", {}).get("industries", {})),
                "companies_analyzed": self.ai_results.get("companies_analyzed", 0),
                "risk_level": self.ai_results.get("risk_assessment", {}).get("risk_summary", {}).get("overall_risk_level", "unknown"),
                "market_trends_identified": len(self.ai_results.get("market_insights", {}).get("market_trends", [])),
                "recommendations_count": len(self.ai_results.get("recommendations", {}).get("strategic_recommendations", []))
            }
        
        return stats
    
    def export_for_mcp_ai(self) -> Dict[str, Any]:
        """
        Export results in enhanced MCP format with AI insights
        
        Returns:
            Dictionary formatted for MCP with AI enhancement
        """
        # Get base MCP export
        mcp_data = super().export_for_mcp()
        
        # Add AI analysis results
        if self.ai_results:
            mcp_data["ai_analysis"] = self.ai_results
        
        if self.executive_summary:
            mcp_data["executive_summary"] = self.executive_summary
        
        # Add AI metadata
        mcp_data["metadata"]["ai_enhanced"] = self.enable_ai
        mcp_data["metadata"]["ai_analysis_status"] = "completed" if self.ai_results else "not_run"
        
        return mcp_data
    
    def get_industry_insights(self) -> Dict[str, Any]:
        """
        Get industry classification insights from AI analysis
        
        Returns:
            Dictionary with industry insights or empty if not available
        """
        if not self.ai_results or "industry_classification" not in self.ai_results:
            return {}
        
        return self.ai_results["industry_classification"]
    
    def get_risk_assessment(self) -> Dict[str, Any]:
        """
        Get risk assessment insights from AI analysis
        
        Returns:
            Dictionary with risk assessment or empty if not available
        """
        if not self.ai_results or "risk_assessment" not in self.ai_results:
            return {}
        
        return self.ai_results["risk_assessment"]
    
    def get_business_relationships(self) -> Dict[str, Any]:
        """
        Get business relationship insights from AI analysis
        
        Returns:
            Dictionary with relationship analysis or empty if not available
        """
        if not self.ai_results or "business_relationships" not in self.ai_results:
            return {}
        
        return self.ai_results["business_relationships"]
    
    def get_market_insights(self) -> Dict[str, Any]:
        """
        Get market insights from AI analysis
        
        Returns:
            Dictionary with market insights or empty if not available
        """
        if not self.ai_results or "market_insights" not in self.ai_results:
            return {}
        
        return self.ai_results["market_insights"]
    
    def get_recommendations(self) -> Dict[str, Any]:
        """
        Get strategic recommendations from AI analysis
        
        Returns:
            Dictionary with recommendations or empty if not available
        """
        if not self.ai_results or "recommendations" not in self.ai_results:
            return {}
        
        return self.ai_results["recommendations"]
    
    def print_ai_summary(self):
        """Print a summary of AI analysis results"""
        if not self.enable_ai:
            print("\n🤖 AI Analysis: Disabled")
            return
        
        if not self.ai_results:
            print("\n🤖 AI Analysis: Not completed")
            return
        
        if "error" in self.ai_results:
            print(f"\n🤖 AI Analysis: Failed - {self.ai_results['error']}")
            return
        
        print("\n" + "="*80)
        print("🤖 AI-ENHANCED ANALYSIS SUMMARY")
        print("="*80)
        
        # Industry insights
        industry_data = self.get_industry_insights()
        if industry_data and "industry_summary" in industry_data:
            summary = industry_data["industry_summary"]
            print(f"Most Common Industry: {summary.get('most_common', 'Unknown')}")
            print(f"Industry Diversity Score: {summary.get('diversity_score', 0):.2f}")
            print(f"Total Industries: {summary.get('total_industries', 0)}")
        
        # Risk assessment
        risk_data = self.get_risk_assessment()
        if risk_data and "risk_summary" in risk_data:
            risk_summary = risk_data["risk_summary"]
            print(f"Overall Risk Level: {risk_summary.get('overall_risk_level', 'Unknown').upper()}")
            concerns = risk_summary.get('key_concerns', [])
            if concerns:
                print(f"Key Concerns: {', '.join(concerns[:3])}")
        
        # Market insights
        market_data = self.get_market_insights()
        if market_data and "market_trends" in market_data:
            trends = market_data["market_trends"]
            print(f"Market Trends Identified: {len(trends)}")
            if trends:
                print(f"Top Trend: {trends[0].get('trend', 'Unknown')}")
        
        # Recommendations
        rec_data = self.get_recommendations()
        if rec_data and "strategic_recommendations" in rec_data:
            recommendations = rec_data["strategic_recommendations"]
            print(f"Strategic Recommendations: {len(recommendations)}")
            if recommendations:
                high_priority = [r for r in recommendations if r.get('priority') == 'high']
                print(f"High Priority Actions: {len(high_priority)}")
        
        print("\n📋 Executive Summary Available: Yes" if self.executive_summary else "\n📋 Executive Summary: Not generated")
        print("="*80)
    
    def save_ai_results(self, output_directory: str = "output") -> List[str]:
        """
        Save AI analysis results to files
        
        Args:
            output_directory: Directory to save files
            
        Returns:
            List of created file paths
        """
        if not self.ai_results:
            self.logger.warning("No AI results to save")
            return []
        
        from pathlib import Path
        import json
        
        output_dir = Path(output_directory)
        output_dir.mkdir(exist_ok=True)
        
        created_files = []
        timestamp = self.results_manager.timestamp
        
        try:
            # Save AI analysis results
            if "error" not in self.ai_results:
                ai_file = output_dir / f"ai_analysis_{timestamp}.json"
                with open(ai_file, 'w', encoding='utf-8') as f:
                    json.dump(self.ai_results, f, indent=2, default=str)
                created_files.append(str(ai_file))
            
            # Save executive summary
            if self.executive_summary:
                summary_file = output_dir / f"executive_summary_{timestamp}.txt"
                with open(summary_file, 'w', encoding='utf-8') as f:
                    f.write(self.executive_summary)
                created_files.append(str(summary_file))
            
            # Save enhanced MCP export
            mcp_file = output_dir / f"mcp_enhanced_{timestamp}.json"
            with open(mcp_file, 'w', encoding='utf-8') as f:
                json.dump(self.export_for_mcp_ai(), f, indent=2, default=str)
            created_files.append(str(mcp_file))
            
            self.logger.info(f"AI results saved to {len(created_files)} files")
            
        except Exception as e:
            self.logger.error(f"Error saving AI results: {e}")
        
        return created_files
    
    def run_interactive_ai_search(self):
        """Run an interactive search session with AI insights"""
        # Run base interactive search first
        super().run_interactive_search()
        
        # Add AI-specific commands if available
        if not self.ai_results or "error" in self.ai_results:
            return
        
        print("\n" + "="*60)
        print("🤖 AI ANALYSIS COMMANDS")
        print("="*60)
        print("Available AI commands:")
        print("  'ai summary' - Show AI analysis summary")
        print("  'ai industry' - Show industry classification")
        print("  'ai risk' - Show risk assessment")
        print("  'ai market' - Show market insights")
        print("  'ai recommendations' - Show strategic recommendations")
        print("  'ai executive' - Show executive summary")
        print("Type 'quit' to exit")
        print()
        
        while True:
            try:
                query = input("AI Analysis > ").strip().lower()
                
                if query in ['quit', 'exit', 'q']:
                    break
                
                if query == 'ai summary':
                    self.print_ai_summary()
                elif query == 'ai industry':
                    industry_data = self.get_industry_insights()
                    print(json.dumps(industry_data, indent=2, default=str))
                elif query == 'ai risk':
                    risk_data = self.get_risk_assessment()
                    print(json.dumps(risk_data, indent=2, default=str))
                elif query == 'ai market':
                    market_data = self.get_market_insights()
                    print(json.dumps(market_data, indent=2, default=str))
                elif query == 'ai recommendations':
                    rec_data = self.get_recommendations()
                    print(json.dumps(rec_data, indent=2, default=str))
                elif query == 'ai executive':
                    if self.executive_summary:
                        print("\n" + "="*60)
                        print("EXECUTIVE SUMMARY")
                        print("="*60)
                        print(self.executive_summary)
                        print("="*60)
                    else:
                        print("Executive summary not available")
                else:
                    print("Unknown AI command. Type 'quit' to exit.")
                
                print()
                
            except KeyboardInterrupt:
                print("\nExiting AI analysis...")
                break 