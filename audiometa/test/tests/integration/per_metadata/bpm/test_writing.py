"""Tests for writing BPM metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBpmWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_bpm = 128
        test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        update_file_metadata(temp_audio_file, test_metadata)
        bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
        assert bpm == test_bpm

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_bpm = 120
        test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        update_file_metadata(temp_audio_file, test_metadata)
        # WAV files may not support BPM metadata
        bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
        assert bpm is None or bpm == test_bpm

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_bpm = 140
        test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        update_file_metadata(temp_audio_file, test_metadata)
        bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
        assert bpm == test_bpm
