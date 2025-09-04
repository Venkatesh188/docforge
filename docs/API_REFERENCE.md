# 📚 DocForge API Reference

## 📋 Table of Contents
- [Core Classes](#core-classes)
- [Service Classes](#service-classes)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [CLI Interface](#cli-interface)
- [Error Handling](#error-handling)
- [Type Definitions](#type-definitions)
- [Usage Examples](#usage-examples)

---

## 🏗️ Core Classes

### DocForgeCore

**Location**: `docforge-ai.py`

The main orchestrator class that coordinates document generation workflows.

```python
class DocForgeCore:
    """
    Core DocForge functionality without authentication or external dependencies.
    
    This class serves as the main entry point for document generation operations,
    coordinating between storage services, AI agents, and user interface.
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize DocForge core with optional base directory.
        
        Args:
            base_dir: Base directory for DocForge operations. 
                     Defaults to current working directory.
                     
        Attributes:
            base_dir (Path): Base directory for operations
            generated_docs_dir (Path): Directory for generated documents
            storage (LocalStorageService): Storage service instance  
            doc_agent_service (DocumentAgentService): AI agent service instance
        """
```

#### Methods

##### `async def generate_documents()`

Generate documents from a project idea using AI agents.

```python
async def generate_documents(
    self, 
    idea: str,
    document_types: Optional[List[str]] = None,
    context: Optional[str] = None,
    project_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate documents from an idea using AI agents.
    
    This is the main workflow method that orchestrates the entire
    document generation process from idea to final output files.
    
    Args:
        idea (str): The project idea or description
        document_types (Optional[List[str]]): List of document types to generate.
                                            If None, generates default set:
                                            ['project_charter', 'srs', 
                                             'high_level_design', 'test_specifications']
        context (Optional[str]): Additional context about the project
                               (technology stack, requirements, etc.)
        project_name (Optional[str]): Custom project name. If None,
                                    extracted from idea.
                                    
    Returns:
        Dict[str, Any]: Generation result containing:
            - success (bool): Whether generation succeeded
            - project_dir (str): Path to generated documents directory
            - documents_generated (int): Number of documents created
            - project_metadata (Dict): Project information and metadata
            - error (str, optional): Error message if generation failed
            
    Raises:
        ConfigurationError: If OpenAI API key is not configured
        StorageError: If file system operations fail
        APIError: If AI service calls fail
        
    Example:
        >>> core = DocForgeCore()
        >>> result = await core.generate_documents(
        ...     idea="E-commerce platform for handmade crafts",
        ...     document_types=["project_charter", "srs"],
        ...     context="React frontend, Node.js backend, PostgreSQL database"
        ... )
        >>> print(f"Generated {result['documents_generated']} documents")
        >>> print(f"Location: {result['project_dir']}")
    """
```

##### `def list_document_types()`

Get list of available document types.

```python
def list_document_types(self) -> List[str]:
    """
    Get list of all available document types that can be generated.
    
    Returns:
        List[str]: List of document type identifiers
        
    Example:
        >>> core = DocForgeCore()
        >>> types = core.list_document_types()
        >>> print(types)
        ['project_charter', 'srs', 'high_level_design', 'low_level_design', 
         'test_specifications', 'deployment_guide', 'operations_manual',
         'business_case', 'market_requirements', 'vision_brief']
    """
```

##### `async def get_project_status()`

Get status information for a generated project.

```python
async def get_project_status(self, project_slug: str) -> Dict[str, Any]:
    """
    Get detailed status information for a specific project.
    
    Args:
        project_slug (str): The URL-friendly project identifier
                          (generated from project name)
                          
    Returns:
        Dict[str, Any]: Project status containing:
            - success (bool): Whether the operation succeeded
            - project (Dict): Complete project metadata
            - documents_count (int): Number of generated documents
            - location (str): File system path to project directory
            - error (str, optional): Error message if project not found
            
    Example:
        >>> status = await core.get_project_status("e-commerce-platform")
        >>> if status["success"]:
        ...     print(f"Project: {status['project']['name']}")
        ...     print(f"Documents: {status['documents_count']}")
        ...     print(f"Location: {status['location']}")
    """
```

##### `async def list_projects()`

List all generated projects with summary information.

```python
async def list_projects(self) -> List[Dict[str, Any]]:
    """
    Get summary list of all generated projects.
    
    Returns:
        List[Dict[str, Any]]: List of project summaries, each containing:
            - slug (str): URL-friendly project identifier
            - name (str): Human-readable project name
            - created_at (str): ISO timestamp of creation
            - documents_count (int): Number of generated documents
            - status (str): Project status ('completed', 'in_progress', etc.)
            
    Projects are sorted by creation date (most recent first).
    
    Example:
        >>> projects = await core.list_projects()
        >>> for project in projects:
        ...     print(f"{project['name']} ({project['documents_count']} docs)")
    """
```

---

## 🛠️ Service Classes

### LocalStorageService

**Location**: `backend/app/services/local_storage_service.py`

File system-based storage service that replaces external database dependencies.

```python
class LocalStorageService:
    """
    Local file-system based storage service to replace Supabase.
    
    Provides all database functionality using local JSON files and organized
    directory structures, eliminating need for external database dependencies.
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize local storage service.
        
        Args:
            base_dir (Optional[Path]): Base directory for storage operations.
                                     Defaults to './storage'
                                     
        Attributes:
            base_dir (Path): Base storage directory
            projects_dir (Path): Directory for project metadata files
            documents_dir (Path): Directory for document metadata files
            generated_docs_dir (Path): Directory for output documents
        """
```

#### Project Management Methods

##### `async def create_project()`

Create a new project with metadata.

```python
async def create_project(
    self, 
    name: str, 
    initial_idea: str,
    expanded_concept: Optional[str] = None,
    additional_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new project with metadata storage.
    
    Args:
        name (str): Human-readable project name
        initial_idea (str): Original project idea or description
        expanded_concept (Optional[str]): AI-expanded project concept
        additional_context (Optional[str]): Extra context provided by user
        
    Returns:
        Dict[str, Any]: Creation result containing:
            - success (bool): Whether project was created successfully
            - project (Dict): Complete project metadata
            - error (str, optional): Error message if creation failed
            
    The project metadata includes:
        - id: Unique UUID for the project
        - name: Human-readable name
        - slug: URL-friendly identifier  
        - initial_idea: Original user input
        - expanded_concept: AI-enhanced description
        - additional_context: User-provided context
        - status: Current project status
        - created_at/updated_at: Timestamps
        - documents_generated: List of document IDs
        - generation_config: AI and generation settings
        
    Example:
        >>> storage = LocalStorageService()
        >>> result = await storage.create_project(
        ...     name="E-commerce Platform",
        ...     initial_idea="Online marketplace for handmade crafts",
        ...     additional_context="React frontend, Node.js backend"
        ... )
        >>> project_id = result["project"]["id"]
    """
```

##### `async def get_project()`

Retrieve project by ID.

```python
async def get_project(self, project_id: str) -> Dict[str, Any]:
    """
    Retrieve project metadata by unique ID.
    
    Args:
        project_id (str): Unique project identifier (UUID)
        
    Returns:
        Dict[str, Any]: Retrieval result containing:
            - success (bool): Whether project was found
            - project (Dict): Complete project metadata  
            - error (str, optional): Error message if not found
    """
```

##### `async def list_projects()`

List all projects with metadata.

```python
async def list_projects(self) -> Dict[str, Any]:
    """
    List all projects stored in the system.
    
    Returns:
        Dict[str, Any]: List result containing:
            - success (bool): Whether operation succeeded
            - projects (List[Dict]): List of all project metadata
            - count (int): Number of projects found
            - error (str, optional): Error message if operation failed
            
    Projects are sorted by creation date (newest first).
    """
```

##### `async def update_project()`

Update existing project metadata.

```python
async def update_project(
    self, 
    project_id: str, 
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update project metadata with new information.
    
    Args:
        project_id (str): Unique project identifier
        updates (Dict[str, Any]): Fields to update (cannot update 'id')
        
    Returns:
        Dict[str, Any]: Update result containing:
            - success (bool): Whether update succeeded
            - project (Dict): Updated project metadata
            - error (str, optional): Error message if update failed
            
    The 'updated_at' timestamp is automatically set to current time.
    """
```

##### `async def delete_project()`

Delete project and all associated documents.

```python
async def delete_project(self, project_id: str) -> Dict[str, Any]:
    """
    Delete a project and all its associated documents.
    
    This operation:
    1. Removes project metadata file
    2. Deletes generated documents directory
    3. Removes individual document metadata files
    
    Args:
        project_id (str): Unique project identifier
        
    Returns:
        Dict[str, Any]: Deletion result containing:
            - success (bool): Whether deletion succeeded
            - message (str): Success message
            - error (str, optional): Error message if deletion failed
            
    Warning:
        This operation is irreversible. All project data and generated
        documents will be permanently deleted.
    """
```

#### Document Management Methods

##### `async def create_document()`

Create and store a new document.

```python
async def create_document(
    self, 
    project_id: str,
    document_type: str,
    title: str,
    content: str = "",
    additional_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new document associated with a project.
    
    Args:
        project_id (str): Parent project unique identifier
        document_type (str): Type of document (from DocumentType enum)
        title (str): Human-readable document title
        content (str): Full document content in Markdown format
        additional_context (Optional[str]): Extra context for this document
        
    Returns:
        Dict[str, Any]: Creation result containing:
            - success (bool): Whether document was created
            - document (Dict): Complete document metadata
            - error (str, optional): Error message if creation failed
            
    The document is stored in two locations:
    1. Metadata as JSON in storage/documents/{document_id}.json
    2. Content as Markdown in generated-docs/{project_slug}/{sequence}_{type}.md
    """
```

##### `async def list_project_documents()`

List all documents for a specific project.

```python
async def list_project_documents(self, project_id: str) -> Dict[str, Any]:
    """
    List all documents associated with a project.
    
    Args:
        project_id (str): Project unique identifier
        
    Returns:
        Dict[str, Any]: List result containing:
            - success (bool): Whether operation succeeded
            - documents (List[Dict]): List of document metadata
            - count (int): Number of documents found
            - error (str, optional): Error message if operation failed
            
    Documents are sorted by creation date (oldest first).
    """
```

#### Utility Methods

##### `def get_storage_info()`

Get storage statistics and information.

```python
def get_storage_info(self) -> Dict[str, Any]:
    """
    Get comprehensive storage statistics.
    
    Returns:
        Dict[str, Any]: Storage information containing:
            - base_directory (str): Base storage path
            - projects_count (int): Number of projects stored
            - documents_count (int): Number of documents stored  
            - total_size_bytes (int): Total storage size in bytes
            - total_size_mb (float): Total storage size in megabytes
            - error (str, optional): Error message if calculation failed
    """
```

##### `def cleanup_storage()`

Clean up orphaned files and optimize storage.

```python
def cleanup_storage(self) -> Dict[str, Any]:
    """
    Remove orphaned documents and optimize storage.
    
    This operation:
    1. Identifies documents without parent projects
    2. Removes orphaned document files
    3. Reports cleanup statistics
    
    Returns:
        Dict[str, Any]: Cleanup result containing:
            - success (bool): Whether cleanup succeeded
            - orphaned_documents_removed (int): Number of files removed
            - message (str): Summary of cleanup operations
            - error (str, optional): Error message if cleanup failed
    """
```

### DocumentAgentService

**Location**: `backend/app/services/document_agents.py`

AI-powered document generation service using specialized agents.

```python
class DocumentAgentService:
    """
    AI agent service for generating specialized documents.
    
    Uses CrewAI framework to coordinate specialized AI agents, each optimized
    for generating specific types of professional documents.
    """
    
    def __init__(self, db=None):
        """
        Initialize document agent service.
        
        Args:
            db: Database connection (unused in self-contained version)
            
        Attributes:
            openai_service (OpenAIService): OpenAI API integration
            agents_config (Dict): Configuration for document type agents
        """
```

##### `async def generate_document()`

Generate a document using a specialized AI agent.

```python
async def generate_document(
    self,
    document_type: DocumentType,
    project: Dict[str, Any],
    additional_context: Optional[str] = None,
    custom_requirements: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generate document using specialized AI agent for the document type.
    
    Args:
        document_type (DocumentType): Type of document to generate
        project (Dict[str, Any]): Project metadata and context
        additional_context (Optional[str]): Extra context for generation
        custom_requirements (Optional[List[str]]): Specific requirements
        
    Returns:
        Dict[str, Any]: Generation result containing:
            - success (bool): Whether generation succeeded
            - content (str): Generated document content in Markdown
            - tokens_used (int): Number of AI tokens consumed
            - agent_used (str): Name of the agent that generated content
            - error (str, optional): Error message if generation failed
            
    The generation process:
    1. Loads agent configuration for document type
    2. Builds context-aware prompt using templates
    3. Calls OpenAI API via CrewAI framework
    4. Processes and validates the response
    5. Returns structured result with metadata
    """
```

### SimpleSettings

**Location**: `backend/app/core/simple_config.py`

Centralized configuration management for self-contained operation.

```python
class SimpleSettings:
    """
    Simplified settings for self-contained DocForge operation.
    
    Manages all configuration through environment variables with
    sensible defaults, eliminating complex configuration systems.
    """
    
    def __init__(self):
        """
        Initialize settings from environment variables.
        
        Configuration is loaded with the following priority:
        1. Environment variables
        2. .env file values  
        3. Built-in default values
        
        Attributes:
            # Application Info
            app_name (str): Application name
            app_version (str): Current version
            debug (bool): Debug mode flag
            
            # AI Configuration  
            openai_api_key (str): OpenAI API key (required)
            openai_model (str): OpenAI model to use (default: gpt-4)
            
            # Storage Configuration
            storage_path (Path): Internal storage directory
            generated_docs_path (Path): Generated documents directory
            
            # Performance Settings
            concurrent_generations (int): Max concurrent document generation
            generation_timeout (int): Timeout for generation requests
            max_file_size (int): Maximum file size in bytes
            
            # Feature Flags
            enable_validation (bool): Enable content validation
            
            # Optional Integrations
            notion_token (str): Notion API token
            notion_database_id (str): Notion database ID
        """
```

#### Configuration Methods

##### `def validate_config()`

Comprehensive configuration validation.

```python
def validate_config(self) -> Dict[str, Any]:
    """
    Validate current configuration and report issues.
    
    Returns:
        Dict[str, Any]: Validation result containing:
            - valid (bool): Whether configuration is valid
            - errors (List[str]): List of error messages
            - warnings (List[str]): List of warning messages
            
    Validation checks:
    - Required settings (OpenAI API key)
    - Directory permissions and creation
    - Optional feature configurations
    
    Example:
        >>> settings = SimpleSettings()
        >>> result = settings.validate_config()
        >>> if not result["valid"]:
        ...     for error in result["errors"]:
        ...         print(f"Error: {error}")
    """
```

##### `def get_config_summary()`

Get summary of current configuration.

```python
def get_config_summary(self) -> Dict[str, Any]:
    """
    Get comprehensive summary of current configuration.
    
    Returns:
        Dict[str, Any]: Configuration summary containing:
            - app_name (str): Application name
            - app_version (str): Current version
            - openai_model (str): Configured AI model
            - openai_api_key_configured (bool): Whether API key is set
            - storage_path (str): Storage directory path
            - generated_docs_path (str): Output directory path
            - document_types_count (int): Number of enabled document types
            - notion_configured (bool): Whether Notion is configured
            - debug_mode (bool): Debug flag status
            - validation_enabled (bool): Validation flag status
            - concurrent_generations (int): Concurrency setting
            
    Useful for debugging configuration issues.
    """
```

---

## 📊 Data Models

### DocumentType Enumeration

**Location**: `backend/app/models.py`

```python
class DocumentType(str, Enum):
    """
    Enumeration of supported document types.
    
    Each document type corresponds to a specialized AI agent
    and prompt template for generating specific kinds of
    professional documentation.
    """
    
    PROJECT_CHARTER = "project_charter"
    """
    Project Charter - Board-grade project initiation documents
    Includes executive summary, objectives, scope, timeline, budget
    """
    
    SRS = "srs"  
    """
    Software Requirements Specification - Comprehensive requirements
    Includes functional, non-functional, and technical requirements
    """
    
    HIGH_LEVEL_DESIGN = "high_level_design"
    """
    System Architecture (HLD) - High-level system design
    Includes architecture diagrams, technology stack, security design
    """
    
    LOW_LEVEL_DESIGN = "low_level_design"
    """
    Low-Level Design (LLD) - Detailed technical design
    Includes API specifications, database design, component details
    """
    
    TEST_SPECIFICATIONS = "test_specifications"
    """
    Test Specifications - Comprehensive testing strategy
    Includes test plans, test cases, acceptance criteria
    """
    
    DEPLOYMENT_GUIDE = "deployment_guide" 
    """
    Deployment Guide - Production deployment procedures
    Includes infrastructure, CI/CD, monitoring, rollback procedures
    """
    
    OPERATIONS_MANUAL = "operations_manual"
    """
    Operations Manual - Operational procedures and maintenance
    Includes monitoring, troubleshooting, support procedures
    """
    
    BUSINESS_CASE = "business_case"
    """
    Business Case - Business justification and ROI analysis
    Includes financial projections, market analysis, risk assessment
    """
    
    MARKET_REQUIREMENTS = "market_requirements"
    """
    Market Requirements - Market analysis and competitive positioning
    Includes competitor analysis, market research, positioning strategy
    """
    
    VISION_BRIEF = "vision_brief"
    """
    Vision Brief - Strategic vision and opportunity assessment
    Includes vision statement, strategic goals, opportunity analysis
    """
```

### Project Metadata Schema

```python
ProjectMetadata = {
    "id": "str",                    # Unique UUID identifier
    "name": "str",                  # Human-readable project name
    "slug": "str",                  # URL-friendly identifier
    "initial_idea": "str",          # Original user input
    "expanded_concept": "str",      # AI-enhanced description
    "additional_context": "str",    # User-provided context
    "status": "str",                # Project status
    "created_at": "str",            # ISO timestamp
    "updated_at": "str",            # ISO timestamp  
    "documents_generated": ["str"], # List of document IDs
    "generation_config": {
        "ai_model": "str",          # AI model used
        "document_types": ["str"],  # Generated document types
        "custom_requirements": ["str"] # Custom requirements
    }
}
```

### Document Metadata Schema

```python
DocumentMetadata = {
    "id": "str",                    # Unique document identifier
    "project_id": "str",            # Parent project ID
    "document_type": "str",         # Document type from enum
    "title": "str",                 # Human-readable title
    "content": "str",               # Full Markdown content
    "additional_context": "str",    # Document-specific context
    "status": "str",                # Document status
    "version": "int",               # Document version number
    "slug": "str",                  # URL-friendly identifier
    "created_at": "str",            # ISO timestamp
    "updated_at": "str",            # ISO timestamp
    "tokens_used": "int",           # AI tokens consumed
    "agent_used": "str"             # Agent that generated content
}
```

---

## ⚙️ Configuration

### Environment Variables

All configuration is managed through environment variables, typically stored in a `.env` file.

#### Required Settings

```bash
# OpenAI API Configuration (Required)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### Optional Settings

```bash
# AI Model Configuration
OPENAI_MODEL=gpt-4                          # Default: gpt-4

# Storage Configuration  
STORAGE_PATH=./storage                      # Default: ./storage
GENERATED_DOCS_PATH=./generated-docs        # Default: ./generated-docs

# Document Type Configuration
ENABLED_DOCUMENT_TYPES=project_charter,srs,high_level_design,test_specifications

# Performance Configuration
CONCURRENT_GENERATIONS=1                    # Default: 1
GENERATION_TIMEOUT=300                      # Default: 300 seconds
MAX_FILE_SIZE=10485760                      # Default: 10MB

# Feature Flags
ENABLE_VALIDATION=true                      # Default: true
DEBUG=false                                 # Default: false
LOG_LEVEL=INFO                             # Default: INFO

# Optional Integrations
NOTION_TOKEN=secret_your_notion_token      # Optional
NOTION_DATABASE_ID=your_database_id        # Optional
```

#### Configuration Validation

```python
# Check if configuration is valid
from backend.app.core.simple_config import settings

validation_result = settings.validate_config()
if not validation_result["valid"]:
    print("Configuration errors:")
    for error in validation_result["errors"]:
        print(f"  - {error}")
```

---

## 💻 CLI Interface

### Command Structure

The CLI interface provides the primary way to interact with DocForge.

```bash
# General format
docforge-ai <command> [arguments] [options]
```

### Available Commands

#### `init` - Initialize DocForge

```bash
docforge-ai init

# Description: Initialize DocForge in the current directory
# Actions:
#   - Creates storage directories
#   - Creates .env template file  
#   - Validates configuration
#   - Reports setup status
```

#### `generate` - Generate Documentation

```bash
docforge-ai generate <idea> [options]

# Arguments:
#   idea (str): Your project idea or description

# Options:
#   --docs <types>      Comma-separated list of document types
#   --context <text>    Additional context about your project  
#   --name <name>       Custom project name

# Examples:
docforge-ai generate "E-commerce platform for handmade crafts"

docforge-ai generate "Mobile fitness app" \
  --docs srs,hld,test_specifications \
  --context "React Native, Node.js backend, PostgreSQL"

docforge-ai generate "AI chatbot" \
  --name "Customer Service Bot" \
  --context "24/7 operation, multi-language support"
```

#### `list-docs` - List Document Types

```bash
docforge-ai list-docs

# Description: Display all available document types
# Output: List of document types with descriptions
```

#### `list-projects` - List Generated Projects

```bash
docforge-ai list-projects

# Description: Display all generated projects with summary information
# Output: Project names, document counts, creation dates, status
```

#### `status` - Get Project Status

```bash
docforge-ai status <project-slug>

# Arguments:
#   project-slug (str): URL-friendly project identifier

# Example:
docforge-ai status e-commerce-platform

# Output: Detailed project information including:
#   - Project name and ID
#   - Creation date and status
#   - Number of generated documents
#   - File system location
```

### CLI Return Codes

```python
# Success codes
0   # Operation completed successfully

# Error codes  
1   # General error (configuration, API, etc.)
2   # Invalid arguments or command
3   # File system error (permissions, space, etc.)
4   # API error (OpenAI rate limit, invalid key, etc.)
```

---

## ❌ Error Handling

### Exception Hierarchy

```python
class DocForgeError(Exception):
    """Base exception for all DocForge operations"""
    pass

class ConfigurationError(DocForgeError):
    """Configuration-related errors"""
    pass

class StorageError(DocForgeError):
    """File system and storage errors"""
    pass

class APIError(DocForgeError):
    """AI service and API errors"""  
    pass

class ValidationError(DocForgeError):
    """Input validation errors"""
    pass
```

### Error Response Format

All methods return errors in a consistent format:

```python
{
    "success": False,
    "error": "Human-readable error message",
    "error_type": "ConfigurationError",
    "operation": "generate_documents", 
    "timestamp": "2024-01-20T10:30:00Z",
    "details": {
        # Additional context-specific information
    }
}
```

### Common Errors

#### Configuration Errors

```python
# Missing OpenAI API key
{
    "success": False,
    "error": "OPENAI_API_KEY is required",
    "error_type": "ConfigurationError"
}

# Invalid storage path
{
    "success": False, 
    "error": "Cannot create storage directories: Permission denied",
    "error_type": "ConfigurationError"
}
```

#### Storage Errors

```python
# File permission error
{
    "success": False,
    "error": "Cannot write project file: Permission denied",
    "error_type": "StorageError"
}

# Disk space error
{
    "success": False,
    "error": "Insufficient disk space for document storage", 
    "error_type": "StorageError"
}
```

#### API Errors

```python
# Rate limit exceeded
{
    "success": False,
    "error": "OpenAI API rate limit exceeded. Please try again later.",
    "error_type": "APIError",
    "details": {
        "retry_after": 60
    }
}

# Invalid API key
{
    "success": False,
    "error": "Invalid OpenAI API key",
    "error_type": "APIError"
}
```

---

## 🔤 Type Definitions

### Common Type Aliases

```python
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Common type aliases used throughout the codebase
ProjectID = str              # UUID string for project identification
DocumentID = str             # UUID string for document identification  
ProjectSlug = str            # URL-friendly project identifier
TimestampISO = str          # ISO format timestamp string
FilePath = Union[str, Path]  # File path (string or Path object)

# Complex type definitions
ProjectMetadata = Dict[str, Any]    # Project metadata dictionary
DocumentMetadata = Dict[str, Any]   # Document metadata dictionary
GenerationResult = Dict[str, Any]   # Document generation result
ConfigValidation = Dict[str, Any]   # Configuration validation result
StorageResult = Dict[str, Any]      # Storage operation result
```

### Function Signatures Reference

```python
# Core functions
async def generate_documents(
    idea: str,
    document_types: Optional[List[str]] = None,
    context: Optional[str] = None,
    project_name: Optional[str] = None
) -> Dict[str, Any]: ...

# Storage functions
async def create_project(
    name: str,
    initial_idea: str,
    expanded_concept: Optional[str] = None,
    additional_context: Optional[str] = None
) -> Dict[str, Any]: ...

# Configuration functions  
def validate_config() -> Dict[str, Any]: ...
def get_config_summary() -> Dict[str, Any]: ...
```

---

## 📖 Usage Examples

### Basic Document Generation

```python
import asyncio
from docforge-ai import DocForgeCore

async def basic_example():
    """Basic document generation example"""
    
    # Initialize DocForge
    core = DocForgeCore()
    
    # Generate default document set
    result = await core.generate_documents(
        idea="E-commerce platform for handmade crafts"
    )
    
    if result["success"]:
        print(f"✅ Generated {result['documents_generated']} documents")
        print(f"📁 Location: {result['project_dir']}")
    else:
        print(f"❌ Generation failed: {result['error']}")

# Run the example
asyncio.run(basic_example())
```

### Advanced Document Generation with Context

```python
async def advanced_example():
    """Advanced document generation with specific types and context"""
    
    core = DocForgeCore()
    
    # Generate specific document types with context
    result = await core.generate_documents(
        idea="AI-powered customer service chatbot",
        document_types=[
            "project_charter",
            "srs", 
            "high_level_design",
            "test_specifications"
        ],
        context="React frontend, Python FastAPI backend, OpenAI GPT-4 integration, CRM connectivity, 24/7 operation",
        project_name="AI Customer Service Bot"
    )
    
    if result["success"]:
        project_metadata = result["project_metadata"]
        print(f"✅ Project: {project_metadata['name']}")
        print(f"📄 Documents: {result['documents_generated']}")
        print(f"🤖 AI Model: {project_metadata['generation_config']['ai_model']}")
        print(f"📁 Location: {result['project_dir']}")
    else:
        print(f"❌ Error: {result['error']}")

asyncio.run(advanced_example())
```

### Project Management

```python
async def project_management_example():
    """Example of project listing and status checking"""
    
    core = DocForgeCore()
    
    # List all projects
    projects = await core.list_projects()
    print(f"📂 Found {len(projects)} projects:")
    
    for project in projects:
        print(f"  • {project['name']} ({project['documents_count']} docs)")
        print(f"    Status: {project['status']}, Created: {project['created_at']}")
    
    # Get detailed status for specific project
    if projects:
        first_project_slug = projects[0]['slug'] 
        status = await core.get_project_status(first_project_slug)
        
        if status["success"]:
            project_info = status["project"]
            print(f"\n📊 Project Details: {project_info['name']}")
            print(f"   ID: {project_info['id']}")
            print(f"   Idea: {project_info['initial_idea']}")
            print(f"   Documents: {status['documents_count']}")
            print(f"   Location: {status['location']}")

asyncio.run(project_management_example())
```

### Configuration and Storage Management

```python
from backend.app.core.simple_config import settings
from backend.app.services.local_storage_service import LocalStorageService

async def configuration_example():
    """Example of configuration validation and storage management"""
    
    # Validate configuration
    validation = settings.validate_config()
    
    if validation["valid"]:
        print("✅ Configuration is valid")
        
        # Show configuration summary
        summary = settings.get_config_summary()
        print(f"🤖 AI Model: {summary['openai_model']}")
        print(f"📁 Storage: {summary['storage_path']}")
        print(f"🔧 Debug Mode: {summary['debug_mode']}")
        
    else:
        print("❌ Configuration errors:")
        for error in validation["errors"]:
            print(f"   - {error}")
    
    # Storage information
    storage = LocalStorageService()
    storage_info = storage.get_storage_info()
    
    print(f"\n💾 Storage Information:")
    print(f"   Location: {storage_info['base_directory']}")  
    print(f"   Projects: {storage_info['projects_count']}")
    print(f"   Documents: {storage_info['documents_count']}")
    print(f"   Size: {storage_info['total_size_mb']} MB")

asyncio.run(configuration_example())
```

### Error Handling Example

```python
async def error_handling_example():
    """Example of proper error handling"""
    
    core = DocForgeCore()
    
    try:
        result = await core.generate_documents(
            idea="Test project for error handling",
            document_types=["invalid_document_type"]  # This will cause an error
        )
        
        if result["success"]:
            print("✅ Generation succeeded")
        else:
            print(f"❌ Generation failed: {result['error']}")
            
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        
    # Check configuration before generation
    validation = settings.validate_config()
    if not validation["valid"]:
        print("⚠️  Configuration issues detected:")
        for error in validation["errors"]:
            print(f"   - {error}")
        return
    
    # Safe generation with error handling
    try:
        result = await core.generate_documents(
            idea="Well-formed project idea",
            document_types=["project_charter"]  # Valid document type
        )
        
        if result["success"]:
            print("✅ Safe generation succeeded")
        else:
            print(f"❌ Safe generation failed: {result['error']}")
            
    except Exception as e:
        print(f"💥 Unexpected error in safe generation: {e}")

asyncio.run(error_handling_example())
```

---

This API reference provides comprehensive documentation of all public interfaces, methods, and data structures in DocForge. For implementation details and internal APIs, refer to the source code and developer guide.
