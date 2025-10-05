"""Tests for complete basic metadata workflows."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.comprehensive
class TestBasicMetadata:
    """Test cases for complete basic metadata workflows."""

    def test_complete_basic_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all basic metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Complete Test Song",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist 1", "Test Artist 2"],
            UnifiedMetadataKey.ALBUM_NAME: "Complete Test Album",
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist"],
            UnifiedMetadataKey.GENRE_NAME: "Rock",
            UnifiedMetadataKey.RATING: 90
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Complete Test Song"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist 1", "Test Artist 2"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Complete Test Album"
        assert metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES) == ["Album Artist"]
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Rock"
        assert metadata.get(UnifiedMetadataKey.RATING) == 90

    def test_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test basic metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "AudioFile Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["AudioFile Test Artist"]
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "AudioFile Test Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["AudioFile Test Artist"]

    def test_metadata_reading_with_different_formats(self, sample_mp3_file: Path):
        """Test reading metadata from different format managers."""
        # Test ID3v2 format specifically
        from audiometa import get_single_format_app_metadata
        
        metadata_id3v2 = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V2)
        assert isinstance(metadata_id3v2, dict)
        
        # Test ID3v1 format specifically
        metadata_id3v1 = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V1)
        assert isinstance(metadata_id3v1, dict)

    def test_empty_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing metadata."""
        # Test reading from file with no metadata
        metadata = get_merged_unified_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific metadata that doesn't exist
        title = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)
        
        artists = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)