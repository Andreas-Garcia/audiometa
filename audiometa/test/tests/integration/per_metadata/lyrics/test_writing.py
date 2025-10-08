"""Tests for writing lyrics metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestLyricsWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_lyrics = "These are test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_lyrics = "RIFF test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_lyrics = "Vorbis test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics
