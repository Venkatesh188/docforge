# Contributing to DocForge

Thank you for your interest in contributing to DocForge! We welcome contributions from everyone and are grateful for every contribution, no matter how small.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/docforge-ai-opensource.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes: `docforge-ai generate "test project"`
6. Commit and push: `git commit -m "Add your feature" && git push origin feature/your-feature-name`
7. Open a Pull Request

## 🎯 Ways to Contribute

### 🚀 **High Impact Contributions**

#### 1. **Custom Document Templates**
Create industry-specific templates for:
- **Fintech** - Banking, payments, financial services
- **Healthcare** - HIPAA-compliant, medical device documentation  
- **E-commerce** - Marketplace, retail, subscription services
- **Gaming** - Game design documents, technical specifications
- **IoT** - Hardware/software integration, device specifications

**How to add a template:**
1. Create a new prompt file in `prompts/`
2. Add the document type to `backend/app/models.py`
3. Configure the agent in `backend/app/services/document_agents.py`
4. Test with real examples

#### 2. **Multiple AI Providers**
Extend support beyond OpenAI:
- **Anthropic Claude** - For detailed, analytical documents
- **Google Gemini** - For creative and diverse content
- **Local Models** - Ollama, LM Studio integration
- **Azure OpenAI** - For enterprise deployments

#### 3. **Export Formats**
- **PDF Generation** - Professional PDF output
- **Word Documents** - .docx format for corporate environments
- **HTML** - Interactive web documentation
- **Confluence** - Direct publishing to Atlassian Confluence

### 📝 **Documentation Contributions**

#### Examples & Tutorials
- **Video tutorials** showing DocForge in action
- **Industry-specific examples** with real project ideas
- **Best practices guide** for different project types
- **Integration tutorials** with popular development tools

#### Internationalization
- **Multi-language support** for generated documents
- **Translated prompts** for different languages
- **Localized examples** for different regions

### 🐛 **Bug Fixes & Improvements**

- **Performance optimizations** for document generation
- **Error handling improvements** with better error messages
- **CLI enhancements** for better user experience
- **Code quality improvements** following Python best practices

## 📋 Development Guidelines

### Code Style

We follow Python best practices:

```python
# Good: Clear, descriptive names
def generate_project_charter(project_idea: str, context: str) -> Dict[str, Any]:
    """Generate a project charter document."""
    pass

# Bad: Unclear names
def gen_doc(idea: str) -> dict:
    pass
```

### Testing

Before submitting a PR:

1. **Test document generation**:
   ```bash
   docforge-ai generate "Test project" --docs project_charter
   ```

2. **Test CLI commands**:
   ```bash
   docforge-ai list-docs
   docforge-ai list-projects
   ```

3. **Check for errors**:
   ```bash
   python -m py_compile docforge-ai.py
   ```

### Commit Messages

Use clear, descriptive commit messages:

```
✅ Good:
feat: Add support for Claude AI provider
fix: Handle OpenAI API timeout errors gracefully
docs: Add examples for e-commerce projects

❌ Bad:
Update stuff
Fix bug
Changes
```

## 🎨 Template Development

### Creating a New Document Template

1. **Create the prompt file** (`prompts/YourDocumentType_Prompt.md`):

```markdown
# Your Document Type Generator

You are an expert [ROLE] who creates professional [DOCUMENT TYPE] documents.

## Context
- Project: {project_name}
- Idea: {initial_idea}
- Additional Context: {additional_context}

## Requirements
- Professional tone
- Industry-standard format
- Complete sections with no placeholders
- Actionable recommendations

## Template Structure
[Your template structure here]
```

2. **Add to models** (`backend/app/models.py`):

```python
class DocumentType(str, Enum):
    # ... existing types
    YOUR_NEW_TYPE = "your_new_type"
```

3. **Configure the agent** (`backend/app/services/document_agents.py`):

```python
DocumentType.YOUR_NEW_TYPE: {
    "role": "Expert Role",
    "goal": "Generate professional your-new-type documentation",
    "prompt_file": "YourDocumentType_Prompt.md",
    "max_tokens": 2500
},
```

4. **Test thoroughly**:
   ```bash
   docforge-ai generate "Test project" --docs your_new_type
   ```

### Template Best Practices

- ✅ **Clear section headers** for easy navigation
- ✅ **Professional language** appropriate for business use
- ✅ **Complete content** with no TODO items or placeholders
- ✅ **Consistent formatting** with other DocForge documents
- ✅ **Industry standards** following recognized best practices

## 🤖 AI Provider Integration

### Adding a New AI Provider

1. **Create provider class** (`backend/app/providers/your_provider.py`):

```python
class YourProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def generate_content(self, prompt: str, context: dict) -> dict:
        # Implementation here
        pass
```

2. **Add provider configuration**:
   - Update settings to include new provider options
   - Add environment variable handling
   - Include in CLI provider selection

3. **Test with different document types**:
   - Ensure consistent quality across all document types
   - Test error handling and timeout scenarios
   - Verify metadata compatibility

## 📝 Issue Templates

### Bug Report
- **Description**: Clear description of the issue
- **Steps to Reproduce**: Exact commands that cause the issue
- **Expected vs Actual**: What should happen vs what happens
- **Environment**: Python version, OS, DocForge version
- **Logs**: Any error messages or logs

### Feature Request
- **Problem**: What problem does this solve?
- **Solution**: Proposed solution or implementation
- **Alternatives**: Other solutions considered
- **Use Case**: Real-world scenario where this would be helpful

### Template Request
- **Industry/Domain**: What industry is this for?
- **Document Type**: What type of document is needed?
- **Requirements**: Specific sections or content needed
- **Examples**: Links to similar documents or standards

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** - All contributors listed
- **Release Notes** - Major contributions highlighted
- **GitHub Contributors** - Automatic GitHub recognition
- **Documentation** - Contributors credited in relevant sections

## 📞 Getting Help

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Documentation** - Check existing docs first
- **Code Examples** - Look at existing implementations

## 🎯 Current Priority Areas

We're particularly looking for help with:

1. **Document Templates** - Industry-specific templates
2. **AI Providers** - Support for more AI services
3. **Export Formats** - PDF, Word, HTML generation
4. **Performance** - Faster document generation
5. **Error Handling** - Better error messages and recovery

## 📜 Code of Conduct

- **Be respectful** - Treat everyone with kindness and respect
- **Be inclusive** - Welcome contributors from all backgrounds
- **Be collaborative** - Help others learn and grow
- **Be constructive** - Provide helpful feedback and suggestions

## 🎉 Thank You!

Every contribution helps make DocForge better for everyone. Whether you're fixing a typo, adding a new feature, or helping with documentation, your efforts are appreciated!

---

*Happy contributing! 🚀*
