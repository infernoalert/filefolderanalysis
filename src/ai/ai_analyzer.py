"""
AI-Enhanced Company Analysis Module

This module integrates OpenAI ChatGPT with company analysis to provide:
- Industry classification and insights
- Business relationship analysis  
- Risk assessment and recommendations
- Competitive landscape analysis
- Market intelligence and trends
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter
import openai
from openai import AsyncOpenAI
import os
from datetime import datetime

from ..config.config import config


class AICompanyAnalyzer:
    """AI-enhanced company analysis using OpenAI ChatGPT"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer
        
        Args:
            api_key: OpenAI API key (uses environment variable if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # AI analysis settings
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.3'))
        self.max_companies_per_batch = int(os.getenv('AI_MAX_COMPANIES_BATCH', '20'))
        
        # Cache for AI responses to avoid duplicate API calls
        self.analysis_cache = {}
    
    async def analyze_companies(self, companies: Counter, company_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze companies using AI for enhanced insights
        
        Args:
            companies: Counter of company names and frequencies
            company_details: Detailed company information
            
        Returns:
            Dict with AI analysis results
        """
        try:
            self.logger.info("Starting AI-enhanced company analysis...")
            
            # Get top companies for analysis
            top_companies = companies.most_common(self.max_companies_per_batch)
            company_names = [name for name, _ in top_companies]
            
            # Perform different types of AI analysis
            analysis_results = {
                'timestamp': datetime.now().isoformat(),
                'model_used': self.model,
                'companies_analyzed': len(company_names),
                'industry_classification': await self._classify_industries(company_names),
                'business_relationships': await self._analyze_relationships(company_names),
                'risk_assessment': await self._assess_risks(company_names, company_details),
                'market_insights': await self._generate_market_insights(company_names),
                'recommendations': await self._generate_recommendations(company_names, companies)
            }
            
            self.logger.info(f"AI analysis completed for {len(company_names)} companies")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    async def _classify_industries(self, companies: List[str]) -> Dict[str, Any]:
        """Classify companies by industry using AI"""
        prompt = f"""
        Analyze the following list of company names and classify them by industry.
        Provide industry categories, confidence scores, and brief explanations.
        
        Companies: {', '.join(companies)}
        
        Return a JSON response with this structure:
        {{
            "industries": {{
                "Technology": ["company1", "company2"],
                "Healthcare": ["company3"],
                ...
            }},
            "analysis": {{
                "company1": {{
                    "industry": "Technology", 
                    "confidence": 0.95,
                    "reasoning": "Brief explanation"
                }},
                ...
            }},
            "industry_summary": {{
                "most_common": "Technology",
                "diversity_score": 0.8,
                "total_industries": 5
            }}
        }}
        """
        
        return await self._get_ai_response(prompt, "industry_classification")
    
    async def _analyze_relationships(self, companies: List[str]) -> Dict[str, Any]:
        """Analyze business relationships between companies"""
        prompt = f"""
        Analyze potential business relationships, partnerships, or competitive dynamics 
        between these companies: {', '.join(companies)}
        
        Consider:
        - Potential partnerships or collaborations
        - Competitive relationships
        - Supply chain connections
        - Market overlap
        
        Return JSON with:
        {{
            "partnerships": [
                {{"companies": ["A", "B"], "type": "strategic_alliance", "likelihood": 0.8}}
            ],
            "competitors": [
                {{"companies": ["C", "D"], "market": "enterprise_software", "intensity": "high"}}
            ],
            "supply_chain": [
                {{"supplier": "E", "customer": "F", "relationship_type": "vendor"}}
            ],
            "market_clusters": {{
                "fintech": ["company1", "company2"],
                "healthcare": ["company3"]
            }}
        }}
        """
        
        return await self._get_ai_response(prompt, "business_relationships")
    
    async def _assess_risks(self, companies: List[str], company_details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess business and compliance risks"""
        # Get frequency data for context
        frequency_context = {}
        for company in companies:
            if company in company_details:
                details = company_details[company]
                frequency_context[company] = {
                    'folder_count': details.get('count', 0),
                    'file_types': list(details.get('file_types', set())),
                    'paths': len(details.get('paths', set()))
                }
        
        prompt = f"""
        Assess potential business and compliance risks for these companies based on:
        1. Company names: {', '.join(companies)}
        2. Data presence context: {json.dumps(frequency_context, indent=2)}
        
        Consider:
        - Regulatory compliance risks
        - Data privacy concerns
        - Industry-specific risks
        - Concentration risks
        - Operational dependencies
        
        Return JSON:
        {{
            "risk_summary": {{
                "overall_risk_level": "medium",
                "key_concerns": ["data_concentration", "regulatory_compliance"]
            }},
            "company_risks": {{
                "company1": {{
                    "risk_level": "high",
                    "risk_factors": ["regulatory", "concentration"],
                    "recommendations": ["diversify_data", "compliance_review"]
                }}
            }},
            "systemic_risks": [
                {{"type": "concentration", "description": "High dependency on tech companies"}}
            ]
        }}
        """
        
        return await self._get_ai_response(prompt, "risk_assessment")
    
    async def _generate_market_insights(self, companies: List[str]) -> Dict[str, Any]:
        """Generate market insights and trends"""
        prompt = f"""
        Provide market insights and trends analysis for these companies: {', '.join(companies)}
        
        Analyze:
        - Current market trends affecting these companies
        - Growth opportunities
        - Technology disruptions
        - Economic factors
        - Competitive landscape changes
        
        Return JSON:
        {{
            "market_trends": [
                {{"trend": "AI adoption", "impact": "positive", "companies": ["tech_companies"]}}
            ],
            "growth_opportunities": [
                {{"opportunity": "cloud migration", "potential": "high", "timeframe": "2024-2025"}}
            ],
            "disruption_risks": [
                {{"disruption": "automation", "industries": ["manufacturing"], "timeline": "near-term"}}
            ],
            "economic_outlook": {{
                "overall": "positive",
                "key_factors": ["interest_rates", "digital_transformation"]
            }}
        }}
        """
        
        return await self._get_ai_response(prompt, "market_insights")
    
    async def _generate_recommendations(self, companies: List[str], companies_counter: Counter) -> Dict[str, Any]:
        """Generate strategic recommendations"""
        # Get top companies by frequency
        top_companies = companies_counter.most_common(10)
        
        prompt = f"""
        Based on this company analysis data, provide strategic recommendations:
        
        Top Companies by Data Presence: {top_companies}
        All Companies: {', '.join(companies)}
        
        Provide recommendations for:
        - Data management and organization
        - Business relationship optimization
        - Risk mitigation strategies
        - Growth opportunities
        - Technology investments
        
        Return JSON:
        {{
            "strategic_recommendations": [
                {{
                    "category": "data_management",
                    "recommendation": "Implement data governance",
                    "priority": "high",
                    "rationale": "Large volume of unstructured company data"
                }}
            ],
            "immediate_actions": [
                {{"action": "data_audit", "timeline": "30_days", "impact": "high"}}
            ],
            "long_term_initiatives": [
                {{"initiative": "ai_integration", "timeline": "6_months", "benefits": ["automation", "insights"]}}
            ]
        }}
        """
        
        return await self._get_ai_response(prompt, "recommendations")
    
    async def _get_ai_response(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get response from OpenAI with caching and error handling"""
        # Check cache first
        cache_key = f"{analysis_type}_{hash(prompt)}"
        if cache_key in self.analysis_cache:
            self.logger.info(f"Using cached response for {analysis_type}")
            return self.analysis_cache[cache_key]
        
        try:
            self.logger.info(f"Requesting AI analysis: {analysis_type}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a business analyst expert. Provide accurate, structured JSON responses with business insights."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Cache the response
            self.analysis_cache[cache_key] = result
            
            self.logger.info(f"AI analysis completed: {analysis_type}")
            return result
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AI response for {analysis_type}: {e}")
            return {"error": f"Invalid JSON response: {str(e)}", "raw_response": response.choices[0].message.content}
        
        except Exception as e:
            self.logger.error(f"AI request failed for {analysis_type}: {e}")
            return {"error": str(e), "type": analysis_type}
    
    async def generate_executive_summary(self, companies: Counter, ai_analysis: Dict[str, Any]) -> str:
        """Generate an executive summary of the analysis"""
        try:
            top_companies = companies.most_common(10)
            
            prompt = f"""
            Generate a comprehensive executive summary based on this company analysis:
            
            Top Companies: {top_companies}
            Total Unique Companies: {len(companies)}
            Total Data Points: {sum(companies.values())}
            
            AI Analysis Results: {json.dumps(ai_analysis, indent=2)}
            
            Create a professional executive summary covering:
            1. Key findings and insights
            2. Industry composition and trends
            3. Risk assessment and recommendations
            4. Strategic opportunities
            5. Next steps and action items
            
            Format as a clear, business-ready report suitable for executives.
            Use bullet points and clear sections.
            """
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an executive business consultant. Create clear, actionable executive summaries."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.2
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Failed to generate executive summary: {e}")
            return f"Executive Summary Generation Failed: {str(e)}"
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get statistics about AI analysis usage"""
        return {
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'cache_size': len(self.analysis_cache),
            'max_companies_per_batch': self.max_companies_per_batch
        }
    
    def clear_cache(self) -> None:
        """Clear the analysis cache"""
        self.analysis_cache.clear()
        self.logger.info("AI analysis cache cleared") 