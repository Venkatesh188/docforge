# DocForge-ai - Open Source AI Documentation Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![PyPI version](https://badge.fury.io/py/docforge-ai.svg)](https://badge.fury.io/py/docforge-ai)
[![Downloads](https://pepy.tech/badge/docforge-ai)](https://pepy.tech/project/docforge-ai)

**DocForge-ai** is a powerful, self-contained AI-powered documentation generator that transforms simple project ideas into comprehensive, professional software documentation. Built with CrewAI and OpenAI, it generates enterprise-grade documents including project charters, requirements specifications, architecture documents, and more.

## 🚀 Quick Start

**Install from PyPI:**
```bash
# Using pip
pip install docforge-ai

# Using uv (faster)
uv pip install docforge-ai
```

**Get started in seconds:**
```bash
docforge-ai init
docforge-ai generate "AI-powered chatbot for customer service"
```

> **📦 Available on PyPI**: Install with `pip install docforge-ai` or `uv pip install docforge-ai`


## 🚀 Features

- **PRD-First Workflow**: Start with a Product Requirements Document including user stories, validate, then expand
- **AI-Powered Generation**: Uses advanced AI agents to create professional documentation
- **Multiple Document Types**: Generate 10+ different types of technical documents
- **Self-Contained**: No external database dependencies - uses local file storage
- **Easy Setup**: Simple installation and configuration with `.env` file
- **Professional Quality**: Enterprise-grade document templates and formatting
- **Document Revision**: Revise PRDs with additional specifications using AI
- **Contextual Generation**: Generate additional documents based on validated PRD content
- **Flexible Output**: Generate specific document types or complete document sets
- **Neat Organization**: Documents are stored in organized project directories
- **Interactive Setup**: Guided initialization with document type selection

## 📋 Supported Document Types

1. **Project Charter** - Executive-level project overview with business objectives, scope, and timeline
2. **Software Requirements Specification (SRS)** - Detailed functional and non-functional requirements with user stories
3. **System Architecture** - High-level system design with components, security, and scalability
4. **Low-Level Design** - Detailed technical design with API specifications and database schema
5. **Test Specification** - Comprehensive testing strategy with test cases and acceptance criteria
6. **Deployment Guide** - Step-by-step deployment and release procedures
7. **Operations Manual** - System operations, monitoring, and maintenance procedures
8. **Business Case** - ROI analysis and business justification for the project
9. **Market Requirements** - Market analysis and user requirements documentation
10. **Vision Brief** - Strategic vision and opportunity brief for stakeholders


## 🎥 Demo Video
Check out the quick demo of **DocForge-AI** in action:  
[![DocForge-AI Demo](https://img.youtube.com/vi/LMP-9WBePdY/0.jpg)](https://youtu.be/LMP-9WBePdY)


## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Install from PyPI (Recommended)

**Using pip:**
```bash
pip install docforge-ai
```

**Using uv (faster and more reliable):**
```bash
# Install uv if you don't have it
pip install uv

# Install docforge-ai
uv pip install docforge-ai
```

**Using conda:**
```bash
conda install -c conda-forge pip
pip install docforge-ai
```

### Install from Source (Development)
```bash
# Clone the repository
git clone https://github.com/Venkatesh188/docforge-ai.git
cd docforge-ai

# Install dependencies
pip install -r requirements.txt

# Initialize DocForge-ai (creates .env file and shows available document types)
docforge-ai init
```

## 🎯 Getting Started

After installation, follow these steps:

1. **Initialize DocForge-ai:**
   ```bash
   docforge-ai init
   ```
   This creates a `.env` file where you'll add your OpenAI API key.

2. **Add your OpenAI API key:**
   ```bash
   # Edit the .env file
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

3. **Generate your first document:**
   ```bash
   docforge-ai generate "AI-powered chatbot for customer service"
   ```

4. **Explore available commands:**
   ```bash
   docforge-ai --help
   docforge-ai list-docs
   ```

### Package Installation
```bash
# Install from source
pip install .

# Or install in development mode
pip install -e .
```

## ⚙️ Configuration

### Initial Setup
1. **Run initialization** to create the `.env` file:
```bash
docforge-ai init
```

2. **Edit the `.env` file** with your OpenAI API key:
```bash
# Required
OPENAI_API_KEY=your_actual_openai_api_key_here

# Optional (defaults shown)
OPENAI_MODEL=gpt-4o-mini
DOCFORGE_GENERATED_DOCS_PATH=generated-docs
```

3. **Get your OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)

## 🚀 Quick Start

### Interactive Mode (Recommended for first-time users)
```bash
python start_docforge-ai.py
```

### Command Line Usage

#### PRD-First Workflow (Recommended)

The recommended approach is to start with a Product Requirements Document (PRD) that includes user stories, validate it, and then generate additional documents based on the validated PRD.

**Step 1: Generate a PRD**
```bash
# Generate a PRD with user stories
docforge-ai generate "AI-powered chatbot for customer service" --docs srs
```

**Step 2: Review and Optionally Revise the PRD**
```bash
# Review the generated PRD file, then optionally add more specifications
docforge-ai revise ai-powered-chatbot-for-customer-service -s "Add multi-language support and integration with Slack and Microsoft Teams"
```

**Step 3: Generate Additional Documents Based on Validated PRD**
```bash
# Generate architecture, testing, and deployment documents based on the PRD
docforge-ai continue ai-powered-chatbot-for-customer-service ARCH TEST DEPLOY

# Or generate specific documents
docforge-ai continue ai-powered-chatbot-for-customer-service ARCHITECTURE
docforge-ai continue ai-powered-chatbot-for-customer-service BUSINESS MARKET
```

#### Alternative: Generate Single Documents
```bash
# Generate individual documents (without PRD workflow)
docforge-ai generate "E-commerce platform for handmade crafts" --docs srs
docforge-ai generate "Mobile banking application" --docs architecture
```

#### Legacy: Generate Complete Documentation Set
```bash
# Generate all default documents at once
docforge-ai generate "E-commerce platform for handmade crafts"
docforge-ai generate "Mobile task management app" --docs project_charter,srs,architecture
```

#### List Available Document Types and Aliases
```bash
docforge-ai list-docs
```

This command shows all available document types and their quick aliases for single document generation.

### 🎯 Why Use PRD-First Workflow?

The PRD-first workflow offers several advantages:

1. **Validation Before Expansion**: Review and validate the core requirements and user stories before generating additional documents
2. **Consistency**: All subsequent documents are generated based on the same validated PRD, ensuring consistency across the documentation set
3. **Iterative Improvement**: Easily revise the PRD with additional specifications without regenerating all documents
4. **Cost Effective**: Generate only what you need - start with PRD, validate, then expand
5. **Better Quality**: Documents generated from a validated PRD tend to be more accurate and detailed
6. **User Story Foundation**: PRDs include comprehensive user stories that inform all other documents

**Document Type Aliases (use with --docs flag):**
- `srs` or `prd` → Software Requirements Specification
- `architecture` or `arch` or `hld` → System Architecture
- `low_level_design` or `lld` or `design` → Low-Level Design
- `test_specification` or `test` or `testing` → Test Specification
- `deployment_guide` or `deploy` or `deployment` → Deployment Guide
- `operations_manual` or `ops` or `operations` → Operations Manual
- `business_case` or `business` → Business Case
- `market_requirements` or `market` → Market Requirements
- `vision_brief` or `vision` → Vision Brief
- `project_charter` or `charter` or `project` → Project Charter

#### Check Project Status
```bash
docforge-ai status my-ecommerce-platform
```

#### List All Projects
```bash
docforge-ai list-projects
```

## 📁 Project Structure

```
docforge-ai/
├── docforge-ai.py              # Main CLI interface
├── start_docforge-ai.py        # Interactive startup script
├── docforge-ai/               # Package directory
│   ├── __init__.py
│   └── docforge-ai.py         # Package main module
├── backend/                # Core application logic
│   └── app/
│       ├── core/           # Configuration and settings
│       │   └── simple_config.py
│       ├── models.py       # Data models
│       └── services/       # Business logic services
│           ├── document_agents.py
│           ├── local_storage_service.py
│           └── openai_service.py
├── prompts/                # AI prompt templates
│   ├── charter.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── design.md
│   ├── testing.md
│   ├── deployment.md
│   ├── operations.md
│   ├── business_case.md
│   ├── market_requirements.md
│   └── vision_brief.md
├── storage/                # Local data storage
│   ├── projects/           # Project metadata
│   ├── documents/          # Document metadata
│   └── generated-docs/     # Generated documentation
├── generated-docs/         # User-generated documentation
├── requirements.txt        # Python dependencies
└── .env                    # Configuration file (created by init)
```

## 📖 Usage Examples

### Example 1: Complete Project Documentation
```bash
docforge-ai generate "AI-powered customer service chatbot" --context "React frontend, Node.js backend, PostgreSQL database"
```

### Example 2: Architecture-Focused Documentation
```bash
docforge-ai generate "Microservices e-commerce platform" --docs architecture,deployment_guide,operations_manual
```

### Example 3: Business-Focused Documentation
```bash
docforge-ai generate "SaaS project management tool" --docs business_case,market_requirements,vision_brief
```

### Example 4: Custom Project Name
```bash
docforge-ai generate "Build a mobile app" --name "MyAwesomeApp" --docs srs,architecture
```

## 📂 Document Organization

DocForge-ai organizes your generated documents neatly:

```
generated-docs/
└── your-project-name/
    ├── README.md                    # Project overview and index
    ├── 01_project_charter.md        # Project charter
    ├── 02_srs.md                    # Software requirements
    ├── 03_architecture.md           # System architecture
    ├── 04_test_specification.md     # Test specification
    └── ...                          # Additional documents
```

Each project gets its own directory with:
- **Sequential numbering** for easy navigation
- **README.md** with project overview and document index
- **Clean markdown files** ready for use
- **Metadata tracking** in the storage system

## 🎯 Document Type Selection

When you run `docforge-ai init`, DocForge-ai will show you all available document types:

```
📋 Available Document Types (10):
 1. Project Charter
     Type: project_charter
     Description: Executive-level project overview with business objectives, scope, and timeline

 2. Software Requirements Specification
     Type: srs
     Description: Detailed functional and non-functional requirements with user stories

 3. System Architecture
     Type: architecture
     Description: High-level system design with components, security, and scalability
...
```

You can then generate specific documents using the type names:
```bash
docforge-ai generate "My project" --docs project_charter,srs,architecture
```

## 🔧 Advanced Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `DOCFORGE_GENERATED_DOCS_PATH` | Generated docs directory | `generated-docs` |
| `DOCFORGE_MAX_TOKENS` | Max tokens per document | `3000` |
| `DOCFORGE_DEFAULT_DOCS` | Default document types | `project_charter,srs,architecture,test_specification` |

### Custom Document Types
You can customize the document generation by modifying the prompt templates in the `prompts/` directory.

### Storage Configuration
DocForge-ai uses local file storage by default. All data is stored in:
- `storage/projects/` - Project metadata (JSON files) - Created automatically when first generating documents
- `storage/documents/` - Document metadata (JSON files) - Created automatically when first generating documents
- `generated-docs/` - Generated markdown files organized by project - Created during initialization

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/Venkatesh188/docforge-ai.git
cd docforge-ai

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/Venkatesh188/docforge-ai/wiki)
- **Issues**: [GitHub Issues](https://github.com/Venkatesh188/docforge-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Venkatesh188/docforge-ai/discussions)

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI) for AI agent orchestration
- Powered by [OpenAI](https://openai.com/) for document generation
- Inspired by the need for better software documentation practices

   #crewai>=0.141.0,<1.0.0

---

**Made with ❤️ by the DocForge Community**