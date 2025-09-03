#!/usr/bin/env python3
"""
Basic tests for DocForge functionality

These tests verify that the core DocForge functionality works correctly
without requiring API keys or external services.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add the backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

def test_import_core_modules():
    """Test that core modules can be imported without errors"""
    try:
        from app.core.simple_config import SimpleSettings, settings
        from app.services.local_storage_service import LocalStorageService
        from app.models import DocumentType
        print("✅ Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        return False

def test_simple_config():
    """Test configuration management"""
    try:
        from app.core.simple_config import SimpleSettings
        
        # Test settings creation
        config = SimpleSettings()
        assert hasattr(config, 'app_name')
        assert hasattr(config, 'app_version')
        assert hasattr(config, 'storage_path')
        
        # Test validation method
        validation = config.validate_config()
        assert 'valid' in validation
        assert 'errors' in validation
        assert 'warnings' in validation
        
        print("✅ Configuration system working correctly")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_local_storage():
    """Test local storage service"""
    try:
        from app.services.local_storage_service import LocalStorageService
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = LocalStorageService(base_dir=Path(temp_dir))
            
            # Test that directories are created
            assert storage.projects_dir.exists()
            assert storage.documents_dir.exists()
            
            # Test storage info
            info = storage.get_storage_info()
            assert 'base_directory' in info
            assert 'projects_count' in info
            
        print("✅ Local storage service working correctly")
        return True
    except Exception as e:
        print(f"❌ Local storage test failed: {e}")
        return False

def test_document_types():
    """Test document type enumeration"""
    try:
        from app.models import DocumentType
        
        # Test that document types are defined
        doc_types = list(DocumentType)
        assert len(doc_types) > 0
        
        # Test specific document types
        assert DocumentType.PROJECT_CHARTER in doc_types
        assert DocumentType.SRS in doc_types
        
        print(f"✅ Document types available: {len(doc_types)} types")
        return True
    except Exception as e:
        print(f"❌ Document types test failed: {e}")
        return False

def test_cli_import():
    """Test that the CLI module can be imported"""
    try:
        import docforge
        print("✅ CLI module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import CLI module: {e}")
        return False

def test_prompt_files():
    """Test that prompt files exist"""
    try:
        prompts_dir = Path(__file__).parent.parent / "prompts"
        if not prompts_dir.exists():
            print("❌ Prompts directory not found")
            return False
        
        prompt_files = list(prompts_dir.glob("*.md"))
        if len(prompt_files) == 0:
            print("❌ No prompt files found")
            return False
        
        print(f"✅ Found {len(prompt_files)} prompt files")
        return True
    except Exception as e:
        print(f"❌ Prompt files test failed: {e}")
        return False

def run_all_tests():
    """Run all basic tests"""
    print("🧪 Running DocForge Basic Tests")
    print("=" * 50)
    
    tests = [
        ("Core Module Import", test_import_core_modules),
        ("Configuration System", test_simple_config),
        ("Local Storage Service", test_local_storage),
        ("Document Types", test_document_types),
        ("CLI Import", test_cli_import),
        ("Prompt Files", test_prompt_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DocForge is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check your installation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
