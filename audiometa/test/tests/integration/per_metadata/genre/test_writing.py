"""Tests for writing genre metadata."""

import pytest
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestGenreWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_genre = "Test Genre ID3v2"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_genre = "Rock"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        metadata = get_merged_unified_metadata(temp_wav_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_genre = "Test Genre Vorbis"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        metadata = get_merged_unified_metadata(temp_flac_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre
