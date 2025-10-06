"""Tests for writing title metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_merged_unified_metadata, update_file_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestTitleWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_title = "Test Title MP3"
        test_metadata = {UnifiedMetadataKey.TITLE: test_title}
        update_file_metadata(temp_audio_file, test_metadata)
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == test_title

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_title = "Test Title WAV"
        test_metadata = {UnifiedMetadataKey.TITLE: test_title}
        update_file_metadata(temp_audio_file, test_metadata)
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == test_title

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_title = "Test Title FLAC"
        test_metadata = {UnifiedMetadataKey.TITLE: test_title}
        update_file_metadata(temp_audio_file, test_metadata)
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == test_title
