#!/usr/bin/env python3
"""
DocForge Setup Script

Installation script for DocForge - Open Source AI-Powered Documentation Generator
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
req_file = this_directory / "requirements.txt"
if req_file.exists():
    with open(req_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="docforge-ai",
    version="2.0.3",
    author="DocForge Community",
    author_email="community@docforge.dev",
    description="Self-contained AI-powered documentation generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Venkatesh188/docforge-ai",
    packages=find_packages(include=["backend*", "prompts*", "docforge*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0"
        ],
        "notion": [
            "notion-client>=2.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "docforge-ai=docforge.docforge:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "prompts/*.md",
            "backend/app/templates/*.py",
            "*.md",
            "*.txt",
            "*.yml",
            "*.yaml"
        ]
    },
    keywords=[
        "documentation",
        "ai",
        "generator",
        "automation",
        "software-development",
        "project-management",
        "crewai",
        "openai",
        "markdown"
    ],
    project_urls={
        "Bug Reports": "https://github.com/Venkatesh188/docforge-ai/issues",
        "Feature Requests": "https://github.com/Venkatesh188/docforge-ai/issues/new?template=feature_request.yml",
        "Documentation": "https://github.com/Venkatesh188/docforge-ai/wiki",
        "Source": "https://github.com/Venkatesh188/docforge-ai",
        "PyPI": "https://pypi.org/project/docforge-ai/",
    },
    zip_safe=False,
)