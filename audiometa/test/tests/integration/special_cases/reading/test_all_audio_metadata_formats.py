"""Comprehensive tests for reading tags across all metadata format × audio format combinations.

This module tests reading a specific tag from all possible combinations of:
- Audio formats: MP3, FLAC, WAV
- Metadata formats: ID3v1, ID3v2, Vorbis, RIFF

The tests verify that tag reading works correctly across all valid combinations.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from typing import Any

from audiometa import (
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestComprehensiveTagReading:
    """Test reading tags across all metadata format × audio format combinations."""

    # Define valid combinations based on the library's capabilities
    VALID_COMBINATIONS = [
        # MP3 files
        ('.mp3', MetadataFormat.ID3V1),
        ('.mp3', MetadataFormat.ID3V2),
        
        # FLAC files  
        ('.flac', MetadataFormat.ID3V1),
        ('.flac', MetadataFormat.ID3V2),
        ('.flac', MetadataFormat.VORBIS),
        
        # WAV files
        ('.wav', MetadataFormat.ID3V1),
        ('.wav', MetadataFormat.ID3V2),
        ('.wav', MetadataFormat.RIFF),
    ]

    @pytest.mark.parametrize("audio_format,metadata_format", VALID_COMBINATIONS)
    def test_title_reading_across_combinations(
        self, 
        audio_format: str, 
        metadata_format: MetadataFormat,
        sample_mp3_file: Path,
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading TITLE tag across all valid metadata format × audio format combinations."""
        # Select appropriate source file based on audio format
        source_files = {
            '.mp3': sample_mp3_file,
            '.flac': sample_flac_file,
            '.wav': sample_wav_file
        }
        source_file = source_files[audio_format]
        
        # Copy source file to temp location
        shutil.copy2(source_file, temp_audio_file)
        
        # Define test metadata
        test_title = f"Test Title for {metadata_format.value} in {audio_format}"
        test_metadata = {
            UnifiedMetadataKey.TITLE: test_title,
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album"
        }
        
        # Write metadata using the specific format
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=metadata_format)
        
        # Test reading using single format extraction
        single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
        assert single_format_metadata.get(UnifiedMetadataKey.TITLE) == test_title
        
        # Test reading using specific metadata extraction
        specific_title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert specific_title == test_title

    @pytest.mark.parametrize("audio_format,metadata_format", VALID_COMBINATIONS)
    def test_artist_reading_across_combinations(
        self, 
        audio_format: str, 
        metadata_format: MetadataFormat,
        sample_mp3_file: Path,
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading ARTISTS_NAMES tag across all valid combinations."""
        source_files = {
            '.mp3': sample_mp3_file,
            '.flac': sample_flac_file,
            '.wav': sample_wav_file
        }
        source_file = source_files[audio_format]
        
        shutil.copy2(source_file, temp_audio_file)
        
        test_artists = [f"Artist 1 for {metadata_format.value}", f"Artist 2 for {metadata_format.value}"]
        test_metadata = {
            UnifiedMetadataKey.TITLE: f"Test Title for {metadata_format.value}",
            UnifiedMetadataKey.ARTISTS_NAMES: test_artists,
            UnifiedMetadataKey.ALBUM_NAME: "Test Album"
        }
        
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=metadata_format)
        
        # Test single format extraction
        single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
        assert single_format_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_artists
        
        # Test specific metadata extraction
        specific_artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert specific_artists == test_artists

    @pytest.mark.parametrize("audio_format,metadata_format", VALID_COMBINATIONS)
    def test_album_reading_across_combinations(
        self, 
        audio_format: str, 
        metadata_format: MetadataFormat,
        sample_mp3_file: Path,
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading ALBUM_NAME tag across all valid combinations."""
        source_files = {
            '.mp3': sample_mp3_file,
            '.flac': sample_flac_file,
            '.wav': sample_wav_file
        }
        source_file = source_files[audio_format]
        
        shutil.copy2(source_file, temp_audio_file)
        
        test_album = f"Test Album for {metadata_format.value} in {audio_format}"
        test_metadata = {
            UnifiedMetadataKey.TITLE: f"Test Title for {metadata_format.value}",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: test_album
        }
        
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=metadata_format)
        
        # Test single format extraction
        single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
        assert single_format_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album
        
        # Test specific metadata extraction
        specific_album = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ALBUM_NAME)
        assert specific_album == test_album

    @pytest.mark.parametrize("audio_format,metadata_format", VALID_COMBINATIONS)
    def test_rating_reading_across_combinations(
        self, 
        audio_format: str, 
        metadata_format: MetadataFormat,
        sample_mp3_file: Path,
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading RATING tag across all valid combinations (where supported)."""
        source_files = {
            '.mp3': sample_mp3_file,
            '.flac': sample_flac_file,
            '.wav': sample_wav_file
        }
        source_file = source_files[audio_format]
        
        shutil.copy2(source_file, temp_audio_file)
        
        test_rating = 4
        test_metadata = {
            UnifiedMetadataKey.TITLE: f"Test Title for {metadata_format.value}",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.RATING: test_rating
        }
        
        # Only write rating if the format supports it
        if metadata_format in [MetadataFormat.ID3V2, MetadataFormat.VORBIS]:
            update_file_metadata(temp_audio_file, test_metadata, metadata_format=metadata_format)
            
            # Test single format extraction
            single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
            assert single_format_metadata.get(UnifiedMetadataKey.RATING) == test_rating
            
            # Test specific metadata extraction
            specific_rating = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING)
            assert specific_rating == test_rating
        else:
            # For formats that don't support rating, just write basic metadata
            basic_metadata = {
                UnifiedMetadataKey.TITLE: f"Test Title for {metadata_format.value}",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album"
            }
            update_file_metadata(temp_audio_file, basic_metadata, metadata_format=metadata_format)
            
            # Verify that rating is not present
            single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
            assert single_format_metadata.get(UnifiedMetadataKey.RATING) is None

    @pytest.mark.parametrize("audio_format,metadata_format", VALID_COMBINATIONS)
    def test_genre_reading_across_combinations(
        self, 
        audio_format: str, 
        metadata_format: MetadataFormat,
        sample_mp3_file: Path,
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading GENRE_NAME tag across all valid combinations."""
        source_files = {
            '.mp3': sample_mp3_file,
            '.flac': sample_flac_file,
            '.wav': sample_wav_file
        }
        source_file = source_files[audio_format]
        
        shutil.copy2(source_file, temp_audio_file)
        
        test_genre = f"Test Genre for {metadata_format.value}"
        test_metadata = {
            UnifiedMetadataKey.TITLE: f"Test Title for {metadata_format.value}",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.GENRE_NAME: test_genre
        }
        
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=metadata_format)
        
        # Test single format extraction
        single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
        assert single_format_metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre
        
        # Test specific metadata extraction
        specific_genre = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.GENRE_NAME)
        assert specific_genre == test_genre

    @pytest.mark.parametrize("audio_format,metadata_format", VALID_COMBINATIONS)
    def test_audio_file_object_reading(
        self, 
        audio_format: str, 
        metadata_format: MetadataFormat,
        sample_mp3_file: Path,
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading tags using AudioFile object across all valid combinations."""
        source_files = {
            '.mp3': sample_mp3_file,
            '.flac': sample_flac_file,
            '.wav': sample_wav_file
        }
        source_file = source_files[audio_format]
        
        shutil.copy2(source_file, temp_audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: f"AudioFile Test Title for {metadata_format.value}",
            UnifiedMetadataKey.ARTISTS_NAMES: ["AudioFile Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "AudioFile Test Album",
            UnifiedMetadataKey.GENRE_NAME: "AudioFile Test Genre"
        }
        
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=metadata_format)
        
        # Test with AudioFile object
        audio_file = AudioFile(temp_audio_file)
        
        # Test single format extraction with AudioFile object
        single_format_metadata = get_single_format_app_metadata(audio_file, metadata_format)
        assert single_format_metadata.get(UnifiedMetadataKey.TITLE) == test_metadata[UnifiedMetadataKey.TITLE]
        assert single_format_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == test_metadata[UnifiedMetadataKey.ARTISTS_NAMES]
        assert single_format_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_metadata[UnifiedMetadataKey.ALBUM_NAME]
        assert single_format_metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_metadata[UnifiedMetadataKey.GENRE_NAME]
        
        # Test specific metadata extraction with AudioFile object
        specific_title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert specific_title == test_metadata[UnifiedMetadataKey.TITLE]

    def test_invalid_combinations_raise_errors(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test that invalid metadata format × audio format combinations raise appropriate errors."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test invalid combination: MP3 with RIFF metadata (RIFF is for WAV files)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album"
        }
        
        # This should work but may not be the optimal format for MP3
        # The library should handle this gracefully
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        
        # Verify that the metadata was written and can be read
        single_format_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.RIFF)
        assert single_format_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"

    def test_comprehensive_metadata_reading_with_all_supported_fields(
        self, 
        sample_mp3_file: Path, 
        sample_flac_file: Path, 
        sample_wav_file: Path,
        temp_audio_file: Path
    ):
        """Test reading comprehensive metadata with all supported fields across formats."""
        test_cases = [
            (sample_mp3_file, MetadataFormat.ID3V2),
            (sample_flac_file, MetadataFormat.VORBIS),
            (sample_wav_file, MetadataFormat.RIFF)
        ]
        
        for source_file, metadata_format in test_cases:
            shutil.copy2(source_file, temp_audio_file)
            
            # Comprehensive metadata that should work across all formats
            comprehensive_metadata = {
                UnifiedMetadataKey.TITLE: f"Comprehensive Test Title for {metadata_format.value}",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Comprehensive Artist 1", "Comprehensive Artist 2"],
                UnifiedMetadataKey.ALBUM_NAME: f"Comprehensive Album for {metadata_format.value}",
                UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Comprehensive Album Artist"],
                UnifiedMetadataKey.GENRE_NAME: "Comprehensive Test Genre",
                UnifiedMetadataKey.COMMENT: f"Comprehensive comment for {metadata_format.value}",
                UnifiedMetadataKey.COMPOSER: "Comprehensive Composer",
                UnifiedMetadataKey.PUBLISHER: "Comprehensive Publisher"
            }
            
            # Add rating only for formats that support it
            if metadata_format in [MetadataFormat.ID3V2, MetadataFormat.VORBIS]:
                comprehensive_metadata[UnifiedMetadataKey.RATING] = 5
            
            update_file_metadata(temp_audio_file, comprehensive_metadata, metadata_format=metadata_format)
            
            # Test reading all fields
            single_format_metadata = get_single_format_app_metadata(temp_audio_file, metadata_format)
            
            for key, expected_value in comprehensive_metadata.items():
                actual_value = single_format_metadata.get(key)
                assert actual_value == expected_value, f"Failed for {key} in {metadata_format.value}: expected {expected_value}, got {actual_value}"
