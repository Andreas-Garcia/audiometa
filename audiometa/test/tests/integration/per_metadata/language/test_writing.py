"""Tests for writing language metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLanguageWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_language = "en"
        test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
        update_file_metadata(temp_audio_file, test_metadata)
        language = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == test_language

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_language = "fr"
        test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
        update_file_metadata(temp_audio_file, test_metadata)
        language = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == test_language

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_language = "de"
        test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
        update_file_metadata(temp_audio_file, test_metadata)
        language = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == test_language
