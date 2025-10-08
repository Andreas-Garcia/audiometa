"""Tests for writing publisher metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestPublisherWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_publisher = "Test Publisher ID3v2"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_publisher = "Test Publisher RIFF"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        publisher = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_publisher = "Test Publisher Vorbis"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        publisher = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher
