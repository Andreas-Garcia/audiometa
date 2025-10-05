"""Integration tests for AudioFile class with metadata APIs."""

import pytest
from pathlib import Path

from audiometa import (
    AudioFile,
    get_merged_app_metadata,
    get_single_format_app_metadata,
    get_specific_metadata
)
from audiometa.utils.MetadataSingleFormat import MetadataSingleFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.integration
class TestAudioFileIntegration:
    """Integration test cases for AudioFile class with metadata APIs."""

    def test_get_duration_in_sec_mp3(self, sample_mp3_file: Path):
        """Test getting duration for MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        duration = audio_file.get_duration_in_sec()
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_flac(self, sample_flac_file: Path):
        """Test getting duration for FLAC file."""
        audio_file = AudioFile(sample_flac_file)
        duration = audio_file.get_duration_in_sec()
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_wav(self, sample_wav_file: Path):
        """Test getting duration for WAV file."""
        audio_file = AudioFile(sample_wav_file)
        duration = audio_file.get_duration_in_sec()
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_bitrate_mp3(self, sample_mp3_file: Path):
        """Test getting bitrate for MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        bitrate = audio_file.get_bitrate()
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_flac(self, sample_flac_file: Path):
        """Test getting bitrate for FLAC file."""
        audio_file = AudioFile(sample_flac_file)
        bitrate = audio_file.get_bitrate()
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_wav(self, sample_wav_file: Path):
        """Test getting bitrate for WAV file."""
        audio_file = AudioFile(sample_wav_file)
        bitrate = audio_file.get_bitrate()
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_audio_file_object_integration(self, sample_mp3_file: Path):
        """Test integration between AudioFile object and functional APIs."""
        audio_file = AudioFile(sample_mp3_file)
        
        # Test that AudioFile object works with functional APIs
        metadata = get_merged_app_metadata(audio_file)
        assert isinstance(metadata, dict)
        
        # Test single format with AudioFile object
        id3v2_metadata = get_single_format_app_metadata(audio_file, MetadataSingleFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        
        # Test specific metadata with AudioFile object
        title = get_specific_metadata(audio_file, AppMetadataKey.TITLE)
        assert title is None or isinstance(title, str)



