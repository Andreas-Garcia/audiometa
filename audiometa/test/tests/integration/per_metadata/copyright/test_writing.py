"""Tests for writing copyright metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestCopyrightWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_copyright = "© 2024 Test Label MP3"
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: test_copyright}
        update_file_metadata(temp_audio_file, test_metadata)
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == test_copyright

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_copyright = "© 2024 Test Label WAV"
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: test_copyright}
        update_file_metadata(temp_audio_file, test_metadata)
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == test_copyright

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_copyright = "© 2024 Test Label FLAC"
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: test_copyright}
        update_file_metadata(temp_audio_file, test_metadata)
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == test_copyright
