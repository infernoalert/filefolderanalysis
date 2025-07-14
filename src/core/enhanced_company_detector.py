"""
Enhanced Company Detection Module

This module uses advanced NLP techniques including spaCy NER, NLTK processing,
and sophisticated pattern matching to more accurately identify company names
while filtering out technical terms, version numbers, and system references.
"""

import re
import spacy
import nltk
from typing import List, Set, Optional, Dict, Any
from textblob import TextBlob
from collections import Counter
import logging
from ..config.config import config


class EnhancedCompanyDetector:
    """Enhanced company detection using NLP libraries"""
    
    def __init__(self):
        self.exclude_patterns = config.get_compiled_patterns()
        self.company_indicators = config.get_compiled_company_indicators()
        self.known_companies = config.known_companies
        self.exclude_words = config.exclude_words
        
        # Setup logging first
        self.logger = logging.getLogger(__name__)
        
        # Initialize NLP models
        self.nlp = None
        self.setup_nlp_models()
        
        # Enhanced technical patterns
        self.technical_patterns = [
            r'^\d+\.\d+\.\d+',  # Version numbers (4.5.1)
            r'.*\b(dev|repo|api|sdk|lib|framework|plugin|module|component)\b.*',  # Technical terms
            r'.*\b(database|server|client|config|settings|admin|system)\b.*',  # System terms
            r'.*\b(template|sample|example|test|demo|prototype)\b.*',  # Development terms
            r'.*\b(backup|archive|temp|tmp|cache|log|debug)\b.*',  # File system terms
            r'.*\b(v\d+|ver\d+|version\d+|release\d+|build\d+)\b.*',  # Version patterns
            r'.*\b(page|pages|document|file|folder|directory)\b.*',  # Document terms
            r'.*\b(internal|external|public|private|shared|common)\b.*',  # Access terms
            r'.*\b(old|new|legacy|current|latest|final|draft)\b.*',  # Status terms
            r'.*\b(part|section|chapter|appendix|index|table)\b.*',  # Document parts
        ]
        
        # Compile technical patterns
        self.compiled_technical_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.technical_patterns
        ]
        
        # Industry-specific technical terms
        self.technical_terms = {
            'dev', 'repo', 'api', 'sdk', 'framework', 'plugin', 'module', 'component',
            'database', 'server', 'client', 'config', 'settings', 'admin', 'system',
            'template', 'sample', 'example', 'test', 'demo', 'prototype', 'poc',
            'backup', 'archive', 'temp', 'tmp', 'cache', 'log', 'debug', 'error',
            'page', 'pages', 'document', 'file', 'folder', 'directory', 'path',
            'internal', 'external', 'public', 'private', 'shared', 'common',
            'old', 'new', 'legacy', 'current', 'latest', 'final', 'draft',
            'part', 'section', 'chapter', 'appendix', 'index', 'table',
            'plc', 'scada', 'hmi', 'dcs', 'mes', 'erp', 'crm', 'bi', 'etl'
        }
        
    def setup_nlp_models(self):
        """Initialize NLP models"""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("spaCy model loaded successfully")
            
            # Download NLTK data if needed
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
                
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords')
                
            try:
                nltk.data.find('taggers/averaged_perceptron_tagger')
            except LookupError:
                nltk.download('averaged_perceptron_tagger')
                
        except Exception as e:
            self.logger.warning(f"Could not load spaCy model: {e}")
            self.logger.warning("Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def analyze_with_spacy(self, text: str) -> Dict[str, Any]:
        """Analyze text using spaCy NER"""
        if not self.nlp:
            return {'entities': [], 'is_organization': False, 'confidence': 0.0}
        
        try:
            doc = self.nlp(text)
            entities = []
            is_organization = False
            
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'confidence': 0.8 if ent.label_ in ['ORG', 'PERSON', 'GPE'] else 0.5
                })
                
                # Check if it's recognized as an organization
                if ent.label_ in ['ORG', 'PERSON', 'GPE']:  # Organization, Person, Geopolitical entity
                    is_organization = True
            
            # Calculate confidence based on entity types
            confidence_scores = []
            for e in entities:
                conf = e.get('confidence', 0.0)
                if isinstance(conf, (int, float)):
                    confidence_scores.append(conf)
                else:
                    confidence_scores.append(0.0)
            
            return {
                'entities': entities,
                'is_organization': is_organization,
                'confidence': max(confidence_scores) if confidence_scores else 0.0
            }
            
        except Exception as e:
            self.logger.error(f"spaCy analysis failed: {e}")
            return {'entities': [], 'is_organization': False, 'confidence': 0.0}
    
    def analyze_with_nltk(self, text: str) -> Dict[str, Any]:
        """Analyze text using NLTK"""
        try:
            # Tokenize and tag
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            
            # Count proper nouns
            proper_nouns = [word for word, pos in pos_tags if pos in ['NNP', 'NNPS']]
            
            # Check for technical terms
            technical_count = sum(1 for word in tokens if word.lower() in self.technical_terms)
            
            return {
                'tokens': tokens,
                'pos_tags': pos_tags,
                'proper_nouns': proper_nouns,
                'proper_noun_ratio': len(proper_nouns) / len(tokens) if tokens else 0,
                'technical_count': technical_count,
                'technical_ratio': technical_count / len(tokens) if tokens else 0
            }
            
        except Exception as e:
            self.logger.error(f"NLTK analysis failed: {e}")
            return {
                'tokens': [],
                'pos_tags': [],
                'proper_nouns': [],
                'proper_noun_ratio': 0,
                'technical_count': 0,
                'technical_ratio': 0
            }
    
    def is_version_number(self, text: str) -> bool:
        """Check if text contains version numbers"""
        version_patterns = [
            r'^\d+\.\d+',  # 4.5, 1.0
            r'^\d+\.\d+\.\d+',  # 4.5.1, 1.0.0
            r'v\d+',  # v1, v2
            r'version\s*\d+',  # version 1
            r'rel\s*\d+',  # rel 1
            r'build\s*\d+',  # build 123
        ]
        
        for pattern in version_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def is_technical_reference(self, text: str) -> bool:
        """Check if text is a technical reference"""
        # Check against compiled technical patterns
        for pattern in self.compiled_technical_patterns:
            if pattern.match(text):
                return True
        
        # Check for multiple technical terms
        words = text.lower().split()
        technical_words = [w for w in words if w in self.technical_terms]
        
        # If more than 30% of words are technical terms, it's likely technical
        if len(words) > 0 and len(technical_words) / len(words) > 0.3:
            return True
        
        return False
    
    def is_document_structure(self, text: str) -> bool:
        """Check if text represents document structure"""
        structure_patterns = [
            r'^\d+\.\d+',  # 4.5, 1.2 (section numbers)
            r'chapter\s*\d+',
            r'section\s*\d+',
            r'part\s*\d+',
            r'appendix\s*[a-z]',
            r'page\s*\d+',
            r'table\s*\d+',
            r'figure\s*\d+',
        ]
        
        for pattern in structure_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def enhanced_company_detection(self, text: str) -> Dict[str, Any]:
        """Enhanced company detection using all available methods"""
        if not text or len(text) < 2:
            return {'is_company': False, 'confidence': 0.0, 'reasons': ['too_short']}
        
        text = str(text).strip()
        reasons = []
        confidence = 0.0
        
        # 1. Check against exclude patterns (original logic)
        if self.is_technical_file(text):
            return {'is_company': False, 'confidence': 0.0, 'reasons': ['technical_file']}
        
        # 2. Check for version numbers
        if self.is_version_number(text):
            reasons.append('version_number')
            return {'is_company': False, 'confidence': 0.0, 'reasons': reasons}
        
        # 3. Check for technical references
        if self.is_technical_reference(text):
            reasons.append('technical_reference')
            return {'is_company': False, 'confidence': 0.0, 'reasons': reasons}
        
        # 4. Check for document structure
        if self.is_document_structure(text):
            reasons.append('document_structure')
            return {'is_company': False, 'confidence': 0.0, 'reasons': reasons}
        
        # 5. Check if it's a known company
        if text in self.known_companies:
            return {'is_company': True, 'confidence': 1.0, 'reasons': ['known_company']}
        
        # 6. spaCy NER analysis
        spacy_result = self.analyze_with_spacy(text)
        if spacy_result['is_organization']:
            confidence += 0.4
            reasons.append('spacy_organization')
        
        # 7. NLTK analysis
        nltk_result = self.analyze_with_nltk(text)
        
        # High proper noun ratio suggests company name
        if nltk_result['proper_noun_ratio'] > 0.7:
            confidence += 0.3
            reasons.append('high_proper_nouns')
        
        # High technical ratio suggests not a company
        if nltk_result['technical_ratio'] > 0.3:
            confidence -= 0.4
            reasons.append('high_technical_terms')
        
        # 8. Traditional pattern matching
        for indicator in self.company_indicators:
            if indicator.search(text):
                confidence += 0.2
                reasons.append('company_indicator')
                break
        
        # 9. Structure analysis
        words = text.split()
        if len(words) >= 2:
            # Multiple capitalized words
            capitalized_words = [w for w in words if w and w[0].isupper() and w.isalpha()]
            if len(capitalized_words) >= 2 and len(capitalized_words) == len(words):
                confidence += 0.2
                reasons.append('multiple_capitalized')
        
        # 10. Single word analysis
        elif len(words) == 1:
            word = words[0]
            if (word[0].isupper() and 
                word.isalpha() and 
                3 <= len(word) <= config.max_company_name_length and
                word not in self.exclude_words):
                confidence += 0.1
                reasons.append('single_proper_noun')
        
        # Final decision
        is_company = confidence > 0.3
        
        return {
            'is_company': is_company,
            'confidence': min(confidence, 1.0),
            'reasons': reasons,
            'spacy_analysis': spacy_result,
            'nltk_analysis': nltk_result
        }
    
    def is_technical_file(self, name: str) -> bool:
        """Check if the name is a technical file (original logic)"""
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
        Main interface - determine if a name is likely a company
        Uses enhanced detection methods
        """
        result = self.enhanced_company_detection(name)
        return result['is_company']
    
    def get_detection_details(self, name: str) -> Dict[str, Any]:
        """Get detailed analysis of why something was/wasn't detected as a company"""
        return self.enhanced_company_detection(name)
    
    def clean_company_name(self, name: str) -> str:
        """Clean and standardize company names (original logic)"""
        if not name:
            return ""
        
        name = str(name).strip()
        
        # Remove common prefixes that aren't part of company names
        name = re.sub(r'^\d{4}\s+', '', name)  # Remove year prefixes
        name = re.sub(r'^(AU|US|UK|NZ)\s+', '', name)  # Remove country prefixes
        
        # Clean up spacing
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def batch_analyze(self, names: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple names at once"""
        results = []
        for name in names:
            result = self.enhanced_company_detection(name)
            result['name'] = name
            results.append(result)
        return results
    
    def get_analysis_summary(self, names: List[str]) -> Dict[str, Any]:
        """Get summary statistics of analysis results"""
        results = self.batch_analyze(names)
        
        companies = [r for r in results if r['is_company']]
        non_companies = [r for r in results if not r['is_company']]
        
        # Count reasons
        company_reasons = Counter()
        non_company_reasons = Counter()
        
        for r in companies:
            for reason in r['reasons']:
                company_reasons[reason] += 1
        
        for r in non_companies:
            for reason in r['reasons']:
                non_company_reasons[reason] += 1
        
        return {
            'total_analyzed': len(names),
            'companies_found': len(companies),
            'non_companies': len(non_companies),
            'company_percentage': len(companies) / len(names) * 100 if names else 0,
            'company_reasons': dict(company_reasons),
            'non_company_reasons': dict(non_company_reasons),
            'average_confidence': sum(r['confidence'] for r in results) / len(results) if results else 0
        }
    
    def add_known_company(self, company_name: str) -> None:
        """Add a company to the known companies list"""
        self.known_companies.add(company_name)
    
    def get_known_companies(self) -> Set[str]:
        """Get the set of known companies"""
        return self.known_companies.copy()
    
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