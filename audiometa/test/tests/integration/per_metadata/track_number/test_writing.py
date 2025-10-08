"""Tests for writing track number metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestTrackNumberWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_track_number = 1
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        track_number = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number == test_track_number

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_track_number = 2
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        track_number = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number == test_track_number

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_track_number = 3
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: test_track_number}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        track_number = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number == test_track_number
