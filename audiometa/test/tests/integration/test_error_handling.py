"""Tests for error handling across different APIs.

These tests verify that error handling is consistent across different
APIs and that appropriate exceptions are raised for various error conditions.
"""

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata,
    delete_metadata,
    get_bitrate,
    get_duration_in_sec
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestErrorHandling:
    """Test cases for error handling across APIs."""

    def test_error_handling_integration(self, temp_audio_file: Path):
        """Test error handling integration across different APIs."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        # All APIs should handle unsupported files consistently
        with pytest.raises(FileTypeNotSupportedError):
            get_merged_unified_metadata(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)
        
        with pytest.raises(FileTypeNotSupportedError):
            get_specific_metadata(str(temp_audio_file), UnifiedMetadataKey.TITLE)
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), {UnifiedMetadataKey.TITLE: "Test"})
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_metadata(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_bitrate(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_duration_in_sec(str(temp_audio_file))

    def test_nonexistent_file_error_handling(self):
        """Test error handling for non-existent files."""
        nonexistent_file = "nonexistent_file.mp3"
        
        with pytest.raises(FileNotFoundError):
            get_merged_unified_metadata(nonexistent_file)
        
        with pytest.raises(FileNotFoundError):
            get_single_format_app_metadata(nonexistent_file, MetadataFormat.ID3V2)
        
        with pytest.raises(FileNotFoundError):
            get_specific_metadata(nonexistent_file, UnifiedMetadataKey.TITLE)

    def test_invalid_metadata_key_error_handling(self, sample_mp3_file: Path):
        """Test error handling for invalid metadata keys."""
        # This should not raise an error, but return None
        invalid_key = "INVALID_KEY"
        result = get_specific_metadata(sample_mp3_file, invalid_key)
        assert result is None

    def test_invalid_format_error_handling(self, sample_mp3_file: Path):
        """Test error handling for invalid format requests."""
        # Try to get Vorbis metadata from MP3 file (should work but return empty)
        vorbis_metadata = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        
        # Try to get RIFF metadata from MP3 file (should work but return empty)
        riff_metadata = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
