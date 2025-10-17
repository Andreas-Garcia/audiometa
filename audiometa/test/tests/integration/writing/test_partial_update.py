"""Tests for general metadata writing functionality using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest

from audiometa import (
    update_file_metadata,
    get_merged_unified_metadata
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.test_helpers import TempFileWithMetadata


@pytest.mark.integration
class TestMetadataWriting:

    # Note: delete_all_metadata tests have been moved to test_delete_all_metadata.py

    def test_write_metadata_partial_update(self):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Get original metadata
            original_metadata = get_merged_unified_metadata(test_file.path)
            original_album = original_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
            
            # Update only title using app's function (this is what we're testing)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Partial Update Title"
            }
            
            update_file_metadata(test_file.path, test_metadata)
            updated_metadata = get_merged_unified_metadata(test_file.path)
            
            # Title should be updated
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Partial Update Title"
            # Other fields should remain unchanged
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == original_album