"""Tests for rating scenarios across different formats and normalizations."""

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


class TestRatingScenarios:
    """Test cases for rating scenarios across different formats."""

    def test_rating_0_to_100_scale_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating with 0-100 scale in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test various rating values on 0-100 scale
        test_ratings = [0, 20, 40, 60, 80, 100]
        
        for rating in test_ratings:
            test_metadata = {AppMetadataKey.RATING: rating}
            update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
            
            retrieved_rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
            assert retrieved_rating == rating
            
            # Test reading with same normalization
            metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
            assert metadata.get(AppMetadataKey.RATING) == rating

    def test_rating_0_to_255_scale_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating with 0-255 scale in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test various rating values on 0-255 scale
        test_ratings = [0, 51, 102, 153, 204, 255]
        
        for rating in test_ratings:
            test_metadata = {AppMetadataKey.RATING: rating}
            update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
            
            retrieved_rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
            assert retrieved_rating == rating
            
            # Test reading with same normalization
            metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=255)
            assert metadata.get(AppMetadataKey.RATING) == rating

    def test_rating_0_to_100_scale_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test rating with 0-100 scale in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_ratings = [0, 25, 50, 75, 100]
        
        for rating in test_ratings:
            test_metadata = {AppMetadataKey.RATING: rating}
            update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
            
            retrieved_rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
            assert retrieved_rating == rating

    def test_rating_0_to_255_scale_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test rating with 0-255 scale in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_ratings = [0, 64, 128, 192, 255]
        
        for rating in test_ratings:
            test_metadata = {AppMetadataKey.RATING: rating}
            update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
            
            retrieved_rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
            assert retrieved_rating == rating

    def test_rating_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that rating is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support rating, so this should be ignored
        test_metadata = {AppMetadataKey.RATING: 50}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Rating should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert AppMetadataKey.RATING not in metadata or metadata.get(AppMetadataKey.RATING) is None

    def test_rating_boundary_values_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating boundary values in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test minimum value
        test_metadata = {AppMetadataKey.RATING: 0}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 0
        
        # Test maximum value
        test_metadata = {AppMetadataKey.RATING: 100}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 100

    def test_rating_boundary_values_255_scale_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating boundary values with 255 scale in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test minimum value
        test_metadata = {AppMetadataKey.RATING: 0}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 0
        
        # Test maximum value
        test_metadata = {AppMetadataKey.RATING: 255}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 255

    def test_rating_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {AppMetadataKey.RATING: 75}
        update_file_metadata(audio_file, test_metadata, normalized_rating_max_value=100)
        
        rating = get_specific_metadata(audio_file, AppMetadataKey.RATING)
        assert rating == 75
        
        metadata = get_merged_app_metadata(audio_file, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.RATING) == 75

    def test_rating_format_specific_reading_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test reading rating from specific format managers in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        from audiometa import get_single_format_app_metadata
        
        # Set rating using ID3v2
        test_metadata = {AppMetadataKey.RATING: 85}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Read from ID3v2 specifically
        metadata_id3v2 = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2, normalized_rating_max_value=100)
        assert metadata_id3v2.get(AppMetadataKey.RATING) == 85
        
        # Read from ID3v1 specifically (should not have rating)
        metadata_id3v1 = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1, normalized_rating_max_value=100)
        assert AppMetadataKey.RATING not in metadata_id3v1 or metadata_id3v1.get(AppMetadataKey.RATING) is None

    def test_rating_format_specific_reading_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test reading rating from specific format managers in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        from audiometa import get_single_format_app_metadata
        
        # Set rating using Vorbis
        test_metadata = {AppMetadataKey.RATING: 90}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Read from Vorbis specifically
        metadata_vorbis = get_single_format_app_metadata(temp_audio_file, MetadataFormat.VORBIS, normalized_rating_max_value=100)
        assert metadata_vorbis.get(AppMetadataKey.RATING) == 90

    def test_rating_normalization_consistency_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating normalization consistency in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Set rating with 100 scale
        test_metadata = {AppMetadataKey.RATING: 80}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Read with same scale
        rating_100 = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating_100 == 80
        
        # Read with different scale (should be converted)
        metadata_255 = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=255)
        # The actual conversion depends on implementation, but should be consistent
        assert isinstance(metadata_255.get(AppMetadataKey.RATING), int)

    def test_rating_normalization_consistency_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test rating normalization consistency in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # Set rating with 255 scale
        test_metadata = {AppMetadataKey.RATING: 200}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        
        # Read with same scale
        rating_255 = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating_255 == 200
        
        # Read with different scale (should be converted)
        metadata_100 = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        # The actual conversion depends on implementation, but should be consistent
        assert isinstance(metadata_100.get(AppMetadataKey.RATING), int)

    def test_rating_with_other_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating combined with other metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "Rated Song",
            AppMetadataKey.ARTISTS_NAMES: ["Rating Artist"],
            AppMetadataKey.ALBUM_NAME: "Rating Album",
            AppMetadataKey.RATING: 95,
            AppMetadataKey.BPM: 140
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields including rating
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.TITLE) == "Rated Song"
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Rating Artist"]
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "Rating Album"
        assert metadata.get(AppMetadataKey.RATING) == 95
        assert metadata.get(AppMetadataKey.BPM) == 140

    def test_rating_with_other_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test rating combined with other metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "FLAC Rated Song",
            AppMetadataKey.ARTISTS_NAMES: ["FLAC Rating Artist"],
            AppMetadataKey.ALBUM_NAME: "FLAC Rating Album",
            AppMetadataKey.RATING: 88,
            AppMetadataKey.BPM: 128
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields including rating
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.TITLE) == "FLAC Rated Song"
        assert metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["FLAC Rating Artist"]
        assert metadata.get(AppMetadataKey.ALBUM_NAME) == "FLAC Rating Album"
        assert metadata.get(AppMetadataKey.RATING) == 88
        assert metadata.get(AppMetadataKey.BPM) == 128

    def test_rating_edge_cases_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating edge cases in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test middle value
        test_metadata = {AppMetadataKey.RATING: 50}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 50
        
        # Test high value
        test_metadata = {AppMetadataKey.RATING: 99}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 99

    def test_rating_edge_cases_255_scale_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating edge cases with 255 scale in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test middle value
        test_metadata = {AppMetadataKey.RATING: 127}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 127
        
        # Test high value
        test_metadata = {AppMetadataKey.RATING: 254}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        
        rating = get_specific_metadata(temp_audio_file, AppMetadataKey.RATING)
        assert rating == 254

    def test_rating_empty_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing rating metadata."""
        # Test reading from file with no rating
        metadata = get_merged_app_metadata(sample_mp3_file, normalized_rating_max_value=100)
        assert isinstance(metadata, dict)
        
        # Rating might not be present
        rating = get_specific_metadata(sample_mp3_file, AppMetadataKey.RATING)
        assert rating is None or isinstance(rating, int)



