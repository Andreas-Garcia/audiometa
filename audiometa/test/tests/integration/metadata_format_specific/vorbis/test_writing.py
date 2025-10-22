

import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    get_specific_metadata,
    update_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestVorbisWriting:

    def test_metadata_writing_flac(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title FLAC",
                UnifiedMetadataKey.ARTISTS: ["Test Artist FLAC"],
                UnifiedMetadataKey.ALBUM: "Test Album FLAC",
                UnifiedMetadataKey.GENRES_NAMES: ["Test Genre FLAC"],
                UnifiedMetadataKey.RATING: 10
            }
            update_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            metadata = get_unified_metadata(test_file.path, normalized_rating_max_value=10)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title FLAC"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist FLAC"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album FLAC"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Test Genre FLAC"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 1

    def test_multiple_metadata_reading(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_metadata = {
                # Basic metadata commonly supported across formats
                UnifiedMetadataKey.TITLE: "Test Song Title",
                UnifiedMetadataKey.ARTISTS: ["Test Artist"],
                UnifiedMetadataKey.ALBUM: "Test Album",
                UnifiedMetadataKey.GENRES_NAMES: ["Test Genre"],
                UnifiedMetadataKey.RATING: 8
            }
            
            update_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
            # Verify all fields
            metadata = get_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
            # Basic metadata assertions
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Test Genre"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_multiple_metadata_writing(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_metadata = {
                # Basic metadata commonly supported across formats
                UnifiedMetadataKey.TITLE: "Written Song Title",
                UnifiedMetadataKey.ARTISTS: ["Written Artist"],
                UnifiedMetadataKey.ALBUM: "Written Album",
                UnifiedMetadataKey.GENRES_NAMES: ["Written Genre"],
                UnifiedMetadataKey.RATING: 9
            }
            
            update_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
            # Verify all fields were written
            metadata = get_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
            # Basic metadata assertions
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Written Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Written Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Written Genre"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_none_field_removal_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # First, set some metadata (without rating to avoid configuration issues)
            initial_metadata = {
                UnifiedMetadataKey.TITLE: "Test FLAC Title",
                UnifiedMetadataKey.ARTISTS: ["Test FLAC Artist"],
                UnifiedMetadataKey.ALBUM: "Test FLAC Album",
                UnifiedMetadataKey.BPM: 140
            }
            update_metadata(test_file.path, initial_metadata)
            
            # Verify metadata was written
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test FLAC Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test FLAC Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test FLAC Album"
            assert metadata.get(UnifiedMetadataKey.BPM) == 140
            
            # Now set some fields to None
            none_metadata = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.BPM: None
            }
            update_metadata(test_file.path, none_metadata)
            
            # Verify fields were removed (return None because they don't exist)
            updated_metadata = get_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert updated_metadata.get(UnifiedMetadataKey.BPM) is None
            
            # Verify other fields are still present
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test FLAC Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM) == "Test FLAC Album"
            
            # Verify at Vorbis level that fields were actually deleted
            vorbis_metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert vorbis_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert vorbis_metadata.get(UnifiedMetadataKey.BPM) is None

    def test_none_vs_empty_string_behavior_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set a field to empty string - should create empty field
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == ""  # Empty string creates empty field
            
            # Set the same field to None - should remove field
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None})
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # None removes field
            
            # Set it back to empty string - should create empty field again
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == ""  # Empty string creates empty field
