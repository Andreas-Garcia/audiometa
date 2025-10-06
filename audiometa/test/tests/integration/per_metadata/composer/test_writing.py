"""Tests for writing composer metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestComposerWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_composer = "Test Composer MP3"
        test_metadata = {UnifiedMetadataKey.COMPOSER: test_composer}
        update_file_metadata(temp_audio_file, test_metadata)
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == test_composer

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_composer = "Test Composer WAV"
        test_metadata = {UnifiedMetadataKey.COMPOSER: test_composer}
        update_file_metadata(temp_audio_file, test_metadata)
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == test_composer

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_composer = "Test Composer FLAC"
        test_metadata = {UnifiedMetadataKey.COMPOSER: test_composer}
        update_file_metadata(temp_audio_file, test_metadata)
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == test_composer
