"""Unit tests for AudioFile class basic functionality."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.unit
class TestAudioFile:
    """Unit test cases for AudioFile class basic functionality."""

    def test_audio_file_with_string_path(self, sample_mp3_file: Path):
        """Test AudioFile initialization with string path."""
        audio_file = AudioFile(str(sample_mp3_file))
        assert audio_file.file_path == str(sample_mp3_file)
        assert audio_file.file_extension == ".mp3"

    def test_audio_file_with_path_object(self, sample_mp3_file: Path):
        """Test AudioFile initialization with Path object."""
        audio_file = AudioFile(sample_mp3_file)
        assert audio_file.file_path == str(sample_mp3_file)
        assert audio_file.file_extension == ".mp3"

    def test_audio_file_nonexistent_file(self):
        """Test AudioFile with non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            AudioFile("nonexistent_file.mp3")

    def test_audio_file_unsupported_type(self, temp_audio_file: Path):
        """Test AudioFile with unsupported file type."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            AudioFile(str(temp_audio_file))

    def test_file_operations(self, temp_audio_file: Path):
        """Test file read/write operations."""
        audio_file = AudioFile(temp_audio_file)
        
        # Test write
        test_data = b"test audio data"
        bytes_written = audio_file.write(test_data)
        assert bytes_written == len(test_data)
        
        # Test read
        read_data = audio_file.read()
        assert read_data == test_data

    def test_file_name_methods(self, sample_mp3_file: Path):
        """Test file name methods."""
        audio_file = AudioFile(sample_mp3_file)
        
        # Test system filename
        system_name = audio_file.get_file_name_system()
        assert system_name == sample_mp3_file.name
        
        # Test original filename (should be same as system for string paths)
        original_name = audio_file.get_file_name_original()
        assert original_name == sample_mp3_file.name

    def test_context_manager(self, sample_mp3_file: Path):
        """Test AudioFile as context manager."""
        with AudioFile(sample_mp3_file) as audio_file:
            assert audio_file.file_path == str(sample_mp3_file)
            # Context manager should work without issues
