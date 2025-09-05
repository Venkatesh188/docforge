#!/usr/bin/env python3
"""
Service layer tests for DocForge functionality
"""

import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.services.local_storage_service import LocalStorageService
from app.services.openai_service import OpenAIService
from app.models import DocumentType

class TestLocalStorageService:
    """Test local storage service"""

    def test_storage_initialization(self):
        """Test storage service initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = LocalStorageService(base_dir=Path(temp_dir))
            
            assert storage.base_dir == Path(temp_dir)
            assert storage.projects_dir.exists()
            assert storage.documents_dir.exists()

    def test_storage_info(self):
        """Test storage info retrieval"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = LocalStorageService(base_dir=Path(temp_dir))
            info = storage.get_storage_info()
            
            assert 'base_directory' in info
            assert 'projects_count' in info
            assert 'documents_count' in info
            assert info['projects_count'] == 0
            assert info['documents_count'] == 0

    def test_project_creation(self):
        """Test project creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = LocalStorageService(base_dir=Path(temp_dir))
            
            project_data = {
                'name': 'test-project',
                'description': 'A test project',
                'created_at': '2024-01-01T00:00:00Z'
            }
            
            project_id = storage.create_project(project_data)
            assert project_id is not None
            
            # Check if project file exists
            project_file = storage.projects_dir / f"{project_id}.json"
            assert project_file.exists()

    def test_document_creation(self):
        """Test document creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = LocalStorageService(base_dir=Path(temp_dir))
            
            document_data = {
                'project_id': 'test-project-id',
                'type': DocumentType.SRS,
                'content': 'Test document content',
                'created_at': '2024-01-01T00:00:00Z'
            }
            
            doc_id = storage.create_document(document_data)
            assert doc_id is not None
            
            # Check if document file exists
            doc_file = storage.documents_dir / f"{doc_id}.json"
            assert doc_file.exists()

class TestOpenAIService:
    """Test OpenAI service"""

    @patch('app.services.openai_service.OpenAI')
    def test_openai_initialization(self, mock_openai):
        """Test OpenAI service initialization"""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        service = OpenAIService(api_key="test-key")
        assert service.client is not None

    @patch('app.services.openai_service.OpenAI')
    def test_generate_content(self, mock_openai):
        """Test content generation"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated content"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        service = OpenAIService(api_key="test-key")
        result = service.generate_content("Test prompt", "test-model")
        
        assert result == "Generated content"
        mock_client.chat.completions.create.assert_called_once()

    def test_invalid_api_key(self):
        """Test handling of invalid API key"""
        with pytest.raises(ValueError):
            OpenAIService(api_key="")

    def test_missing_api_key(self):
        """Test handling of missing API key"""
        with pytest.raises(ValueError):
            OpenAIService(api_key=None)
