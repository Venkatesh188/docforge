# 🔧 DocForge Installation Guide

This guide provides detailed installation instructions for DocForge on different platforms and environments.

## 📋 System Requirements

### **Minimum Requirements**
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended for better performance)
- **Storage**: 2GB free space
- **Internet**: Required for AI model API calls

### **Supported Platforms**
- **Windows**: Windows 10/11
- **macOS**: macOS 10.15 (Catalina) or later
- **Linux**: Ubuntu 18.04+, CentOS 7+, or equivalent

### **Python Version Support**
| Python Version | Status | Notes |
|----------------|--------|-------|
| 3.8 | ✅ Supported | Minimum version |
| 3.9 | ✅ Supported | Recommended |
| 3.10 | ✅ Supported | Recommended |
| 3.11 | ✅ Supported | Best performance |
| 3.12 | ✅ Supported | Latest features |

## 🚀 Installation Methods

### **Method 1: PyPI (Recommended)**

```bash
# Install from PyPI (when published)
pip install docforge-ai-opensource

# Initialize and run
docforge-ai init
docforge-ai generate "Your project idea"
```

### **Method 2: Git Clone (Development)**

```bash
# Clone the repository
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource

# Create virtual environment (recommended)
python -m venv docforge-ai-env
source docforge-ai-env/bin/activate  # On Windows: docforge-ai-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize DocForge
docforge-ai init
```

### **Method 3: Docker (Containerized)**

```bash
# Clone the repository
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource

# Build Docker image
docker build -t docforge-ai .

# Run DocForge in container
docker run -v $(pwd)/generated-docs:/app/generated-docs \
           -v $(pwd)/.env:/app/.env \
           docforge-ai docforge-ai generate "Your project idea"
```

## 🛠️ Platform-Specific Instructions

### **Windows Installation**

#### **Option A: Using Command Prompt**
```cmd
# Check Python version
python --version

# Clone repository
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize
docforge-ai init
```

#### **Option B: Using PowerShell**
```powershell
# Set execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Follow same steps as Command Prompt
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
docforge-ai init
```

#### **Windows Troubleshooting**
- **Python not found**: Install Python from [python.org](https://python.org) or Microsoft Store
- **Git not found**: Install Git from [git-scm.com](https://git-scm.com)
- **Permission errors**: Run Command Prompt as Administrator
- **Path issues**: Add Python to your system PATH environment variable

### **macOS Installation**

#### **Using Homebrew (Recommended)**
```bash
# Install Python (if not already installed)
brew install python

# Clone repository
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize
docforge-ai init
```

#### **Using System Python**
```bash
# Check Python version
python3 --version

# Follow same steps, using python3 instead of python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docforge-ai init
```

#### **macOS Troubleshooting**
- **Xcode Command Line Tools**: Run `xcode-select --install` if needed
- **Homebrew issues**: Reinstall with `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- **Permission issues**: Use `sudo` carefully, prefer virtual environments
- **M1/M2 Macs**: All dependencies are compatible with Apple Silicon

### **Linux Installation**

#### **Ubuntu/Debian**
```bash
# Update package manager
sudo apt update

# Install Python and pip (if not installed)
sudo apt install python3 python3-pip python3-venv git

# Clone repository
git clone https://github.com/docforge-ai-community/docforge-ai-opensource.git
cd docforge-ai-opensource

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize
docforge-ai init
```

#### **CentOS/RHEL/Fedora**
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip git
# or for newer versions: sudo dnf install python3 python3-pip git

# Fedora
sudo dnf install python3 python3-pip git

# Follow same steps as Ubuntu
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docforge-ai init
```

#### **Linux Troubleshooting**
- **Package not found**: Update package manager or use alternative package names
- **Permission denied**: Ensure user has write permissions to installation directory
- **SSL certificate errors**: Update ca-certificates package
- **Virtual environment issues**: Install python3-venv package separately

## 🔑 Configuration Setup

### **1. OpenAI API Key Setup**

After installation, you need to configure your OpenAI API key:

```bash
# Initialize DocForge (creates .env file)
docforge-ai init

# Edit .env file with your preferred editor
nano .env
# or
vim .env
# or on Windows
notepad .env
```

Add your API key to the `.env` file:
```bash
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_MODEL=gpt-4
```

### **2. Get OpenAI API Key**

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (you won't see it again)
5. Add billing information to your OpenAI account
6. Start with a small credit amount ($10-20) for testing

### **3. Verify Installation**

```bash
# Test basic functionality
docforge-ai list-docs

# Test configuration
docforge-ai generate "Test project for verification" --docs project_charter

# Check generated files
ls generated-docs/
```

## 🐳 Docker Setup (Advanced)

### **Creating Dockerfile**

If you want to containerize DocForge:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash docforge-ai
RUN chown -R docforge-ai:docforge-ai /app
USER docforge-ai

# Create directories
RUN mkdir -p generated-docs storage

# Set environment
ENV PYTHONPATH=/app
ENV DOCFORGE_CLI_MODE=true

# Default command
CMD ["python", "docforge-ai.py", "--help"]
```

### **Docker Compose Setup**

```yaml
version: '3.8'
services:
  docforge-ai:
    build: .
    volumes:
      - ./generated-docs:/app/generated-docs
      - ./storage:/app/storage
      - ./.env:/app/.env
    environment:
      - PYTHONPATH=/app
      - DOCFORGE_CLI_MODE=true
    working_dir: /app
```

## 🚨 Troubleshooting Common Issues

### **Installation Issues**

#### **"Python not found" Error**
```bash
# Check if Python is installed
python --version
python3 --version

# If not found, install Python:
# Windows: Download from python.org
# macOS: brew install python
# Linux: sudo apt install python3
```

#### **"pip not found" Error**
```bash
# Install pip
python -m ensurepip --upgrade

# Or install separately:
# Windows: included with Python installer
# macOS: brew install python (includes pip)
# Linux: sudo apt install python3-pip
```

#### **Permission Denied Errors**
```bash
# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Or install with user flag
pip install --user -r requirements.txt
```

### **Runtime Issues**

#### **OpenAI API Errors**
```bash
# Check API key configuration
python -c "import os; print('OPENAI_API_KEY' in os.environ)"

# Verify API key format (starts with sk-)
python -c "import os; key=os.getenv('OPENAI_API_KEY'); print('Valid format' if key and key.startswith('sk-') else 'Invalid format')"

# Test API connectivity
python -c "import openai; openai.api_key='your-key'; print('API key works' if openai.Model.list() else 'API key failed')"
```

#### **Module Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### **File Permission Errors**
```bash
# Check directory permissions
ls -la generated-docs/
ls -la storage/

# Fix permissions
chmod 755 generated-docs/ storage/
```

### **Performance Issues**

#### **Slow Document Generation**
- Use gpt-3.5-turbo for faster (but lower quality) generation
- Reduce concurrent generations in configuration
- Check internet connection speed
- Monitor OpenAI API rate limits

#### **Memory Issues**
- Close other applications
- Use smaller batch sizes
- Consider upgrading system RAM
- Use swap space on Linux/macOS

## 📊 Verification Checklist

After installation, verify everything works:

- [ ] Python 3.8+ installed and accessible
- [ ] DocForge repository cloned successfully
- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] OpenAI API key configured in `.env` file
- [ ] `docforge-ai.py init` runs without errors
- [ ] `docforge-ai.py list-docs` shows available document types
- [ ] Test document generation completes successfully
- [ ] Generated files appear in `generated-docs/` directory

## 💡 Next Steps

Once installation is complete:

1. **Read the [Quick Start Guide](../README.md#quick-start)**
2. **Explore [Examples](../examples/README.md)**
3. **Try generating your first documentation**
4. **Join our [Community Discussions](https://github.com/docforge-ai-community/docforge-ai-opensource/discussions)**

## 🆘 Getting Help

If you encounter issues not covered here:

1. **Check [GitHub Issues](https://github.com/docforge-ai-community/docforge-ai-opensource/issues)** for known problems
2. **Search [GitHub Discussions](https://github.com/docforge-ai-community/docforge-ai-opensource/discussions)** for community help
3. **Create a new issue** with detailed error messages and system information
4. **Include the following in bug reports**:
   - Operating system and version
   - Python version
   - Full error message
   - Steps to reproduce the issue

---

**Need more help?** Join our community discussions or create an issue on GitHub. We're here to help you get DocForge running smoothly!
