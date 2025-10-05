"""Tests for complete additional metadata workflows."""

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


@pytest.mark.comprehensive
class TestAdditionalMetadata:
    """Test cases for complete additional metadata workflows."""

    def test_complete_additional_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all additional metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.COMPOSER: "Test Composer",
            AppMetadataKey.PUBLISHER: "Test Publisher",
            AppMetadataKey.COPYRIGHT: "© 2024 Test Label",
            AppMetadataKey.LYRICS: "Test lyrics\nWith multiple lines",
            AppMetadataKey.COMMENT: "Test comment",
            AppMetadataKey.ENCODER: "LAME 3.100",
            AppMetadataKey.URL: "https://example.com/track",
            AppMetadataKey.ISRC: "USRC17607839",
            AppMetadataKey.MOOD: "Happy",
            AppMetadataKey.KEY: "C"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.COMPOSER) == "Test Composer"
        assert metadata.get(AppMetadataKey.PUBLISHER) == "Test Publisher"
        assert metadata.get(AppMetadataKey.COPYRIGHT) == "© 2024 Test Label"
        assert metadata.get(AppMetadataKey.LYRICS) == "Test lyrics\nWith multiple lines"
        assert metadata.get(AppMetadataKey.COMMENT) == "Test comment"
        assert metadata.get(AppMetadataKey.ENCODER) == "LAME 3.100"
        assert metadata.get(AppMetadataKey.URL) == "https://example.com/track"
        assert metadata.get(AppMetadataKey.ISRC) == "USRC17607839"
        assert metadata.get(AppMetadataKey.MOOD) == "Happy"
        assert metadata.get(AppMetadataKey.KEY) == "C"

    def test_additional_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test additional metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.COMPOSER: "AudioFile Composer",
            AppMetadataKey.PUBLISHER: "AudioFile Publisher",
            AppMetadataKey.COMMENT: "AudioFile Comment"
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.COMPOSER) == "AudioFile Composer"
        assert metadata.get(AppMetadataKey.PUBLISHER) == "AudioFile Publisher"
        assert metadata.get(AppMetadataKey.COMMENT) == "AudioFile Comment"

    def test_empty_additional_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing additional metadata."""
        # Test reading from file with no additional metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific additional metadata that doesn't exist
        composer = get_specific_metadata(sample_mp3_file, AppMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)
        
        publisher = get_specific_metadata(sample_mp3_file, AppMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)
        
        lyrics = get_specific_metadata(sample_mp3_file, AppMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)