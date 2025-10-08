"""Tests for writing album metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestAlbumWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_album = "Test Album ID3v2"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_album = "Test Album RIFF"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        metadata = get_merged_unified_metadata(temp_wav_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_album = "Test Album Vorbis"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        metadata = get_merged_unified_metadata(temp_flac_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album
