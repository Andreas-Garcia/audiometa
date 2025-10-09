"""Tests for writing language metadata."""

import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestLanguageWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_language = "en"
        test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        language = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == test_language

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_language = "fr"
        test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        language = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.LANGUAGE)
        assert language == test_language

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_language = "de"
        test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        language = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.LANGUAGE)
        assert language == test_language
