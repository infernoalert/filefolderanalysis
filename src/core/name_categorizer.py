"""
Name Categorization Module

This module provides intelligent categorization of detected names to distinguish
between actual companies and other entities like abbreviations, technical terms,
and document references. It provides descriptions for the offline analysis mode.
"""

import re
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import logging


class NameCategorizer:
    """
    Intelligent name categorization system for offline analysis
    
    This class analyzes detected names and provides descriptions about what
    they actually represent, helping users understand the analysis results.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common abbreviation patterns and their expansions
        self.common_abbreviations = {
            # Business/Legal
            'PROP & VAR': 'Proposal and Variation',
            'PROP VAR': 'Proposal and Variation',
            'PROP': 'Proposal',
            'VAR': 'Variation', 
            'P&V': 'Proposal and Variation',
            'T&C': 'Terms and Conditions',
            'T&CS': 'Terms and Conditions',
            'R&D': 'Research and Development',
            'P&L': 'Profit and Loss',
            'B&P': 'Business and Procurement',
            'HR': 'Human Resources',
            'IT': 'Information Technology',
            'QA': 'Quality Assurance',
            'QC': 'Quality Control',
            'PR': 'Public Relations',
            'CEO': 'Chief Executive Officer',
            'CTO': 'Chief Technology Officer',
            'CFO': 'Chief Financial Officer',
            'COO': 'Chief Operating Officer',
            'VP': 'Vice President',
            'GM': 'General Manager',
            'PM': 'Project Manager',
            'BA': 'Business Analyst',
            'SA': 'System Administrator',
            'DBA': 'Database Administrator',
            
            # Construction/Engineering
            'BIM': 'Building Information Modeling',
            'CAD': 'Computer-Aided Design',
            'MEP': 'Mechanical, Electrical, and Plumbing',
            'HVAC': 'Heating, Ventilation, and Air Conditioning',
            'QS': 'Quantity Surveying',
            'BOQ': 'Bill of Quantities',
            'RFI': 'Request for Information',
            'RFP': 'Request for Proposal',
            'RFQ': 'Request for Quote',
            'SOW': 'Statement of Work',
            'WBS': 'Work Breakdown Structure',
            'PO': 'Purchase Order',
            'SO': 'Sales Order',
            'DO': 'Delivery Order',
            'DN': 'Delivery Note',
            'GRN': 'Goods Received Note',
            'MTO': 'Material Take-Off',
            'IFC': 'Industry Foundation Classes',
            'DWG': 'Drawing',
            'PDF': 'Portable Document Format',
            'JPG': 'JPEG Image',
            'PNG': 'Portable Network Graphics',
            'DOC': 'Document',
            'XLS': 'Excel Spreadsheet',
            'PPT': 'PowerPoint Presentation',
            
            # Technical/IT
            'API': 'Application Programming Interface',
            'SDK': 'Software Development Kit',
            'IDE': 'Integrated Development Environment',
            'CRM': 'Customer Relationship Management',
            'ERP': 'Enterprise Resource Planning',
            'SCM': 'Supply Chain Management',
            'PLM': 'Product Lifecycle Management',
            'CMS': 'Content Management System',
            'LMS': 'Learning Management System',
            'DBMS': 'Database Management System',
            'OS': 'Operating System',
            'UI': 'User Interface',
            'UX': 'User Experience',
            'SQL': 'Structured Query Language',
            'XML': 'Extensible Markup Language',
            'JSON': 'JavaScript Object Notation',
            'CSV': 'Comma-Separated Values',
            'FTP': 'File Transfer Protocol',
            'HTTP': 'Hypertext Transfer Protocol',
            'HTTPS': 'Hypertext Transfer Protocol Secure',
            'URL': 'Uniform Resource Locator',
            'IP': 'Internet Protocol',
            'TCP': 'Transmission Control Protocol',
            'UDP': 'User Datagram Protocol',
            'DNS': 'Domain Name System',
            'VPN': 'Virtual Private Network',
            'LAN': 'Local Area Network',
            'WAN': 'Wide Area Network',
            'WIFI': 'Wireless Fidelity',
            'USB': 'Universal Serial Bus',
            'SSD': 'Solid State Drive',
            'HDD': 'Hard Disk Drive',
            'CPU': 'Central Processing Unit',
            'GPU': 'Graphics Processing Unit',
            'RAM': 'Random Access Memory',
            'ROM': 'Read-Only Memory',
            
            # Financial/Accounting
            'GST': 'Goods and Services Tax',
            'VAT': 'Value Added Tax',
            'POS': 'Point of Sale',
            'ROI': 'Return on Investment',
            'NPV': 'Net Present Value',
            'IRR': 'Internal Rate of Return',
            'EBITDA': 'Earnings Before Interest, Taxes, Depreciation, and Amortization',
            'CAPEX': 'Capital Expenditure',
            'OPEX': 'Operating Expenditure',
            'AP': 'Accounts Payable',
            'AR': 'Accounts Receivable',
            'GL': 'General Ledger',
            'COA': 'Chart of Accounts',
            'JE': 'Journal Entry',
            'TB': 'Trial Balance',
            'BS': 'Balance Sheet',
            'IS': 'Income Statement',
            'CF': 'Cash Flow',
            
            # Time/Date
            'YTD': 'Year to Date',
            'QTD': 'Quarter to Date',
            'MTD': 'Month to Date',
            'EOD': 'End of Day',
            'EOW': 'End of Week',
            'EOM': 'End of Month',
            'EOY': 'End of Year',
            'FY': 'Financial Year',
            'Q1': 'Quarter 1',
            'Q2': 'Quarter 2',
            'Q3': 'Quarter 3',
            'Q4': 'Quarter 4',
            
            # General Business
            'KPI': 'Key Performance Indicator',
            'SLA': 'Service Level Agreement',
            'NDA': 'Non-Disclosure Agreement',
            'MOU': 'Memorandum of Understanding',
            'LOI': 'Letter of Intent',
            'FAQ': 'Frequently Asked Questions',
            'SOP': 'Standard Operating Procedure',
            'WIP': 'Work in Progress',
            'ETA': 'Estimated Time of Arrival',
            'ETD': 'Estimated Time of Departure',
            'FYI': 'For Your Information',
            'ASAP': 'As Soon As Possible',
            'TBD': 'To Be Determined',
            'TBA': 'To Be Announced',
            'TBC': 'To Be Confirmed',
            'N/A': 'Not Applicable',
            'TBD': 'To Be Determined',
            
            # Location/Geography
            'HQ': 'Headquarters',
            'HO': 'Head Office',
            'BO': 'Branch Office',
            'RO': 'Regional Office',
            'USA': 'United States of America',
            'UK': 'United Kingdom',
            'UAE': 'United Arab Emirates',
            'KSA': 'Kingdom of Saudi Arabia',
            'EU': 'European Union',
            'APAC': 'Asia-Pacific',
            'EMEA': 'Europe, Middle East, and Africa',
            'LATAM': 'Latin America',
            'ANZ': 'Australia and New Zealand',
            'SEA': 'South East Asia',
            'MENA': 'Middle East and North Africa',
        }
        
        # Pattern-based categorization rules
        self.pattern_rules = [
            # Version numbers
            (r'v?\d+\.\d+(\.\d+)?', 'Version Number', 'Software or document version identifier'),
            (r'version\s+\d+', 'Version Number', 'Software or document version identifier'),
            (r'build\s+\d+', 'Build Number', 'Software build identifier'),
            (r'release\s+\d+', 'Release Number', 'Software release identifier'),
            
            # Document sections
            (r'section\s+\d+', 'Document Section', 'Document section reference'),
            (r'chapter\s+\d+', 'Document Chapter', 'Document chapter reference'),
            (r'page\s+\d+', 'Page Number', 'Document page reference'),
            (r'appendix\s+[a-z]', 'Document Appendix', 'Document appendix reference'),
            
            # File types
            (r'.*\.(pdf|doc|docx|xls|xlsx|ppt|pptx|txt|csv|xml|json)$', 'File Extension', 'Document or data file type'),
            (r'.*\.(jpg|jpeg|png|gif|bmp|tiff|svg)$', 'Image File', 'Image file type'),
            (r'.*\.(mp4|avi|mov|wmv|flv|webm)$', 'Video File', 'Video file type'),
            (r'.*\.(mp3|wav|flac|aac|ogg)$', 'Audio File', 'Audio file type'),
            
            # Technical terms
            (r'.*\b(server|database|admin|system|config|settings|backup|archive|temp|cache|log|debug)\b.*', 'Technical Term', 'Technical or system-related term'),
            (r'.*\b(api|sdk|framework|library|plugin|module|component|service|microservice)\b.*', 'Software Component', 'Software development component'),
            (r'.*\b(test|testing|qa|quality|validation|verification|staging|production|development)\b.*', 'Environment/Testing', 'Software development environment or testing term'),
            
            # Business processes
            (r'.*\b(process|procedure|workflow|pipeline|automation|integration|migration)\b.*', 'Business Process', 'Business or operational process'),
            (r'.*\b(report|dashboard|analytics|metrics|kpi|performance|monitoring)\b.*', 'Reporting/Analytics', 'Business reporting or analytics term'),
            (r'.*\b(training|workshop|seminar|course|certification|manual|guide)\b.*', 'Training/Education', 'Training or educational material'),
            
            # Project/Task related
            (r'.*\b(project|task|milestone|deliverable|phase|sprint|iteration|scrum|agile)\b.*', 'Project Management', 'Project or task management term'),
            (r'.*\b(meeting|conference|call|session|workshop|presentation|demo)\b.*', 'Meeting/Event', 'Meeting or event-related term'),
            
            # Geographic/Location
            (r'.*\b(office|building|floor|room|site|location|address|facility)\b.*', 'Location/Facility', 'Physical location or facility reference'),
            (r'.*\b(north|south|east|west|central|regional|local|global|international)\b.*', 'Geographic Reference', 'Geographic or regional reference'),
            
            # Time/Date patterns
            (r'.*\b(daily|weekly|monthly|quarterly|yearly|annual|q[1-4]|fy\d{2,4})\b.*', 'Time Period', 'Time period or schedule reference'),
            (r'.*\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december)\b.*', 'Date Reference', 'Date or calendar reference'),
            
            # Codes and identifiers
            (r'^[A-Z]{2,4}-?\d{2,6}$', 'Code/Identifier', 'Code or identifier reference'),
            (r'^[A-Z]{1,3}\d{1,6}$', 'Code/Identifier', 'Code or identifier reference'),
            (r'^\d{4,10}$', 'Numeric Identifier', 'Numeric identifier or reference number'),
            
            # Single letters or very short codes
            (r'^[A-Z]$', 'Single Letter', 'Single letter reference'),
            (r'^[A-Z]{2}$', 'Two-Letter Code', 'Two-letter code or abbreviation'),
        ]
        
        # Industry-specific terms
        self.industry_terms = {
            'construction': [
                'contractor', 'subcontractor', 'supplier', 'vendor', 'architect', 'engineer', 'surveyor',
                'construction', 'building', 'development', 'infrastructure', 'renovation', 'maintenance',
                'concrete', 'steel', 'timber', 'materials', 'equipment', 'machinery', 'tools',
                'safety', 'compliance', 'permits', 'inspections', 'certifications'
            ],
            'technology': [
                'software', 'hardware', 'technology', 'digital', 'tech', 'innovation', 'solutions',
                'platform', 'application', 'system', 'network', 'cloud', 'data', 'analytics',
                'artificial', 'intelligence', 'machine', 'learning', 'automation', 'integration'
            ],
            'finance': [
                'financial', 'banking', 'investment', 'insurance', 'accounting', 'audit', 'tax',
                'capital', 'funding', 'loan', 'mortgage', 'credit', 'payment', 'transaction',
                'portfolio', 'asset', 'liability', 'equity', 'revenue', 'expense', 'budget'
            ],
            'healthcare': [
                'medical', 'health', 'hospital', 'clinic', 'pharmacy', 'healthcare', 'patient',
                'treatment', 'diagnosis', 'therapy', 'medicine', 'pharmaceutical', 'research',
                'clinical', 'surgical', 'nursing', 'care', 'wellness', 'rehabilitation'
            ],
            'education': [
                'school', 'university', 'college', 'education', 'training', 'learning', 'teaching',
                'student', 'academic', 'research', 'curriculum', 'course', 'program', 'degree',
                'certification', 'knowledge', 'skills', 'development', 'scholarship'
            ],
            'retail': [
                'retail', 'store', 'shop', 'market', 'sales', 'customer', 'product', 'service',
                'brand', 'merchandise', 'inventory', 'supply', 'distribution', 'logistics',
                'marketing', 'advertising', 'promotion', 'discount', 'price', 'purchase'
            ]
        }
        
        # Known real companies (can be expanded)
        self.known_companies = {
            # Technology
            'microsoft', 'apple', 'google', 'amazon', 'meta', 'facebook', 'tesla', 'netflix',
            'oracle', 'salesforce', 'adobe', 'cisco', 'intel', 'nvidia', 'ibm', 'dell',
            'hp', 'lenovo', 'samsung', 'sony', 'lg', 'huawei', 'xiaomi', 'spotify',
            
            # Finance
            'jpmorgan', 'morgan', 'chase', 'wells', 'fargo', 'citigroup', 'goldman', 'sachs',
            'american', 'express', 'visa', 'mastercard', 'paypal', 'square', 'stripe',
            
            # Retail/Consumer
            'walmart', 'target', 'costco', 'home', 'depot', 'lowes', 'macys', 'nike',
            'adidas', 'puma', 'under', 'armour', 'coca', 'cola', 'pepsi', 'starbucks',
            
            # Healthcare/Pharma
            'pfizer', 'johnson', 'merck', 'abbott', 'bristol', 'myers', 'squibb',
            'novartis', 'roche', 'sanofi', 'gsk', 'glaxosmithkline',
            
            # Automotive
            'toyota', 'honda', 'nissan', 'ford', 'chevrolet', 'bmw', 'mercedes', 'audi',
            'volkswagen', 'hyundai', 'kia', 'volvo', 'subaru', 'mazda',
            
            # Construction/Engineering
            'caterpillar', 'deere', 'boeing', 'lockheed', 'martin', 'general', 'electric',
            'siemens', 'schneider', 'electric', 'honeywell', 'emerson', '3m',
            
            # Energy/Utilities
            'exxon', 'mobil', 'chevron', 'shell', 'bp', 'total', 'conocophillips',
            'duke', 'energy', 'southern', 'company', 'dominion', 'nextera',
            
            # Telecommunications
            'verizon', 'att', 'tmobile', 'sprint', 'comcast', 'charter', 'dish',
            'vodafone', 'orange', 'telefonica', 'deutsche', 'telekom',
            
            # Media/Entertainment
            'disney', 'warner', 'bros', 'universal', 'paramount', 'sony', 'pictures',
            'fox', 'cbs', 'nbc', 'abc', 'espn', 'cnn', 'bbc', 'reuters',
            
            # Airlines/Travel
            'american', 'airlines', 'delta', 'united', 'southwest', 'jetblue',
            'lufthansa', 'air', 'france', 'british', 'airways', 'emirates',
            
            # Food/Beverage
            'mcdonalds', 'subway', 'starbucks', 'dominos', 'pizza', 'hut',
            'taco', 'bell', 'kfc', 'burger', 'king', 'wendys',
            
            # Shipping/Logistics
            'fedex', 'ups', 'dhl', 'usps', 'amazon', 'logistics', 'maersk',
            'cosco', 'evergreen', 'hapag', 'lloyd', 'msc'
        }
    
    def categorize_name(self, name: str) -> Tuple[str, str]:
        """
        Categorize a detected name and provide description
        
        Args:
            name: The name to categorize
            
        Returns:
            Tuple of (category, description)
        """
        if not name:
            return ('Unknown', 'Empty or invalid name')
        
        name_clean = name.strip()
        name_upper = name_clean.upper()
        name_lower = name_clean.lower()
        
        # 1. Check exact abbreviation matches
        if name_upper in self.common_abbreviations:
            return ('Abbreviation', self.common_abbreviations[name_upper])
        
        # 2. Check pattern-based rules
        for pattern, category, description in self.pattern_rules:
            if re.match(pattern, name_lower, re.IGNORECASE):
                return (category, description)
        
        # 3. Check if it's a known company
        name_words = name_lower.split()
        for word in name_words:
            if word in self.known_companies:
                return ('Company', f'Known business entity: {name_clean}')
        
        # 4. Check company indicators
        company_indicators = [
            'ltd', 'limited', 'inc', 'incorporated', 'corp', 'corporation', 'llc',
            'plc', 'pty', 'gmbh', 'sa', 'bv', 'nv', 'srl', 'spa', 'ag',
            'co', 'company', 'group', 'holdings', 'enterprises', 'solutions',
            'services', 'systems', 'technologies', 'international', 'global'
        ]
        
        for indicator in company_indicators:
            if indicator in name_lower:
                return ('Company', f'Business entity with corporate indicator: {name_clean}')
        
        # 5. Check industry-specific terms
        for industry, terms in self.industry_terms.items():
            for term in terms:
                if term in name_lower:
                    return ('Industry Term', f'{industry.title()} industry term: {name_clean}')
        
        # 6. Length-based categorization
        if len(name_clean) <= 3:
            if name_clean.isupper():
                return ('Abbreviation', f'Likely abbreviation: {name_clean}')
            else:
                return ('Short Code', f'Short code or reference: {name_clean}')
        
        # 7. Special characters analysis
        special_chars = ['&', '+', '-', '_', '/', '\\', '|', ':', ';', '=', '@', '#', '%']
        if any(char in name_clean for char in special_chars):
            return ('Code/Reference', f'Code or reference with special characters: {name_clean}')
        
        # 8. Numeric analysis
        if name_clean.isdigit():
            return ('Numeric Code', f'Numeric identifier: {name_clean}')
        
        # 9. Mixed case analysis
        if name_clean.isupper():
            return ('Acronym', f'Likely acronym or abbreviation: {name_clean}')
        
        # 10. Word count analysis
        word_count = len(name_clean.split())
        if word_count == 1:
            if name_clean.istitle():
                return ('Single Name', f'Single capitalized name: {name_clean}')
            else:
                return ('Single Term', f'Single term or identifier: {name_clean}')
        elif word_count >= 2:
            # Check if all words are capitalized (typical company pattern)
            words = name_clean.split()
            if all(word[0].isupper() for word in words if word):
                return ('Potential Company', f'Multiple capitalized words, likely business name: {name_clean}')
            else:
                return ('Multi-word Term', f'Multi-word term or phrase: {name_clean}')
        
        # Default fallback
        return ('Unclassified', f'Unclassified name: {name_clean}')
    
    def batch_categorize(self, names: List[str]) -> List[Dict[str, str]]:
        """
        Categorize multiple names at once
        
        Args:
            names: List of names to categorize
            
        Returns:
            List of dictionaries with name, category, and description
        """
        results = []
        for name in names:
            category, description = self.categorize_name(name)
            results.append({
                'name': name,
                'category': category,
                'description': description
            })
        return results
    
    def get_category_summary(self, names: List[str]) -> Dict[str, int]:
        """
        Get summary statistics of categories
        
        Args:
            names: List of names to analyze
            
        Returns:
            Dictionary with category counts
        """
        category_counts = defaultdict(int)
        for name in names:
            category, _ = self.categorize_name(name)
            category_counts[category] += 1
        return dict(category_counts)
    
    def add_custom_abbreviation(self, abbrev: str, expansion: str):
        """
        Add a custom abbreviation and its expansion
        
        Args:
            abbrev: The abbreviation
            expansion: The full expansion
        """
        self.common_abbreviations[abbrev.upper()] = expansion
        
    def add_known_company(self, company_name: str):
        """
        Add a known company to the database
        
        Args:
            company_name: Name of the company to add
        """
        self.known_companies.add(company_name.lower()) 