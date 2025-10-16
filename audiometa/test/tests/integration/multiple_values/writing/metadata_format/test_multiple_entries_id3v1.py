import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesId3v1:
    def test_write_single_artist_id3v1_limitation(self, sample_mp3_file: Path, temp_audio_file: Path):
        # ID3v1 has limited support for multiple values
        # It typically only supports single values for most fields
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Single Artist"]  # Only one artist for ID3v1
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Read back using unified function
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # ID3v1 should return a single value, not a list
        assert artists == "Single Artist"

    def test_write_single_artist_id3v1_specific(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Write single artist to ID3v1 format specifically
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Primary Artist"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Read back using ID3v1 specific function
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # ID3v1 should return a single value
        assert artists == "Primary Artist"

    def test_write_single_album_artist(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Write single album artist
        metadata = {
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        # ID3v1 should return a single value
        assert album_artists == "Album Artist"

    def test_write_single_composer(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Write single composer
        metadata = {
            UnifiedMetadataKey.COMPOSER: ["Composer Name"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        composer = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        
        # ID3v1 should return a single value
        assert composer == "Composer Name"

    def test_write_basic_metadata_fields(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Write basic metadata fields that ID3v1 supports
        metadata = {
            UnifiedMetadataKey.TITLE: "Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist Name"],
            UnifiedMetadataKey.ALBUM_NAME: "Album Name",
            UnifiedMetadataKey.GENRE_NAME: "Rock",
            UnifiedMetadataKey.COMMENT: "Comment text"
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Check that all fields were written as single values
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Song Title"
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == "Artist Name"
        assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Album Name"
        assert unified_metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Rock"
        assert unified_metadata.get(UnifiedMetadataKey.COMMENT) == "Comment text"

    def test_write_none_removes_field(self, sample_mp3_file: Path, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist Name"]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: None
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_write_empty_string_removes_field(self, sample_mp3_file: Path, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist Name"]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write empty string (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [""]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_id3v1_field_length_limitations(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Test ID3v1 field length limitations
        long_title = "A" * 31  # ID3v1 title field is 30 characters max
        long_artist = "B" * 31  # ID3v1 artist field is 30 characters max
        long_album = "C" * 31  # ID3v1 album field is 30 characters max
        
        metadata = {
            UnifiedMetadataKey.TITLE: long_title,
            UnifiedMetadataKey.ARTISTS_NAMES: [long_artist],
            UnifiedMetadataKey.ALBUM_NAME: long_album
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Check that fields were truncated to ID3v1 limits
        title = unified_metadata.get(UnifiedMetadataKey.TITLE)
        artist = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        album = unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
        
        # Should be truncated to 30 characters
        assert len(title) <= 30
        assert len(artist) <= 30
        assert len(album) <= 30
