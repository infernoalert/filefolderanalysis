"""
Configuration Management

This package contains configuration management for the company analyzer
including settings, patterns, and environment configuration.
"""

from .config import AnalyzerConfig, ConfigurationError

__all__ = [
    "AnalyzerConfig",
    "ConfigurationError"
] 