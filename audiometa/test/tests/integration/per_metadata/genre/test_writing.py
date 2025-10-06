"""Tests for writing genre metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestGenreWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_genre = "Test Genre MP3"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_genre = "Test Genre WAV"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_genre = "Test Genre FLAC"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre
