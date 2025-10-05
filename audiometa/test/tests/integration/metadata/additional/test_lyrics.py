"""Tests for lyrics metadata."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_app_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLyricsMetadata:
    """Test cases for lyrics metadata."""

    def test_lyrics_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test lyrics metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_lyrics = "These are test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_lyrics_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test lyrics metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_lyrics = "FLAC test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_lyrics_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test lyrics metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_lyrics = "WAV test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_lyrics_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test lyrics metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_lyrics = "AudioFile test lyrics\nWith multiple lines\nFor testing purposes"
        test_metadata = {UnifiedMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(audio_file, test_metadata)
        
        lyrics = get_specific_metadata(audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_lyrics_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test lyrics metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test short lyrics
        short_lyrics = "Short"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LYRICS: short_lyrics})
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == short_lyrics
        
        # Test long lyrics
        long_lyrics = "A" * 10000
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LYRICS: long_lyrics})
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == long_lyrics
        
        # Test empty lyrics
        empty_lyrics = ""
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LYRICS: empty_lyrics})
        lyrics = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LYRICS)
        assert lyrics == empty_lyrics

