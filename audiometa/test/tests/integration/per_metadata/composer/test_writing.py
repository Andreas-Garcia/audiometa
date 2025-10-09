"""Tests for writing composer metadata."""

import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestComposerWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_composer = "Test Composer ID3v2"
        test_metadata = {UnifiedMetadataKey.COMPOSER: test_composer}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == test_composer

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_composer = "Test Composer RIFF"
        test_metadata = {UnifiedMetadataKey.COMPOSER: test_composer}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        composer = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.COMPOSER)
        assert composer == test_composer

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_composer = "Test Composer Vorbis"
        test_metadata = {UnifiedMetadataKey.COMPOSER: test_composer}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        composer = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.COMPOSER)
        assert composer == test_composer
