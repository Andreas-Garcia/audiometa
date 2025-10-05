"""Tests for artists metadata."""

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
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.integration
class TestArtistsMetadata:
    """Test cases for artists metadata."""

    def test_artists_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test artists metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_artists = ["Test Artist 1", "Test Artist 2"]
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_artists_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test artists metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_artists = ["FLAC Artist 1", "FLAC Artist 2"]
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_artists_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test artists metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_artists = ["WAV Artist 1", "WAV Artist 2"]
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_artists_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test artists metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_artists = ["AudioFile Artist 1", "AudioFile Artist 2"]
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_single_artist(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test single artist metadata."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_artists = ["Single Artist"]
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_multiple_artists(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test multiple artists metadata."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_artists = ["Artist One", "Artist Two", "Artist Three"]
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: test_artists}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == test_artists

    def test_artists_separation_formats(self, artists_one_two_three_comma_id3v2, artists_one_two_three_semicolon_id3v2, artists_one_two_three_multi_tags_vorbis):
        """Test different artist separation formats."""
        # Comma separation (ID3v2)
        metadata = get_merged_app_metadata(artists_one_two_three_comma_id3v2)
        artists = metadata.get(AppMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert "One Two Three" in artists
        
        # Semicolon separation (ID3v2)
        metadata = get_merged_app_metadata(artists_one_two_three_semicolon_id3v2)
        artists = metadata.get(AppMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert "One Two Three" in artists
        
        # Multi-tags (Vorbis)
        metadata = get_merged_app_metadata(artists_one_two_three_multi_tags_vorbis)
        artists = metadata.get(AppMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert "One Two Three" in artists

