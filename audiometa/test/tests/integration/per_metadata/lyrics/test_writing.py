"""Tests for writing lyrics metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLyricsWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_lyrics = "These are test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_lyrics = "WAV test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_lyrics = "FLAC test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics
