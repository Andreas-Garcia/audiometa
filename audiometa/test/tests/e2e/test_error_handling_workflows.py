"""
End-to-end tests for error handling and recovery workflows.

These tests verify that the system handles errors gracefully and recovers
properly from various error conditions in real-world scenarios.
"""
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    delete_all_metadata,
    get_bitrate,
    get_duration_in_sec
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.e2e
class TestErrorHandlingWorkflows:

    def test_error_recovery_workflow(self):
        # E2E test for error scenarios
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Test invalid operations - try to update with rating without normalized_rating_max_value
            with pytest.raises(Exception):  # ConfigurationError
                update_file_metadata(test_file.path, {UnifiedMetadataKey.RATING: 75})  # Missing normalized_rating_max_value
        
            # Test recovery after errors
            test_metadata = {UnifiedMetadataKey.TITLE: "Recovery Test"}
            update_file_metadata(test_file.path, test_metadata)
        
            # Verify the file is still usable
            metadata = get_merged_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Recovery Test"

    def test_error_handling_workflow(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        test_file = temp_audio_file.with_suffix(".txt")
        test_file.write_bytes(b"fake audio content")
        
        # All operations should raise FileTypeNotSupportedError
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_merged_unified_metadata(str(test_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            update_file_metadata(str(test_file), {UnifiedMetadataKey.TITLE: "Test"})
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            delete_all_metadata(str(test_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_bitrate(str(test_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_duration_in_sec(str(test_file))
