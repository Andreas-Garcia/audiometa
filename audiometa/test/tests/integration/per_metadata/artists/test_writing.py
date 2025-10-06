"""Tests for writing artists metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestArtistsWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_artists = ["Test Artist 1", "Test Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_artists = ["WAV Artist 1", "WAV Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_artists = ["FLAC Artist 1", "FLAC Artist 2"]
        test_metadata = {UnifiedMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists
