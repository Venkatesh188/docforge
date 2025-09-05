#!/usr/bin/env python3
"""
Pytest configuration and fixtures for DocForge tests
"""

import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_path:
        yield Path(temp_path)

@pytest.fixture
def mock_openai():
    """Mock OpenAI service"""
    with patch('app.services.openai_service.OpenAI') as mock:
        mock_client = mock.return_value
        mock_response = mock_client.chat.completions.create.return_value
        mock_response.choices = [mock_response.choices[0] if hasattr(mock_response, 'choices') else type('MockChoice', (), {
            'message': type('MockMessage', (), {'content': 'Generated content'})()
        })()]
        yield mock

@pytest.fixture
def mock_settings():
    """Mock settings configuration"""
    with patch('app.core.simple_config.SimpleSettings') as mock:
        mock_instance = mock.return_value
        mock_instance.validate_config.return_value = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        mock_instance.app_name = 'DocForge-ai'
        mock_instance.app_version = '2.0.3'
        yield mock_instance

@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        'name': 'test-project',
        'description': 'A test project for documentation generation',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    }

@pytest.fixture
def sample_document_data():
    """Sample document data for testing"""
    return {
        'project_id': 'test-project-id',
        'type': 'srs',
        'title': 'Software Requirements Specification',
        'content': 'Test document content',
        'created_at': '2024-01-01T00:00:00Z',
        'updated_at': '2024-01-01T00:00:00Z'
    }
