"""
Manual AI Analysis Module

This module provides AI-powered analysis for manually selected terms/phrases
that may contain company names. It uses configurable JSON templates to define
different types of analysis.
"""

import json
import asyncio
import logging
from typing import List, Dict, Any, Optional
from collections import Counter
from datetime import datetime
import openai
from pathlib import Path


class ManualAIAnalyzer:
    """
    AI analyzer for manually selected terms/phrases
    
    This class provides AI-powered analysis for terms that users manually
    select as potentially containing company names.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the manual AI analyzer
        
        Args:
            api_key: OpenAI API key (if not provided, will use environment variable)
        """
        self.logger = logging.getLogger(__name__)
        
        # Setup OpenAI client
        if api_key:
            self.client = openai.AsyncOpenAI(api_key=api_key)
        else:
            self.client = openai.AsyncOpenAI()
        
        # Analysis cache
        self.analysis_cache = {}
        
        # Load available configurations
        self.configs_dir = Path("ai_analysis_configs")
        self.available_configs = self._load_available_configs()
    
    def _load_available_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load all available AI analysis configurations"""
        configs = {}
        
        if self.configs_dir.exists():
            for config_file in self.configs_dir.glob("*.json"):
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        configs[config_file.stem] = config
                except Exception as e:
                    self.logger.error(f"Failed to load config {config_file}: {e}")
        
        return configs
    
    def get_available_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get all available analysis configurations"""
        return self.available_configs
    
    async def analyze_manual_selection(
        self, 
        selected_terms: List[str], 
        config_name: str,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze manually selected terms using specified configuration
        
        Args:
            selected_terms: List of terms/phrases to analyze
            config_name: Name of the configuration to use
            custom_prompt: Optional custom prompt to override config
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Validate configuration
            if config_name not in self.available_configs:
                raise ValueError(f"Configuration '{config_name}' not found")
            
            config = self.available_configs[config_name]
            
            # Prepare prompt
            if custom_prompt:
                prompt = custom_prompt.format(terms=", ".join(selected_terms))
            else:
                prompt = config["prompt_template"].format(terms=", ".join(selected_terms))
            
            # Get AI response
            response = await self._get_ai_response(prompt, config)
            
            # Process and validate response
            processed_results = self._process_ai_response(response, config, selected_terms)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'config_used': config_name,
                'terms_analyzed': len(selected_terms),
                'analysis_results': processed_results,
                'summary': self._generate_summary(processed_results, config),
                'status': 'success'
            }
            
        except Exception as e:
            self.logger.error(f"Manual AI analysis failed: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    async def _get_ai_response(self, prompt: str, config: Dict[str, Any]) -> str:
        """Get response from OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=config.get("openai_model", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "You are a business analysis expert. Provide accurate, detailed analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.get("max_tokens", 2000),
                temperature=config.get("temperature", 0.3)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _process_ai_response(self, response: str, config: Dict[str, Any], original_terms: List[str]) -> List[Dict[str, Any]]:
        """Process and validate AI response"""
        try:
            # Try to parse JSON response
            if response.strip().startswith('['):
                results = json.loads(response)
            elif response.strip().startswith('{'):
                # Single object response
                results = [json.loads(response)]
            else:
                # Try to extract JSON from text
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    results = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse JSON response")
            
            # Validate results
            validated_results = []
            for result in results:
                if self._validate_result(result, config):
                    validated_results.append(result)
            
            return validated_results
            
        except Exception as e:
            self.logger.error(f"Failed to process AI response: {e}")
            return []
    
    def _validate_result(self, result: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Validate a single analysis result"""
        validation_rules = config.get("validation_rules", {})
        required_fields = validation_rules.get("required_fields", [])
        
        # Check required fields
        for field in required_fields:
            if field not in result:
                return False
        
        # Check confidence threshold
        min_confidence = validation_rules.get("min_confidence", 0.0)
        if "confidence_score" in result:
            if result["confidence_score"] < min_confidence:
                return False
        
        return True
    
    def _generate_summary(self, results: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics from analysis results"""
        if not results:
            return {"error": "No valid results to summarize"}
        
        summary = {
            "total_analyzed": len(results),
            "valid_results": len(results),
            "config_name": config.get("name", "Unknown"),
            "analysis_type": config.get("analysis_type", "Unknown")
        }
        
        # Add confidence statistics
        confidence_scores = [r.get("confidence_score", 0) for r in results if "confidence_score" in r]
        if confidence_scores:
            summary["confidence_stats"] = {
                "average": sum(confidence_scores) / len(confidence_scores),
                "min": min(confidence_scores),
                "max": max(confidence_scores)
            }
        
        # Add industry statistics if available
        industries = [r.get("primary_industry", r.get("industry", "Unknown")) for r in results]
        if industries:
            industry_counts = Counter(industries)
            summary["industry_distribution"] = dict(industry_counts.most_common(5))
        
        return summary
    
    def add_custom_config(self, config_name: str, config_data: Dict[str, Any]):
        """Add a custom analysis configuration"""
        self.available_configs[config_name] = config_data
        
        # Save to file
        config_file = self.configs_dir / f"{config_name}.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get statistics about the analyzer"""
        return {
            "available_configs": len(self.available_configs),
            "config_names": list(self.available_configs.keys()),
            "cache_size": len(self.analysis_cache)
        }
    
    def clear_cache(self):
        """Clear the analysis cache"""
        self.analysis_cache.clear() 