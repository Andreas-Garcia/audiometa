

import pytest
from pathlib import Path
import shutil

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestVorbisWriting:

    def test_metadata_writing_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title FLAC",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist FLAC"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album FLAC",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre FLAC",
            UnifiedMetadataKey.RATING: 10
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title FLAC"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist FLAC"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album FLAC"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre FLAC"
        assert metadata.get(UnifiedMetadataKey.RATING) == 1

    def test_multiple_metadata_reading(self, sample_flac_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata commonly supported across formats
            UnifiedMetadataKey.TITLE: "Test Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre",
            UnifiedMetadataKey.RATING: 8
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre"
        assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_multiple_metadata_writing(self, sample_flac_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata commonly supported across formats
            UnifiedMetadataKey.TITLE: "Written Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Written Album",
            UnifiedMetadataKey.GENRE_NAME: "Written Genre",
            UnifiedMetadataKey.RATING: 9
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields were written
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Written Genre"
        assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_none_field_removal_vorbis(self, sample_flac_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location with correct extension
        temp_flac_file = temp_audio_file.with_suffix('.flac')
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # First, set some metadata (without rating to avoid configuration issues)
        initial_metadata = {
            UnifiedMetadataKey.TITLE: "Test FLAC Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test FLAC Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test FLAC Album",
            UnifiedMetadataKey.BPM: 140
        }
        update_file_metadata(temp_flac_file, initial_metadata)
        
        # Verify metadata was written
        metadata = get_merged_unified_metadata(temp_flac_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test FLAC Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test FLAC Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test FLAC Album"
        assert metadata.get(UnifiedMetadataKey.BPM) == 140
        
        # Now set some fields to None
        none_metadata = {
            UnifiedMetadataKey.TITLE: None,
            UnifiedMetadataKey.BPM: None
        }
        update_file_metadata(temp_flac_file, none_metadata)
        
        # Verify fields were removed (return None because they don't exist)
        updated_metadata = get_merged_unified_metadata(temp_flac_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
        assert updated_metadata.get(UnifiedMetadataKey.BPM) is None
        
        # Verify other fields are still present
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test FLAC Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test FLAC Album"
        
        # Verify at Vorbis level that fields were actually deleted
        vorbis_metadata = get_single_format_app_metadata(temp_flac_file, MetadataFormat.VORBIS)
        assert vorbis_metadata.get(UnifiedMetadataKey.TITLE) is None
        assert vorbis_metadata.get(UnifiedMetadataKey.BPM) is None

    def test_none_vs_empty_string_behavior_vorbis(self, sample_flac_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location with correct extension
        temp_flac_file = temp_audio_file.with_suffix('.flac')
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Set a field to empty string - should create empty field
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.TITLE: ""})
        title = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.TITLE)
        assert title == ""  # Empty string creates empty field
        
        # Set the same field to None - should remove field
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.TITLE: None})
        title = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.TITLE)
        assert title is None  # None removes field
        
        # Set it back to empty string - should create empty field again
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.TITLE: ""})
        title = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.TITLE)
        assert title == ""  # Empty string creates empty field
