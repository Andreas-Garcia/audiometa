"""Tests for cross-API error handling consistency.

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
class TestCrossApiConsistency:

    def test_error_handling_consistency_across_apis(self, temp_audio_file: Path):
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
