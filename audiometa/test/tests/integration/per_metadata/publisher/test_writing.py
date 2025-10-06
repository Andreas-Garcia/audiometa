"""Tests for writing publisher metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestPublisherWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_publisher = "Test Publisher MP3"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        update_file_metadata(temp_audio_file, test_metadata)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_publisher = "Test Publisher WAV"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        update_file_metadata(temp_audio_file, test_metadata)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_publisher = "Test Publisher FLAC"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        update_file_metadata(temp_audio_file, test_metadata)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher
