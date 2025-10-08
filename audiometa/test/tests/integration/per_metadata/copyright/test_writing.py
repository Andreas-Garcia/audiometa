"""Tests for writing copyright metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestCopyrightWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_copyright = "© 2024 Test Label ID3v2"
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: test_copyright}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == test_copyright

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_copyright = "© 2024 Test Label RIFF"
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: test_copyright}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == test_copyright

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_copyright = "© 2024 Test Label Vorbis"
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: test_copyright}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == test_copyright
