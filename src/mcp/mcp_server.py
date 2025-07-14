"""
MCP Server for Company Analysis

This module implements a Model Context Protocol server that exposes
company analysis functionality for integration with AI assistants
and other MCP-compatible tools.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

from ..core.company_analyzer import CompanyAnalyzer
from ..ai.ai_analyzer import AICompanyAnalyzer
from ..config.config import AnalyzerConfig


# Pydantic models for API requests/responses
class AnalysisRequest(BaseModel):
    csv_file_path: str
    chunk_size: Optional[int] = None
    filter_type: Optional[str] = "all"
    enable_ai_analysis: Optional[bool] = True
    ai_model: Optional[str] = "gpt-3.5-turbo"


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    timestamp: str
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CompanySearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10


class AIInsightRequest(BaseModel):
    companies: List[str]
    analysis_type: Optional[str] = "comprehensive"


class MCPCompanyAnalysisServer:
    """MCP server for company analysis with AI integration"""
    
    def __init__(self, config: Optional[AnalyzerConfig] = None):
        """Initialize MCP server"""
        self.config = config or AnalyzerConfig()
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format=self.config.log_format
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="Company Analysis MCP Server",
            description="Model Context Protocol server for AI-enhanced company analysis",
            version="1.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure as needed for security
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Analysis results storage (in production, use proper database)
        self.analysis_results = {}
        self.analysis_counter = 0
        
        # Initialize AI analyzer if API key is available
        self.ai_analyzer = None
        try:
            if os.getenv('OPENAI_API_KEY'):
                self.ai_analyzer = AICompanyAnalyzer()
                self.logger.info("AI analyzer initialized successfully")
            else:
                self.logger.warning("OpenAI API key not found - AI features disabled")
        except Exception as e:
            self.logger.warning(f"AI analyzer initialization failed: {e}")
        
        # Setup API routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes for MCP endpoints"""
        
        @self.app.get("/")
        async def root():
            """Root endpoint with server information"""
            return {
                "service": "Company Analysis MCP Server",
                "version": "1.0.0",
                "status": "operational",
                "features": {
                    "company_detection": True,
                    "ai_analysis": self.ai_analyzer is not None,
                    "enhanced_nlp": True,
                    "batch_processing": True
                },
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "config_loaded": self.config is not None,
                "ai_enabled": self.ai_analyzer is not None
            }
        
        @self.app.post("/analyze", response_model=AnalysisResponse)
        async def analyze_companies(request: AnalysisRequest, background_tasks: BackgroundTasks):
            """Start company analysis"""
            try:
                # Validate file exists
                if not Path(request.csv_file_path).exists():
                    raise HTTPException(status_code=404, detail=f"CSV file not found: {request.csv_file_path}")
                
                # Generate analysis ID
                self.analysis_counter += 1
                analysis_id = f"analysis_{self.analysis_counter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Initialize analysis result
                self.analysis_results[analysis_id] = {
                    "status": "running",
                    "timestamp": datetime.now().isoformat(),
                    "request": request.dict()
                }
                
                # Start analysis in background
                background_tasks.add_task(
                    self._run_analysis,
                    analysis_id,
                    request
                )
                
                return AnalysisResponse(
                    analysis_id=analysis_id,
                    status="started",
                    timestamp=datetime.now().isoformat()
                )
                
            except Exception as e:
                self.logger.error(f"Analysis request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
        async def get_analysis_result(analysis_id: str):
            """Get analysis results"""
            if analysis_id not in self.analysis_results:
                raise HTTPException(status_code=404, detail="Analysis not found")
            
            result = self.analysis_results[analysis_id]
            return AnalysisResponse(
                analysis_id=analysis_id,
                status=result["status"],
                timestamp=result["timestamp"],
                results=result.get("results"),
                error=result.get("error")
            )
        
        @self.app.get("/analyses")
        async def list_analyses():
            """List all analyses"""
            return {
                "analyses": [
                    {
                        "analysis_id": aid,
                        "status": result["status"],
                        "timestamp": result["timestamp"]
                    }
                    for aid, result in self.analysis_results.items()
                ],
                "total": len(self.analysis_results)
            }
        
        @self.app.post("/search")
        async def search_companies(request: CompanySearchRequest):
            """Search companies across all analyses"""
            results = []
            
            for analysis_id, analysis in self.analysis_results.items():
                if analysis["status"] == "completed" and "results" in analysis:
                    companies = analysis["results"].get("companies", {})
                    for company, count in companies.items():
                        if request.query.lower() in company.lower():
                            results.append({
                                "company": company,
                                "count": count,
                                "analysis_id": analysis_id,
                                "timestamp": analysis["timestamp"]
                            })
            
            # Sort by count descending
            results.sort(key=lambda x: x["count"], reverse=True)
            
            return {
                "query": request.query,
                "results": results[:request.max_results],
                "total_found": len(results)
            }
        
        @self.app.post("/ai/insights")
        async def get_ai_insights(request: AIInsightRequest):
            """Get AI insights for specific companies"""
            if not self.ai_analyzer:
                raise HTTPException(status_code=503, detail="AI analysis not available - OpenAI API key required")
            
            try:
                # Create a mock Counter and details for the AI analysis
                from collections import Counter
                companies_counter = Counter({company: 1 for company in request.companies})
                company_details = {}
                
                # Run AI analysis
                ai_results = await self.ai_analyzer.analyze_companies(companies_counter, company_details)
                
                # Generate executive summary
                executive_summary = await self.ai_analyzer.generate_executive_summary(companies_counter, ai_results)
                
                return {
                    "companies": request.companies,
                    "analysis_type": request.analysis_type,
                    "ai_insights": ai_results,
                    "executive_summary": executive_summary,
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                self.logger.error(f"AI insights request failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/ai/stats")
        async def get_ai_stats():
            """Get AI analysis statistics"""
            if not self.ai_analyzer:
                return {"ai_enabled": False, "reason": "OpenAI API key not configured"}
            
            return {
                "ai_enabled": True,
                "stats": self.ai_analyzer.get_analysis_stats(),
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.delete("/analysis/{analysis_id}")
        async def delete_analysis(analysis_id: str):
            """Delete analysis results"""
            if analysis_id not in self.analysis_results:
                raise HTTPException(status_code=404, detail="Analysis not found")
            
            del self.analysis_results[analysis_id]
            return {"message": f"Analysis {analysis_id} deleted successfully"}
        
        @self.app.post("/config/reload")
        async def reload_config():
            """Reload configuration"""
            try:
                self.config.reload()
                return {
                    "message": "Configuration reloaded successfully",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Config reload failed: {str(e)}")
    
    async def _run_analysis(self, analysis_id: str, request: AnalysisRequest):
        """Run company analysis in background"""
        try:
            self.logger.info(f"Starting analysis {analysis_id}")
            
            # Initialize analyzer
            analyzer = CompanyAnalyzer(
                csv_file_path=request.csv_file_path,
                chunk_size=request.chunk_size or self.config.chunk_size,
                filter_type=request.filter_type or "all"
            )
            
            # Run analysis
            success = analyzer.analyze()
            
            if not success:
                self.analysis_results[analysis_id].update({
                    "status": "failed",
                    "error": "Company analysis failed"
                })
                return
            
            # Get basic results
            results = {
                "companies": dict(analyzer.companies.most_common()),
                "statistics": analyzer.get_analysis_stats(),
                "mcp_export": analyzer.export_for_mcp()
            }
            
            # Add AI analysis if enabled and available
            if request.enable_ai_analysis and self.ai_analyzer:
                try:
                    self.logger.info(f"Running AI analysis for {analysis_id}")
                    ai_results = await self.ai_analyzer.analyze_companies(
                        analyzer.companies, 
                        analyzer.company_details
                    )
                    
                    # Generate executive summary
                    executive_summary = await self.ai_analyzer.generate_executive_summary(
                        analyzer.companies, 
                        ai_results
                    )
                    
                    results.update({
                        "ai_analysis": ai_results,
                        "executive_summary": executive_summary
                    })
                    
                except Exception as e:
                    self.logger.error(f"AI analysis failed for {analysis_id}: {e}")
                    results["ai_analysis_error"] = str(e)
            
            # Update results
            self.analysis_results[analysis_id].update({
                "status": "completed",
                "results": results,
                "completion_time": datetime.now().isoformat()
            })
            
            self.logger.info(f"Analysis {analysis_id} completed successfully")
            
        except Exception as e:
            self.logger.error(f"Analysis {analysis_id} failed: {e}")
            self.analysis_results[analysis_id].update({
                "status": "failed",
                "error": str(e),
                "completion_time": datetime.now().isoformat()
            })
    
    def run_server(self, host: str = "0.0.0.0", port: int = 8005):
        """Run the MCP server"""
        self.logger.info(f"Starting MCP server on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


# MCP Tools for external integration
class MCPTools:
    """Tools for MCP integration with external systems"""
    
    @staticmethod
    def get_tools() -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        return [
            {
                "name": "analyze_companies",
                "description": "Analyze CSV file to extract and classify company names with AI insights",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "csv_file_path": {
                            "type": "string",
                            "description": "Path to the CSV file to analyze"
                        },
                        "filter_type": {
                            "type": "string",
                            "enum": ["all", "folders", "files"],
                            "description": "Type of items to analyze"
                        },
                        "enable_ai_analysis": {
                            "type": "boolean",
                            "description": "Enable AI-enhanced analysis with ChatGPT"
                        }
                    },
                    "required": ["csv_file_path"]
                }
            },
            {
                "name": "search_companies",
                "description": "Search for companies across analysis results",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for company names"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_ai_insights",
                "description": "Get AI-powered business insights for specific companies",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "companies": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of company names to analyze"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["comprehensive", "industry", "risk", "market"],
                            "description": "Type of analysis to perform"
                        }
                    },
                    "required": ["companies"]
                }
            }
        ]


# Main entry point
async def main():
    """Main entry point for MCP server"""
    # Load configuration
    config = AnalyzerConfig()
    
    # Initialize and run MCP server
    server = MCPCompanyAnalysisServer(config)
    server.run_server()


if __name__ == "__main__":
    asyncio.run(main()) 