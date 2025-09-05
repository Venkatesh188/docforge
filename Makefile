# DocForge-ai Development Makefile

.PHONY: help install install-dev test test-cov lint format type-check security clean build publish docs

# Default target
help:
	@echo "DocForge-ai Development Commands"
	@echo "================================="
	@echo ""
	@echo "Setup:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  setup        Complete development setup"
	@echo ""
	@echo "Testing:"
	@echo "  test         Run all tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  test-quick   Run quick tests only"
	@echo "  test-watch   Run tests in watch mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         Run all linters"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run type checking with mypy"
	@echo "  security     Run security checks"
	@echo "  quality      Run all quality checks"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  build        Build package"
	@echo "  publish      Publish to PyPI (requires PYPI_API_TOKEN)"
	@echo "  docker       Build Docker image"
	@echo ""
	@echo "Utilities:"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Generate documentation"
	@echo "  pre-commit   Install pre-commit hooks"
	@echo "  update-deps  Update dependencies"

# Setup
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e ".[dev]"

setup: install-dev pre-commit
	@echo "Development setup complete!"

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=docforge --cov=backend --cov-report=html --cov-report=term-missing

test-quick:
	pytest tests/ -v -m "not slow"

test-watch:
	pytest-watch tests/ -v

# Code Quality
lint:
	flake8 docforge.py backend/ tests/
	black --check docforge.py backend/ tests/
	isort --check-only docforge.py backend/ tests/
	mypy docforge.py backend/ --ignore-missing-imports

format:
	black docforge.py backend/ tests/
	isort docforge.py backend/ tests/

type-check:
	mypy docforge.py backend/ --ignore-missing-imports

security:
	safety check
	bandit -r docforge.py backend/
	semgrep --config=auto .

quality: lint type-check security
	@echo "All quality checks passed!"

# Build & Deploy
build:
	python -m build

publish: build
	twine upload dist/*

docker:
	docker build -t docforge-ai:latest .

# Utilities
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	@echo "Documentation generation not implemented yet"

pre-commit:
	pre-commit install

update-deps:
	pip-compile requirements.in
	pip-compile requirements-dev.in

# CI/CD helpers
ci-test: install-dev
	pytest tests/ -v --cov=docforge --cov=backend --cov-report=xml

ci-lint: install-dev
	flake8 docforge.py backend/ tests/
	black --check docforge.py backend/ tests/
	isort --check-only docforge.py backend/ tests/

ci-security: install-dev
	safety check
	bandit -r docforge.py backend/

ci-build: install-dev
	python -m build
	twine check dist/*

# Development helpers
dev-install:
	pip install -e ".[dev]"

dev-test:
	pytest tests/ -v --tb=short

dev-format:
	black docforge.py backend/ tests/
	isort docforge.py backend/ tests/

dev-lint:
	ruff check docforge.py backend/ tests/
	ruff check --fix docforge.py backend/ tests/

# Release helpers
version-patch:
	bump2version patch

version-minor:
	bump2version minor

version-major:
	bump2version major

release-check:
	@echo "Checking release readiness..."
	@echo "1. Running tests..."
	make test
	@echo "2. Running linting..."
	make lint
	@echo "3. Running security checks..."
	make security
	@echo "4. Building package..."
	make build
	@echo "Release check complete!"

# Docker helpers
docker-run:
	docker run --rm -it docforge-ai:latest

docker-test:
	docker run --rm docforge-ai:latest python docforge.py --help

# Database helpers (if needed in future)
db-migrate:
	@echo "Database migrations not implemented yet"

db-reset:
	@echo "Database reset not implemented yet"
