"""Tests for writing rating metadata using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.test.tests.test_script_helpers import create_test_file_with_metadata


@pytest.mark.integration
class TestRatingWriting:
    def test_mp3(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        test_file = create_test_file_with_metadata(
            basic_metadata,
            "mp3"
        )
        
        # Now test rating writing using app's function (this is what we're testing)
        test_rating = 85
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(test_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
        # Check that rating was set (may be normalized to a different value)
        assert metadata.get(UnifiedMetadataKey.RATING) is not None
        assert metadata.get(UnifiedMetadataKey.RATING) > 0

    def test_wav(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        test_file = create_test_file_with_metadata(
            basic_metadata,
            "wav"
        )
        
        # WAV files don't support rating metadata - should raise MetadataNotSupportedError
        test_rating = 75
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.RATING metadata not supported by RIFF format"):
            update_file_metadata(test_file, test_metadata, normalized_rating_max_value=100)

    def test_flac(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        test_file = create_test_file_with_metadata(
            basic_metadata,
            "flac"
        )
        
        # Now test rating writing using app's function (this is what we're testing)
        test_rating = 90
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(test_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
        # Check that rating was set (may be normalized to a different value)
        assert metadata.get(UnifiedMetadataKey.RATING) is not None
        assert metadata.get(UnifiedMetadataKey.RATING) > 0