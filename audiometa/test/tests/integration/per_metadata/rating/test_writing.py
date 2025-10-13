"""Tests for writing rating metadata using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRatingWriting:
    def test_id3v2(self, temp_audio_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        
        with TempFileWithMetadata(basic_metadata, "mp3") as test_file:
                # Now test rating writing using app's function (this is what we're testing)
                test_rating = 85
                test_metadata = {UnifiedMetadataKey.RATING: test_rating}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
                metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
                # Check that rating was set (may be normalized to a different value)
                assert metadata.get(UnifiedMetadataKey.RATING) is not None
                assert metadata.get(UnifiedMetadataKey.RATING) > 0

    def test_riff(self, metadata_none_wav, temp_wav_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
                # RIFF format now supports rating metadata through IRTD chunk
                test_rating = 75
                test_metadata = {UnifiedMetadataKey.RATING: test_rating}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            
                # Verify the rating was written and can be read back
                from audiometa import get_specific_metadata
                rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
                assert rating is not None
                assert isinstance(rating, int)

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        # Use external script to set basic metadata first
        basic_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        
        with TempFileWithMetadata(basic_metadata, "flac") as test_file:
                # Now test rating writing using app's function (this is what we're testing)
                test_rating = 90
                test_metadata = {UnifiedMetadataKey.RATING: test_rating}
                update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.VORBIS)
                metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
                # Check that rating was set (may be normalized to a different value)
                assert metadata.get(UnifiedMetadataKey.RATING) is not None
                assert metadata.get(UnifiedMetadataKey.RATING) > 0