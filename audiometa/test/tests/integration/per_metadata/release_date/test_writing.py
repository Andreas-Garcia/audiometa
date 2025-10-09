"""Tests for writing release date metadata."""

import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestReleaseDateWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_release_date = "2024-01-01"
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: test_release_date}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        release_date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date == test_release_date

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_release_date = "2024-02-01"
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: test_release_date}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        release_date = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date == test_release_date

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_release_date = "2024-03-01"
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: test_release_date}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        release_date = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date == test_release_date
