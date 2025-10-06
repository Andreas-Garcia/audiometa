"""Tests for writing rating metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestRatingWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_rating = 85
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RATING) == test_rating

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_rating = 75
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RATING) == test_rating

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_rating = 90
        test_metadata = {UnifiedMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RATING) == test_rating
