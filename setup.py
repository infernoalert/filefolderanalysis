"""
Setup script for Company Analyzer package
"""

from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="company-analyzer",
    version="1.0.0",
    author="Company Analyzer Team",
    author_email="info@companyanalyzer.com",
    description="A powerful, AI-enhanced Python solution for extracting company names from CSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/company-analyzer",
    packages=find_packages(),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Business",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "ai": ["openai>=1.3.0"],
        "mcp": ["fastapi>=0.104.0", "uvicorn>=0.24.0"],
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "isort>=5.0.0", "flake8>=5.0.0", "mypy>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "company-analyzer=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src.config": ["*.json", "*.yaml"],
        "docs": ["*.md"],
        "examples": ["*.py"],
    },
    keywords="company analysis, NLP, CSV processing, business intelligence, AI",
    project_urls={
        "Bug Reports": "https://github.com/your-username/company-analyzer/issues",
        "Source": "https://github.com/your-username/company-analyzer",
        "Documentation": "https://github.com/your-username/company-analyzer/tree/main/docs",
    },
) 