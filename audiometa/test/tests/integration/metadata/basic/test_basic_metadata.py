"""Tests for complete basic metadata workflows."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_app_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.utils.MetadataSingleFormat import MetadataSingleFormat


@pytest.mark.integration
class TestBasicMetadata:
    """Test cases for complete basic metadata workflows."""

    def test_complete_basic_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all basic metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "Complete Test Song",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist 1", "Test Artist 2"],
            AppMetadataKey.ALBUM_NAME: "Complete Test Album",
            AppMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist"],
            AppMetadataKey.GENRE_NAME: "Rock",
            AppMetadataKey.RATING: 90
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == "Complete Test Song"
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist 1", "Test Artist 2"]
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "Complete Test Album"
        assert metadata.get(AppMetadataKey.ALBUM_ARTISTS_NAMES) == ["Album Artist"]
        assert metadata.get(AppMetadataKey.GENRE_NAME) == "Rock"
        assert metadata.get(AppMetadataKey.RATING) == 90

    def test_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test basic metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "AudioFile Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["AudioFile Test Artist"]
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == "AudioFile Test Title"
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["AudioFile Test Artist"]

    def test_metadata_reading_with_different_formats(self, sample_mp3_file: Path):
        """Test reading metadata from different format managers."""
        # Test ID3v2 format specifically
        from audiometa import get_single_format_app_metadata
        
        metadata_id3v2 = get_single_format_app_metadata(sample_mp3_file, MetadataSingleFormat.ID3V2)
        assert isinstance(metadata_id3v2, dict)
        
        # Test ID3v1 format specifically
        metadata_id3v1 = get_single_format_app_metadata(sample_mp3_file, MetadataSingleFormat.ID3V1)
        assert isinstance(metadata_id3v1, dict)

    def test_empty_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing metadata."""
        # Test reading from file with no metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific metadata that doesn't exist
        title = get_specific_metadata(sample_mp3_file, AppMetadataKey.TITLE)
        assert title is None or isinstance(title, str)
        
        artists = get_specific_metadata(sample_mp3_file, AppMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)