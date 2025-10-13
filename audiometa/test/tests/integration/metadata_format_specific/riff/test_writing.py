"""Tests for RIFF format writing functionality using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRiffWriting:

    def test_metadata_writing_wav(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
                        # Now test RIFF writing using app's function (this is what we're testing)
                        test_metadata = {
                            UnifiedMetadataKey.TITLE: "Test Title WAV",
                            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist WAV"],
                            UnifiedMetadataKey.ALBUM_NAME: "Test Album WAV",
                        }
                        update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
                        metadata = get_merged_unified_metadata(test_file.path)
                        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title WAV"
                        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist WAV"]
                        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album WAV"

    def test_multiple_metadata_reading(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
                        # Now test RIFF writing using app's function (this is what we're testing)
                        test_metadata = {
                            # Basic metadata commonly supported across formats
                            UnifiedMetadataKey.TITLE: "Test Song Title",
                            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                        }
            
                        update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
                        # Verify all fields
                        metadata = get_merged_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
                        # Basic metadata assertions
                        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
                        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
                        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_multiple_metadata_writing(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
                        # Now test RIFF writing using app's function (this is what we're testing)
                        test_metadata = {
                            # Basic metadata commonly supported across formats
                            UnifiedMetadataKey.TITLE: "Written Song Title",
                            UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
                            UnifiedMetadataKey.ALBUM_NAME: "Written Album",
                        }
            
                        update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
                        # Verify all fields were written
                        metadata = get_merged_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
                        # Basic metadata assertions
                        assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
                        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
                        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"

    def test_none_field_removal_riff(self, temp_audio_file):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
                        # First, set some metadata using app's function (this is what we're testing)
                        # Only supported fields for WAV
                        initial_metadata = {
                            UnifiedMetadataKey.TITLE: "Test WAV Title",
                            UnifiedMetadataKey.ARTISTS_NAMES: ["Test WAV Artist"],
                            UnifiedMetadataKey.ALBUM_NAME: "Test WAV Album"
                        }
                        update_file_metadata(test_file.path, initial_metadata)
            
                        # Verify metadata was written
                        metadata = get_merged_unified_metadata(test_file.path)
                        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test WAV Title"
                        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test WAV Artist"]
                        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test WAV Album"
            
                        # Now set some fields to None (RiffManager replaces entire INFO chunk, so we need to include fields we want to keep)
                        none_metadata = {
                            UnifiedMetadataKey.TITLE: None,
                            UnifiedMetadataKey.ARTISTS_NAMES: ["Test WAV Artist"],  # Keep this field
                            UnifiedMetadataKey.ALBUM_NAME: "Test WAV Album"  # Keep this field
                        }
                        update_file_metadata(test_file.path, none_metadata)
            
                        # Verify fields were removed (return None because they don't exist)
                        updated_metadata = get_merged_unified_metadata(test_file.path)
                        assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            
                        # Verify other fields are still present
                        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test WAV Artist"]
                        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test WAV Album"
            
                        # Verify at RIFF level that fields were actually removed
                        riff_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
                        assert riff_metadata.get(UnifiedMetadataKey.TITLE) is None

    def test_none_vs_empty_string_behavior_riff(self, temp_audio_file):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
                        # Set a field to empty string - should remove field (same as None)
                        update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
                        title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
                        assert title is None  # Empty string removes field in RIFF
            
                        # Set the same field to None - should remove field
                        update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None})
                        title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
                        assert title is None  # None removes field
            
                        # Set it back to empty string - should remove field again
                        update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
                        title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
                        assert title is None  # Empty string removes field in RIFF