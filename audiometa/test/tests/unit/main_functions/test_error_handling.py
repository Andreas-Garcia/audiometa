"""Tests for error handling in main functions."""

import pytest
from pathlib import Path

from audiometa import get_bitrate, get_duration_in_sec
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.unit
class TestErrorHandling:
    """Test cases for error handling in main functions."""

    def test_unsupported_file_type_raises_error(self, temp_audio_file: Path):
        """Test that unsupported file types raise FileTypeNotSupportedError."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_bitrate(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_duration_in_sec(str(temp_audio_file))
