"""Tests for complete additional metadata workflows using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

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
from audiometa.test.tests.test_script_helpers import create_test_file_with_metadata


@pytest.mark.integration
class TestAdditionalMetadata:

    def test_complete_additional_metadata_mp3(self, temp_audio_file: Path):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist",
            "album": "Test Album"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            basic_metadata,
            "mp3"
        )
        
        # Now test additional metadata using app's function (this is what we're testing)
        test_metadata = {
            UnifiedMetadataKey.COMPOSER: "Test Composer",
            UnifiedMetadataKey.PUBLISHER: "Test Publisher",
            UnifiedMetadataKey.COPYRIGHT: "© 2024 Test Label",
            UnifiedMetadataKey.LYRICS: "Test lyrics\nWith multiple lines",
            UnifiedMetadataKey.COMMENT: "Test comment",
            UnifiedMetadataKey.ENCODER: "LAME 3.100",
            UnifiedMetadataKey.URL: "https://example.com/track",
            UnifiedMetadataKey.ISRC: "USRC17607839",
            UnifiedMetadataKey.MOOD: "Happy",
            UnifiedMetadataKey.KEY: "C"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.COMPOSER) == "Test Composer"
        assert metadata.get(UnifiedMetadataKey.PUBLISHER) == "Test Publisher"
        assert metadata.get(UnifiedMetadataKey.COPYRIGHT) == "© 2024 Test Label"
        assert metadata.get(UnifiedMetadataKey.LYRICS) == "Test lyrics\nWith multiple lines"
        assert metadata.get(UnifiedMetadataKey.COMMENT) == "Test comment"
        assert metadata.get(UnifiedMetadataKey.ENCODER) == "LAME 3.100"
        assert metadata.get(UnifiedMetadataKey.URL) == "https://example.com/track"
        assert metadata.get(UnifiedMetadataKey.ISRC) == "USRC17607839"
        assert metadata.get(UnifiedMetadataKey.MOOD) == "Happy"
        assert metadata.get(UnifiedMetadataKey.KEY) == "C"

    def test_additional_metadata_with_audio_file_object(self, temp_audio_file: Path):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            basic_metadata,
            "mp3"
        )
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.COMPOSER: "AudioFile Composer",
            UnifiedMetadataKey.PUBLISHER: "AudioFile Publisher",
            UnifiedMetadataKey.COMMENT: "AudioFile Comment"
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(audio_file)
        assert metadata.get(UnifiedMetadataKey.COMPOSER) == "AudioFile Composer"
        assert metadata.get(UnifiedMetadataKey.PUBLISHER) == "AudioFile Publisher"
        assert metadata.get(UnifiedMetadataKey.COMMENT) == "AudioFile Comment"

    def test_empty_additional_metadata_handling(self, sample_mp3_file: Path):
        # Test reading from file with no additional metadata
        metadata = get_merged_unified_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific additional metadata that doesn't exist
        composer = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)
        
        publisher = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)
        
        lyrics = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)