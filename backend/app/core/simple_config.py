"""
Simple Configuration for DocForge CLI
Handles environment variables and settings for the self-contained version
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic_settings import BaseSettings
from pydantic import Field
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Configuration settings for DocForge"""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    
    # Storage Configuration
    storage_path: Path = Field(Path("storage"), env="DOCFORGE_STORAGE_PATH")
    generated_docs_path: Path = Field(Path("generated-docs"), env="DOCFORGE_GENERATED_DOCS_PATH")
    
    # Document Generation Settings
    max_tokens_per_document: int = Field(3000, env="DOCFORGE_MAX_TOKENS")
    default_document_types: List[str] = Field(
        ["project_charter", "srs", "architecture", "test_specification"],
        env="DOCFORGE_DEFAULT_DOCS"
    )
    
    # Logging Configuration
    log_level: str = Field("INFO", env="DOCFORGE_LOG_LEVEL")
    log_file: Optional[str] = Field(None, env="DOCFORGE_LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from environment
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate the current configuration"""
        errors = []
        warnings = []
        
        # Check OpenAI API key
        if not self.openai_api_key:
            errors.append("OpenAI API key is required. Set OPENAI_API_KEY in .env file")
        
        # Check if API key looks valid (basic validation)
        if self.openai_api_key and not self.openai_api_key.startswith("sk-"):
            warnings.append("OpenAI API key format may be invalid (should start with 'sk-')")
        
        # Check storage paths
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self.generated_docs_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create storage directories: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

# Global settings instance
settings = Settings()



def check_configuration() -> bool:
    """Quick check if configuration is valid"""
    validation = settings.validate_config()
    return validation["valid"]

def create_env_template(env_path: str) -> None:
    """Create a .env template file"""
    template_content = """# DocForge Configuration
# Copy this file and update with your actual values

# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Output Configuration (Optional)
DOCFORGE_GENERATED_DOCS_PATH=generated-docs

# Document Generation Settings (Optional)
DOCFORGE_MAX_TOKENS=3000
DOCFORGE_DEFAULT_DOCS=project_charter,srs,architecture,test_specification

# Logging Configuration (Optional)
DOCFORGE_LOG_LEVEL=INFO
DOCFORGE_LOG_FILE=

# How to get your OpenAI API key:
# 1. Go to https://platform.openai.com/api-keys
# 2. Sign in to your OpenAI account
# 3. Click "Create new secret key"
# 4. Copy the key and replace 'your_openai_api_key_here' above
# 5. Save this file as .env
"""
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    logger.info(f"Created .env template at {env_path}")

def get_available_document_types() -> List[Dict[str, str]]:
    """Get list of available document types with descriptions"""
    return [
        {
            "type": "project_charter",
            "name": "Project Charter",
            "description": "Executive-level project overview with business objectives, scope, and timeline"
        },
        {
            "type": "srs",
            "name": "Software Requirements Specification",
            "description": "Detailed functional and non-functional requirements with user stories"
        },
        {
            "type": "architecture",
            "name": "System Architecture",
            "description": "High-level system design with components, security, and scalability"
        },
        {
            "type": "low_level_design",
            "name": "Low-Level Design",
            "description": "Detailed technical design with API specifications and database schema"
        },
        {
            "type": "test_specification",
            "name": "Test Specification",
            "description": "Comprehensive testing strategy with test cases and acceptance criteria"
        },
        {
            "type": "deployment_guide",
            "name": "Deployment Guide",
            "description": "Step-by-step deployment and release procedures"
        },
        {
            "type": "operations_manual",
            "name": "Operations Manual",
            "description": "System operations, monitoring, and maintenance procedures"
        },
        {
            "type": "business_case",
            "name": "Business Case",
            "description": "ROI analysis and business justification for the project"
        },
        {
            "type": "market_requirements",
            "name": "Market Requirements",
            "description": "Market analysis and user requirements documentation"
        },
        {
            "type": "vision_brief",
            "name": "Vision Brief",
            "description": "Strategic vision and opportunity brief for stakeholders"
        }
    ]

def get_prompt_mapping() -> Dict[str, str]:
    """Get mapping of document types to their prompt files"""
    return {
        "project_charter": "charter.md",
        "srs": "requirements.md", 
        "architecture": "architecture.md",
        "low_level_design": "design.md",
        "test_specification": "testing.md",
        "deployment_guide": "deployment.md",
        "operations_manual": "operations.md",
        "business_case": "business_case.md",
        "market_requirements": "market_requirements.md",
        "vision_brief": "vision_brief.md"
    }
