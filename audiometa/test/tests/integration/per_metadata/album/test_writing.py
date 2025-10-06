"""Tests for writing album metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestAlbumWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_album = "Test Album MP3"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_album = "Test Album WAV"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_album = "Test Album FLAC"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album
