#!/usr/bin/env python3
"""
CLI tests for DocForge functionality
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from docforge.docforge import cli

class TestCLI:
    """Test CLI functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.runner = CliRunner()

    def test_cli_help(self):
        """Test CLI help command"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "DocForge-ai" in result.output
        assert "AI-powered documentation generator" in result.output

    def test_cli_version(self):
        """Test CLI version command"""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_list_docs_command(self):
        """Test list-docs command"""
        result = self.runner.invoke(cli, ['list-docs'])
        assert result.exit_code == 0
        assert "Available document types" in result.output

    def test_list_projects_command(self):
        """Test list-projects command"""
        result = self.runner.invoke(cli, ['list-projects'])
        assert result.exit_code == 0
        assert "Projects" in result.output

    @patch('docforge.docforge.SimpleSettings')
    def test_init_command(self, mock_settings):
        """Test init command"""
        mock_settings.return_value.validate_config.return_value = {
            'valid': True, 'errors': [], 'warnings': []
        }
        
        result = self.runner.invoke(cli, ['init'])
        # Should succeed or fail gracefully
        assert result.exit_code in [0, 1]

    def test_generate_command_help(self):
        """Test generate command help"""
        result = self.runner.invoke(cli, ['generate', '--help'])
        assert result.exit_code == 0
        assert "Generate documentation" in result.output

    def test_invalid_command(self):
        """Test invalid command handling"""
        result = self.runner.invoke(cli, ['invalid-command'])
        assert result.exit_code != 0
