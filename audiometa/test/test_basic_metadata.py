"""Tests for basic metadata fields (title, artist, album, genre, rating)."""

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
from audiometa.utils.TagFormat import MetadataFormat


class TestBasicMetadata:
    """Test cases for basic metadata fields."""

    def test_title_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test title metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test writing title
        test_metadata = {AppMetadataKey.TITLE: "Test Song Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Test reading title
        title = get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE)
        assert title == "Test Song Title"
        
        # Test reading from merged metadata
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == "Test Song Title"

    def test_title_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test title metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.TITLE: "FLAC Test Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        title = get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE)
        assert title == "FLAC Test Title"

    def test_title_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test title metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.TITLE: "WAV Test Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        title = get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE)
        assert title == "WAV Test Title"

    def test_artists_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test artists metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test single artist
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: ["Test Artist"]}
        update_file_metadata(temp_audio_file, test_metadata)
        
        artists = get_specific_metadata(temp_audio_file, AppMetadataKey.ARTISTS_NAMES)
        assert artists == ["Test Artist"]
        
        # Test multiple artists
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]}
        update_file_metadata(temp_audio_file, test_metadata)
        
        artists = get_specific_metadata(temp_audio_file, AppMetadataKey.ARTISTS_NAMES)
        assert artists == ["Artist One", "Artist Two", "Artist Three"]

    def test_artists_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test artists metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ARTISTS_NAMES: ["FLAC Artist One", "FLAC Artist Two"]}
        update_file_metadata(temp_audio_file, test_metadata)
        
        artists = get_specific_metadata(temp_audio_file, AppMetadataKey.ARTISTS_NAMES)
        assert artists == ["FLAC Artist One", "FLAC Artist Two"]

    def test_album_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test album metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ALBUM_NAME: "Test Album Name"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        album = get_specific_metadata(temp_audio_file, AppMetadataKey.ALBUM_NAME)
        assert album == "Test Album Name"

    def test_album_artists_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test album artists metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist One", "Album Artist Two"]}
        update_file_metadata(temp_audio_file, test_metadata)
        
        album_artists = get_specific_metadata(temp_audio_file, AppMetadataKey.ALBUM_ARTISTS_NAMES)
        assert album_artists == ["Album Artist One", "Album Artist Two"]

    def test_genre_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test genre metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.GENRE_NAME: "Electronic"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        genre = get_specific_metadata(temp_audio_file, AppMetadataKey.GENRE_NAME)
        assert genre == "Electronic"

    def test_rating_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different rating values
        for rating in [0, 25, 50, 75, 100]:
            test_metadata = {AppMetadataKey.RATING: rating}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
            assert retrieved_rating == rating

    def test_rating_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test rating metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.RATING: 85}
        update_file_metadata(temp_audio_file, test_metadata)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 85

    def test_rating_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that rating is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support rating, so this should be ignored
        test_metadata = {AppMetadataKey.RATING: 50}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Rating should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.RATING not in metadata or metadata.get(AppMetadataKey.RATING) is None

    def test_complete_basic_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all basic metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "Complete Test Song",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist 1", "Test Artist 2"],
            AppMetadataKey.ALBUM_NAME: "Complete Test Album",
            AppMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist"],
            AppMetadataKey.GENRE_NAME: "Rock",
            AppMetadataKey.RATING: 90
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == "Complete Test Song"
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist 1", "Test Artist 2"]
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "Complete Test Album"
        assert metadata.get(AppMetadataKey.ALBUM_ARTISTS_NAMES) == ["Album Artist"]
        assert metadata.get(AppMetadataKey.GENRE_NAME) == "Rock"
        assert metadata.get(AppMetadataKey.RATING) == 90

    def test_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test basic metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "AudioFile Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["AudioFile Test Artist"]
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == "AudioFile Test Title"
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["AudioFile Test Artist"]

    def test_metadata_reading_with_different_formats(self, sample_mp3_file: Path):
        """Test reading metadata from different format managers."""
        # Test ID3v2 format specifically
        from audiometa import get_single_format_app_metadata
        
        metadata_id3v2 = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V2)
        assert isinstance(metadata_id3v2, dict)
        
        # Test ID3v1 format specifically
        metadata_id3v1 = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V1)
        assert isinstance(metadata_id3v1, dict)

    def test_empty_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing metadata."""
        # Test reading from file with no metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific metadata that doesn't exist
        title = get_specific_metadata(sample_mp3_file, AppMetadataKey.TITLE)
        assert title is None or isinstance(title, str)
        
        artists = get_specific_metadata(sample_mp3_file, AppMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)



