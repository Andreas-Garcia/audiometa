"""Tests for format-specific error handling scenarios."""

import pytest

from audiometa import (
    get_merged_app_metadata,
    get_single_format_app_metadata,
    get_specific_metadata
)
from audiometa.utils.MetadataSingleFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestFormatSpecificErrorHandling:
    """Test cases for format-specific error handling."""

    def test_unsupported_format_error(self, temp_audio_file):
        """Test that unsupported formats raise appropriate errors."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_merged_app_metadata(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)
        
        with pytest.raises(FileTypeNotSupportedError):
            get_specific_metadata(str(temp_audio_file), UnifiedMetadataKey.TITLE)
