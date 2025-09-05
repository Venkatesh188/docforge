# 🛠️ Development Guide

This guide will help you set up a development environment for DocForge-ai and contribute to the project.

## 📋 Prerequisites

- Python 3.10 or higher
- Git
- Make (optional, for using Makefile commands)
- Docker (optional, for containerized development)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Venkatesh188/docforge-ai.git
cd docforge-ai
```

### 2. Set Up Development Environment

```bash
# Using Make (recommended)
make setup

# Or manually
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e ".[dev]"
pre-commit install
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your OpenAI API key
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 4. Run Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run quick tests only
make test-quick
```

## 🏗️ Project Structure

```
docforge-ai/
├── .github/                 # GitHub workflows and templates
│   ├── workflows/          # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── dependabot.yml      # Dependency updates
├── backend/                # Core application logic
│   └── app/
│       ├── core/           # Configuration and settings
│       ├── models.py       # Data models
│       └── services/       # Business logic services
├── docforge/               # Main package
├── prompts/                # AI prompt templates
├── tests/                  # Test suite
├── storage/                # Local data storage
├── generated-docs/         # Generated documentation
├── .pre-commit-config.yaml # Pre-commit hooks
├── pyproject.toml          # Project configuration
├── Makefile               # Development commands
└── README.md              # Project documentation
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cli.py

# Run tests with coverage
pytest --cov=docforge --cov=backend

# Run tests in watch mode
pytest-watch

# Run only quick tests
pytest -m "not slow"
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **CLI Tests**: Test command-line interface
- **API Tests**: Test API endpoints (if any)

### Writing Tests

1. Create test files in the `tests/` directory
2. Use descriptive test names
3. Follow the AAA pattern (Arrange, Act, Assert)
4. Use fixtures for common setup
5. Mock external dependencies

Example test:

```python
def test_document_creation(temp_dir, sample_document_data):
    """Test document creation functionality"""
    # Arrange
    storage = LocalStorageService(base_dir=temp_dir)
    
    # Act
    doc_id = storage.create_document(sample_document_data)
    
    # Assert
    assert doc_id is not None
    assert storage.documents_dir.exists()
```

## 🔧 Code Quality

### Linting and Formatting

```bash
# Run all linters
make lint

# Format code
make format

# Type checking
make type-check

# Security checks
make security

# Run all quality checks
make quality
```

### Pre-commit Hooks

Pre-commit hooks run automatically on each commit:

```bash
# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Use type hints for all functions
- Write docstrings for all public functions
- Keep line length under 88 characters

## 🚀 CI/CD Pipeline

### Workflow Overview

1. **Quick Check** (PRs): Fast validation
2. **Test Suite**: Comprehensive testing across platforms
3. **Security Scan**: Vulnerability and security checks
4. **Package Test**: Build and validate package
5. **Docker Build**: Container testing
6. **Performance Test**: Performance benchmarking
7. **Publish**: PyPI publication (on release)

### Local CI Simulation

```bash
# Simulate CI test pipeline
make ci-test

# Simulate CI lint pipeline
make ci-lint

# Simulate CI security pipeline
make ci-security

# Simulate CI build pipeline
make ci-build
```

## 📦 Building and Publishing

### Building Package

```bash
# Build package
make build

# Check package
twine check dist/*

# Test package installation
pip install dist/*.whl
```

### Publishing to PyPI

```bash
# Set up PyPI token
export PYPI_API_TOKEN=your_pypi_token

# Publish package
make publish
```

### Version Management

```bash
# Patch version (2.0.3 -> 2.0.4)
make version-patch

# Minor version (2.0.3 -> 2.1.0)
make version-minor

# Major version (2.0.3 -> 3.0.0)
make version-major
```

## 🐳 Docker Development

### Building Docker Image

```bash
# Build image
make docker

# Run container
make docker-run

# Test container
make docker-test
```

### Docker Compose (if needed)

```yaml
version: '3.8'
services:
  docforge-ai:
    build: .
    volumes:
      - .:/app
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    command: python docforge.py --help
```

## 🔍 Debugging

### Debug Mode

```bash
# Run with debug logging
PYTHONPATH=. python -m pdb docforge.py --help

# Run with verbose output
python docforge.py --verbose --help
```

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH includes project root
2. **API Key Issues**: Check .env file configuration
3. **Permission Errors**: Check file permissions in storage directory
4. **Memory Issues**: Monitor memory usage during document generation

## 📚 Documentation

### Generating Documentation

```bash
# Generate API documentation
make docs

# Update README
# Edit README.md manually
```

### Documentation Standards

- Use clear, concise language
- Include code examples
- Update documentation with code changes
- Use markdown formatting consistently

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new functionality
5. Run quality checks
6. Submit a pull request

### Pull Request Guidelines

- Use descriptive commit messages
- Include tests for new features
- Update documentation as needed
- Follow the PR template
- Ensure all CI checks pass

### Code Review Process

1. Automated checks must pass
2. At least one reviewer approval required
3. Address all review comments
4. Maintain test coverage above 80%

## 🐛 Troubleshooting

### Common Problems

**Problem**: Import errors when running tests
**Solution**: Ensure PYTHONPATH includes project root

**Problem**: Pre-commit hooks failing
**Solution**: Run `pre-commit run --all-files` to fix issues

**Problem**: Tests failing on different Python versions
**Solution**: Check Python version compatibility in pyproject.toml

**Problem**: Docker build failing
**Solution**: Check Dockerfile syntax and base image availability

### Getting Help

- Check existing issues on GitHub
- Create a new issue with detailed description
- Join discussions in GitHub Discussions
- Review the troubleshooting guide

## 📊 Performance

### Benchmarking

```bash
# Run performance tests
pytest tests/ --benchmark-only

# Profile memory usage
python -m memory_profiler docforge.py generate "test project"
```

### Optimization Tips

- Use async/await for I/O operations
- Cache frequently accessed data
- Minimize API calls to OpenAI
- Use efficient data structures
- Profile code regularly

## 🔒 Security

### Security Best Practices

- Never commit API keys or secrets
- Use environment variables for configuration
- Regularly update dependencies
- Run security scans before releases
- Follow OWASP guidelines

### Security Tools

- **Safety**: Dependency vulnerability scanning
- **Bandit**: Python security linting
- **Semgrep**: Static analysis security testing
- **Pre-commit**: Automated security checks

## 📈 Monitoring

### Health Checks

```bash
# Run health check
make health-check

# Check system status
python docforge.py status
```

### Logging

- Use structured logging
- Include relevant context
- Set appropriate log levels
- Rotate logs regularly

## 🎯 Future Improvements

### Planned Features

- [ ] Web interface
- [ ] Plugin system
- [ ] Advanced templates
- [ ] Team collaboration
- [ ] Version control integration

### Technical Debt

- [ ] Improve test coverage
- [ ] Refactor legacy code
- [ ] Optimize performance
- [ ] Enhance error handling
- [ ] Improve documentation

---

**Happy coding! 🚀**

For more information, see the [main README](README.md) or [API documentation](docs/API_REFERENCE.md).
