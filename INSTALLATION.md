# DocForge Installation Guide

This guide will help you install and configure DocForge on your system.

## Prerequisites

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **OpenAI API Key** - [Get your API key](https://platform.openai.com/api-keys)
- **Git** (for cloning) - [Download Git](https://git-scm.com/downloads)

## Installation Methods

### Method 1: Direct Installation (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize DocForge**
```bash
docforge-ai init
```

4. **Configure your API key**
   - Edit the `.env` file created during initialization
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

### Method 2: Package Installation

1. **Clone and install as package**
```bash
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource
pip install .
```

2. **Initialize DocForge**
```bash
docforge-ai init
```

3. **Configure your API key**
   - Edit the `.env` file with your OpenAI API key

### Method 3: Development Installation

1. **Clone and install in development mode**
```bash
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource
pip install -e .
```

2. **Install development dependencies**
```bash
pip install -e ".[dev]"
```

## Configuration

### Step 1: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 2: Configure DocForge

1. **Run initialization** (if not done already):
```bash
docforge-ai init
```

2. **Edit the `.env` file**:
```bash
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional (defaults shown)
OPENAI_MODEL=gpt-4o-mini
DOCFORGE_GENERATED_DOCS_PATH=generated-docs
DOCFORGE_MAX_TOKENS=3000
DOCFORGE_DEFAULT_DOCS=project_charter,srs,architecture,test_specification
```

### Step 3: Verify Installation

```bash
# Check if DocForge is working
docforge-ai list-docs

# Should show all available document types
```

## First Usage

### Interactive Mode (Recommended for beginners)

```bash
python start_docforge-ai.py
```

This will guide you through:
- Checking your configuration
- Showing available document types
- Helping you generate your first document

### Command Line Usage

```bash
# Generate complete documentation set
docforge-ai generate "My awesome project idea"

# Generate specific document types
docforge-ai generate "E-commerce platform" --docs project_charter,srs,architecture

# List all available document types
docforge-ai list-docs

# Check project status
docforge-ai status my-project-name

# List all your projects
docforge-ai list-projects
```

## Troubleshooting

### Common Issues

#### 1. "OpenAI API key is required" Error
- **Solution**: Make sure you've set your API key in the `.env` file
- **Check**: Verify the key starts with `sk-` and is not wrapped in quotes

#### 2. "Module not found" Error
- **Solution**: Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

#### 3. "Permission denied" Error
- **Solution**: Make sure you have write permissions in the current directory
- **Alternative**: Run with appropriate permissions or change directory

#### 4. "Python version not supported" Error
- **Solution**: Upgrade to Python 3.10 or higher
- **Check version**: `python --version`

### Getting Help

1. **Check the logs**: Look for error messages in the terminal output
2. **Verify configuration**: Run `docforge-ai init` to check setup
3. **Test API key**: Make sure your OpenAI API key is valid and has credits
4. **Check dependencies**: Ensure all required packages are installed

### Support Channels

- **GitHub Issues**: [Report bugs or request features](https://github.com/docforge-ai-community/docforge-ai-opensource/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/docforge-ai-community/docforge-ai-opensource/discussions)
- **Documentation**: [Wiki](https://github.com/docforge-ai-community/docforge-ai-opensource/wiki)

## Uninstallation

To remove DocForge:

```bash
# If installed as package
pip uninstall docforge-ai

# Remove local files
rm -rf docforge-ai-opensource/
rm -rf storage/
rm -rf generated-docs/
rm .env
```

## Updating DocForge

To update to the latest version:

```bash
# Navigate to DocForge directory
cd docforge-ai-opensource

# Pull latest changes
git pull origin main

# Reinstall if needed
pip install -r requirements.txt
```

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Internet**: Required for OpenAI API calls

### Recommended Requirements
- **OS**: Latest version of Windows, macOS, or Linux
- **Python**: 3.11 or higher
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **Internet**: Stable broadband connection

## Security Notes

- **API Key Security**: Never share your OpenAI API key or commit it to version control
- **Local Storage**: All data is stored locally on your machine
- **No External Dependencies**: DocForge doesn't send data to external services except OpenAI
- **Environment Variables**: Use `.env` file for configuration (already in `.gitignore`)

## Next Steps

After successful installation:

1. **Read the [README](README.md)** for detailed usage instructions
2. **Try the [examples](examples/)** to see DocForge in action
3. **Check the [API Reference](docs/API_REFERENCE.md)** for advanced usage
4. **Join the community** on GitHub Discussions

Happy documenting! 🚀
