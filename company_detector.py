"""
Company Detection Module

This module contains the logic for detecting and validating company names
from text data. It uses pattern matching and heuristics to identify
legitimate company names while filtering out technical files and noise.
"""

import re
from typing import List, Set, Optional
from config import config


class CompanyDetector:
    """Handles company name detection and validation"""
    
    def __init__(self):
        self.exclude_patterns = config.get_compiled_patterns()
        self.company_indicators = config.get_compiled_company_indicators()
        self.known_companies = config.known_companies
        self.exclude_words = config.exclude_words
        
    def is_technical_file(self, name: str) -> bool:
        """Check if the name is a technical file that should be excluded"""
        if not name:
            return True
        
        name = str(name).strip()
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if pattern.match(name):
                return True
        
        return False
    
    def is_likely_company(self, name: str) -> bool:
        """
        Determine if a name is likely a company name using improved logic
        
        Args:
            name: The name to check
            
        Returns:
            bool: True if likely a company name, False otherwise
        """
        if not name or len(name) < config.min_company_name_length:
            return False
        
        name = str(name).strip()
        
        # Skip if it's a technical file
        if self.is_technical_file(name):
            return False
        
        # Check if it's a known company
        if name in self.known_companies:
            return True
        
        # Check for company indicators
        for indicator in self.company_indicators:
            if indicator.search(name):
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
                3 <= len(word) <= config.max_company_name_length and
                word not in self.exclude_words):
                return True
        
        return False
    
    def clean_company_name(self, name: str) -> str:
        """
        Clean and standardize company names
        
        Args:
            name: The raw company name
            
        Returns:
            str: Cleaned company name
        """
        if not name:
            return ""
        
        name = str(name).strip()
        
        # Remove common prefixes that aren't part of company names
        name = re.sub(r'^\d{4}\s+', '', name)  # Remove year prefixes
        name = re.sub(r'^(AU|US|UK|NZ)\s+', '', name)  # Remove country prefixes
        
        # Clean up spacing
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def detect_companies_from_text(self, text: str) -> List[str]:
        """
        Detect company names from a given text
        
        Args:
            text: The text to analyze
            
        Returns:
            List[str]: List of detected company names
        """
        companies = []
        
        # Split text into potential company names
        # This is a basic implementation - can be enhanced
        potential_names = [text]  # Start with the full text
        
        # Also try splitting by common delimiters
        for delimiter in [' - ', ' / ', ' | ', ' & ']:
            if delimiter in text:
                potential_names.extend(text.split(delimiter))
        
        for name in potential_names:
            cleaned_name = self.clean_company_name(name)
            if self.is_likely_company(cleaned_name):
                companies.append(cleaned_name)
        
        return companies
    
    def validate_company_name(self, name: str) -> bool:
        """
        Validate if a given name is a valid company name
        
        Args:
            name: The name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not name:
            return False
        
        name = name.strip()
        
        # Length checks
        if len(name) < config.min_company_name_length or len(name) > config.max_company_name_length:
            return False
        
        # Basic validation
        if not name[0].isupper():
            return False
        
        # Check against exclude words
        if name in self.exclude_words:
            return False
        
        return True
    
    def add_known_company(self, company_name: str) -> None:
        """Add a company to the known companies list"""
        self.known_companies.add(company_name)
    
    def get_known_companies(self) -> Set[str]:
        """Get the set of known companies"""
        return self.known_companies.copy() 