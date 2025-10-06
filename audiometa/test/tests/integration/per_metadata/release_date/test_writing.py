"""Tests for writing release date metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestReleaseDateWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_release_date = "2024-01-01"
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: test_release_date}
        update_file_metadata(temp_audio_file, test_metadata)
        release_date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date == test_release_date

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_release_date = "2024-02-01"
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: test_release_date}
        update_file_metadata(temp_audio_file, test_metadata)
        release_date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date == test_release_date

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_release_date = "2024-03-01"
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: test_release_date}
        update_file_metadata(temp_audio_file, test_metadata)
        release_date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date == test_release_date
