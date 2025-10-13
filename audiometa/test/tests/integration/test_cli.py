"""Tests for CLI functionality."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from audiometa.cli import main, format_output, format_as_table


class TestCLI:
    
    def test_format_output_json(self):
        data = {"title": "Test Song", "artist": "Test Artist"}
        result = format_output(data, "json")
        parsed = json.loads(result)
        assert parsed == data
    
    def test_format_output_yaml(self):
        data = {"title": "Test Song", "artist": "Test Artist"}
        result = format_output(data, "yaml")
        # Should fall back to JSON if PyYAML not available
        assert "Test Song" in result
    
    def test_format_output_table(self):
        data = {
            "unified_metadata": {"title": "Test Song", "artist": "Test Artist"},
            "technical_info": {"duration_seconds": 180, "bitrate_kbps": 320}
        }
        result = format_as_table(data)
        assert "Test Song" in result
        assert "Test Artist" in result
        assert "180" in result
        assert "320" in result
    
    def test_cli_help(self):
        """Test that CLI shows help when no arguments provided."""
        result = subprocess.run([sys.executable, "-m", "audiometa"], 
                              capture_output=True, text=True)
        assert result.returncode == 1  # Should exit with error
        assert "usage:" in result.stdout.lower() or "help" in result.stdout.lower()
    
    def test_cli_read_help(self):
        """Test that read command shows help."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "read" in result.stdout.lower()
    
    def test_cli_unified_help(self):
        """Test that unified command shows help."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "unified", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "unified" in result.stdout.lower()
    
    def test_cli_write_help(self):
        """Test that write command shows help."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "write" in result.stdout.lower()
    
    def test_cli_delete_help(self):
        """Test that delete command shows help."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "delete", "--help"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "delete" in result.stdout.lower()
    
    def test_cli_read_nonexistent_file(self, tmp_path):
        """Test CLI error handling for nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.mp3"
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", str(nonexistent_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "error" in result.stderr.lower()
    
    def test_cli_read_with_continue_on_error(self, tmp_path):
        """Test CLI continues on error when flag is set."""
        nonexistent_file = tmp_path / "nonexistent.mp3"
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(nonexistent_file), "--continue-on-error"], 
                              capture_output=True, text=True)
        # Should not exit with error when continue-on-error is set
        assert result.returncode == 0
    
    def test_cli_write_no_metadata(self, sample_mp3_file):
        """Test CLI write command with no metadata fields."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", str(sample_mp3_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 1
        assert "no metadata fields specified" in result.stderr.lower()
    
    def test_cli_write_basic_metadata(self, sample_mp3_file):
        """Test CLI write command with basic metadata."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "write", 
                               str(sample_mp3_file), "--title", "CLI Test Title"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Updated metadata" in result.stdout
    
    def test_cli_unified_output(self, sample_mp3_file):
        """Test CLI unified command output."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "unified", 
                               str(sample_mp3_file), "--format", "json"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        # Should output valid JSON
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
    
    def test_cli_read_output_formats(self, sample_mp3_file):
        """Test CLI read command with different output formats."""
        # Test JSON format
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(sample_mp3_file), "--format", "json"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "unified_metadata" in data
        
        # Test table format
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(sample_mp3_file), "--format", "table"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "UNIFIED METADATA" in result.stdout or "TECHNICAL INFO" in result.stdout
    
    def test_cli_output_to_file(self, sample_mp3_file, tmp_path):
        """Test CLI output to file."""
        output_file = tmp_path / "metadata.json"
        result = subprocess.run([sys.executable, "-m", "audiometa", "read", 
                               str(sample_mp3_file), "--output", str(output_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert output_file.exists()
        
        # Verify file contains valid JSON
        with open(output_file) as f:
            data = json.load(f)
        assert isinstance(data, dict)
    
    def test_cli_delete_metadata(self, sample_mp3_file):
        """Test CLI delete command."""
        result = subprocess.run([sys.executable, "-m", "audiometa", "delete", 
                               str(sample_mp3_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Deleted all metadata" in result.stdout or "No metadata found" in result.stdout
