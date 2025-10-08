"""Tests for writing rating metadata using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.test_script_helpers import create_test_file_with_specific_metadata


@pytest.mark.integration
class TestRatingWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_specific_metadata(
            metadata_none_mp3,
            temp_audio_file,
            basic_metadata,
            "mp3"
        )
        
        # Now test rating writing using app's function (this is what we're testing)
        test_rating = 85
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RATING) == test_rating

    def test_wav(self, metadata_none_wav, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_specific_metadata(
            metadata_none_wav,
            temp_audio_file,
            basic_metadata,
            "wav"
        )
        
        # Now test rating writing using app's function (this is what we're testing)
        test_rating = 75
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RATING) == test_rating

    def test_flac(self, metadata_none_flac, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_specific_metadata(
            metadata_none_flac,
            temp_audio_file,
            basic_metadata,
            "flac"
        )
        
        # Now test rating writing using app's function (this is what we're testing)
        test_rating = 90
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RATING) == test_rating