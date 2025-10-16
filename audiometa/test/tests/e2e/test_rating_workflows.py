"""
End-to-end tests for rating normalization workflows.

These tests verify that the system correctly handles different rating scales
and normalization values across different audio formats.
"""
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.e2e
class TestRatingWorkflows:

    def test_metadata_with_different_rating_normalizations(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Initial Rating Test",
            "artist": "Initial Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Test with 0-100 rating scale
            test_metadata_100 = {
                UnifiedMetadataKey.TITLE: "Rating Test 100",
                UnifiedMetadataKey.RATING: 60
            }
            update_file_metadata(test_file.path, test_metadata_100, normalized_rating_max_value=100, metadata_format=MetadataFormat.ID3V2)
    
            metadata_100 = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            assert metadata_100.get(UnifiedMetadataKey.TITLE) == "Rating Test 100"
            assert metadata_100.get(UnifiedMetadataKey.RATING) == 60
    
            # Test with 0-255 rating scale
            test_metadata_255 = {
                UnifiedMetadataKey.TITLE: "Rating Test 255",
                UnifiedMetadataKey.RATING: 153  # 60% of 255
            }
            update_file_metadata(test_file.path, test_metadata_255, normalized_rating_max_value=255, metadata_format=MetadataFormat.ID3V2)
    
            metadata_255 = get_merged_unified_metadata(test_file, normalized_rating_max_value=255)
            assert metadata_255.get(UnifiedMetadataKey.TITLE) == "Rating Test 255"
            assert metadata_255.get(UnifiedMetadataKey.RATING) == 153
