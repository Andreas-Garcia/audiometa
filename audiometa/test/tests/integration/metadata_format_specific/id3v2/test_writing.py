

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v2Writing:

    def test_metadata_writing_mp3(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title MP3",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist MP3"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album MP3",
                UnifiedMetadataKey.GENRES_NAMES: ["Test Genre MP3"],
                UnifiedMetadataKey.RATING: 10
            }
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            metadata = get_merged_unified_metadata(test_file.path, normalized_rating_max_value=10)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title MP3"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist MP3"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album MP3"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Test Genre MP3"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 1

    def test_multiple_metadata_reading(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_metadata = {
                # Basic metadata commonly supported across formats
                UnifiedMetadataKey.TITLE: "Test Song Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.GENRES_NAMES: ["Test Genre"],
                UnifiedMetadataKey.RATING: 8
            }
            
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
            # Verify all fields
            metadata = get_merged_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
            # Basic metadata assertions
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Test Genre"]
            assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_multiple_metadata_writing(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_metadata = {
                # Basic metadata commonly supported across formats
                UnifiedMetadataKey.TITLE: "Written Song Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Written Album",
                UnifiedMetadataKey.GENRES_NAMES: ["Written Genre"],
                UnifiedMetadataKey.RATING: 9
            }
            
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100)
            
            # Verify all fields were written
            metadata = get_merged_unified_metadata(test_file.path, normalized_rating_max_value=10)
            
            # Basic metadata assertions
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Written Genre"]   
            assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_none_field_removal_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # First, set some metadata (without rating to avoid configuration issues)
            initial_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.BPM: 120
            }
            update_file_metadata(test_file.path, initial_metadata)
            
            # Verify metadata was written
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.BPM) == 120
            
            # Now set some fields to None
            none_metadata = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.BPM: None
            }
            update_file_metadata(test_file.path, none_metadata)
            
            # Verify fields were removed (return None because they don't exist)
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert updated_metadata.get(UnifiedMetadataKey.BPM) is None
            
            # Verify other fields are still present
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Verify at ID3v2 level that frames were actually deleted
            id3v2_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_metadata.get(UnifiedMetadataKey.BPM) is None

    def test_none_vs_empty_string_behavior_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set a field to empty string - mutagen removes empty frames, so field is removed
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field (mutagen removes empty frames)
            
            # Set the same field to None - should remove field
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None})
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # None removes field
            
            # Set it back to empty string - should remove field again
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field (mutagen removes empty frames)

    def test_mp3_writes_id3v2_3_format_by_default(self):
        from mutagen.id3 import ID3
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Prepare test metadata (without rating to avoid configuration issues)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2.3 Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.3 Test Album",
                UnifiedMetadataKey.BPM: 120
            }
            
            # Update metadata using the library (should default to ID3v2.3)
            update_file_metadata(test_file.path, test_metadata)
            
            # Verify that the file now contains ID3v2.3 tags
            id3_tags = ID3(test_file.path)
            assert id3_tags.version == (2, 3, 0), f"Expected ID3v2.3, but got version {id3_tags.version}"
            
            # Verify metadata was written correctly
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Test Title"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Test Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2.3 Test Album"
            assert updated_metadata.get(UnifiedMetadataKey.BPM) == 120

    def test_mp3_writes_id3v2_4_format_when_specified(self):
        from mutagen.id3 import ID3
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Prepare test metadata (without rating to avoid configuration issues)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.4 Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2.4 Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.4 Test Album",
                UnifiedMetadataKey.BPM: 120
            }
            
            # Update metadata using the library with explicit ID3v2.4 version
            update_file_metadata(test_file.path, test_metadata, id3v2_version=(2, 4, 0))
            
            # Verify that the file now contains ID3v2.4 tags
            id3_tags = ID3(test_file.path)
            assert id3_tags.version == (2, 4, 0), f"Expected ID3v2.4, but got version {id3_tags.version}"
            
            # Verify metadata was written correctly
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.4 Test Title"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.4 Test Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2.4 Test Album"
            assert updated_metadata.get(UnifiedMetadataKey.BPM) == 120

    def test_mp3_writes_id3v2_3_format_when_explicitly_specified(self):
        from mutagen.id3 import ID3
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Prepare test metadata (without rating to avoid configuration issues)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Explicit Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2.3 Explicit Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.3 Explicit Test Album",
                UnifiedMetadataKey.BPM: 120
            }
            
            # Update metadata using the library with explicit ID3v2.3 version
            update_file_metadata(test_file.path, test_metadata, id3v2_version=(2, 3, 0))
            
            # Verify that the file now contains ID3v2.3 tags
            id3_tags = ID3(test_file.path)
            assert id3_tags.version == (2, 3, 0), f"Expected ID3v2.3, but got version {id3_tags.version}"
            
            # Verify metadata was written correctly
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Explicit Test Title"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Explicit Test Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2.3 Explicit Test Album"
            assert updated_metadata.get(UnifiedMetadataKey.BPM) == 120

    def test_mp3_upgrades_existing_id3v2_4_to_id3v2_3_when_specified(self):
        from mutagen.id3 import ID3
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # First, create ID3v2.4 tags
            test_metadata_v4 = {
                UnifiedMetadataKey.TITLE: "Original ID3v2.4 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original ID3v2.4 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Original ID3v2.4 Album"
            }
            update_file_metadata(test_file.path, test_metadata_v4, id3v2_version=(2, 4, 0))
            
            # Verify it's ID3v2.4
            id3_tags = ID3(test_file.path)
            assert id3_tags.version == (2, 4, 0), f"Expected ID3v2.4, but got version {id3_tags.version}"
            
            # Now update with ID3v2.3 version - should upgrade existing tags
            test_metadata_v3 = {
                UnifiedMetadataKey.TITLE: "Updated ID3v2.3 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Updated ID3v2.3 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Updated ID3v2.3 Album"
            }
            update_file_metadata(test_file.path, test_metadata_v3, id3v2_version=(2, 3, 0))
            
            # Verify it's now ID3v2.3
            id3_tags = ID3(test_file.path)
            assert id3_tags.version == (2, 3, 0), f"Expected ID3v2.3, but got version {id3_tags.version}"
            
            # Verify metadata was updated correctly
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Updated ID3v2.3 Title"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Updated ID3v2.3 Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Updated ID3v2.3 Album"
