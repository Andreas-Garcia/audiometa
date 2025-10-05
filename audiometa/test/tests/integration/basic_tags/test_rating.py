"""Tests for rating metadata."""

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
class TestRatingMetadata:
    """Test cases for rating metadata."""

    def test_rating_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_rating = 85
        test_metadata = {AppMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RATING) == test_rating

    def test_rating_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test rating metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_rating = 90
        test_metadata = {AppMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RATING) == test_rating

    def test_rating_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test rating metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_rating = 75
        test_metadata = {AppMetadataKey.RATING: test_rating}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RATING) == test_rating

    def test_rating_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_rating = 95
        test_metadata = {AppMetadataKey.RATING: test_rating}
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.RATING) == test_rating

    def test_rating_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test rating metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test minimum rating
        min_rating = 0
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: min_rating})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RATING) == min_rating
        
        # Test maximum rating
        max_rating = 100
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: max_rating})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RATING) == max_rating
        
        # Test middle rating
        mid_rating = 50
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: mid_rating})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RATING) == mid_rating

    def test_mp3_id3v2_rating_scenarios(self, rating_id3v2_base_255_5_star_mp3):
        """Test MP3 ID3v2 rating scenarios."""
        # Base 255 normalization
        metadata = get_merged_app_metadata(rating_id3v2_base_255_5_star_mp3, normalized_rating_max_value=255)
        assert metadata.get(AppMetadataKey.RATING) == 10
        
        # Base 100 normalization (should still work)
        metadata = get_merged_app_metadata(rating_id3v2_base_255_5_star_mp3, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.RATING) == 10

    def test_wav_id3v2_rating_scenarios(self, rating_id3v2_base_100_0_star_wav, rating_id3v2_base_100_5_star_wav):
        """Test WAV ID3v2 rating scenarios."""
        # 0 star rating
        metadata = get_merged_app_metadata(rating_id3v2_base_100_0_star_wav, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.RATING) == 0
        
        # 5 star rating
        metadata = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.RATING) == 10

    def test_wav_riff_rating_scenarios(self, rating_riff_base_100_5_star_wav):
        """Test WAV RIFF rating scenarios."""
        metadata = get_merged_app_metadata(rating_riff_base_100_5_star_wav, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.RATING) == 10

    def test_flac_vorbis_rating_scenarios(self, rating_vorbis_base_100_5_star_flac):
        """Test FLAC Vorbis rating scenarios."""
        metadata = get_merged_app_metadata(rating_vorbis_base_100_5_star_flac, normalized_rating_max_value=100)
        assert metadata.get(AppMetadataKey.RATING) == 10

    def test_id3v2_rating_base_100_scenarios(self, rating_id3v2_base_100_0_star_wav, rating_id3v2_base_100_5_star_wav):
        """Test ID3v2 rating scenarios with base 100 normalization."""
        # 0 star rating
        metadata = get_merged_app_metadata(rating_id3v2_base_100_0_star_wav, normalized_rating_max_value=100)
        assert metadata[AppMetadataKey.RATING] == 0
        
        # 5 star rating
        metadata = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=100)
        assert metadata[AppMetadataKey.RATING] == 10

    def test_id3v2_rating_base_255_scenarios(self, rating_id3v2_base_255_5_star_mp3):
        """Test ID3v2 rating scenarios with base 255 normalization."""
        metadata = get_merged_app_metadata(rating_id3v2_base_255_5_star_mp3, normalized_rating_max_value=255)
        assert metadata[AppMetadataKey.RATING] == 10

    def test_riff_rating_base_100_scenarios(self, rating_riff_base_100_5_star_wav):
        """Test RIFF rating scenarios with base 100 normalization."""
        metadata = get_merged_app_metadata(rating_riff_base_100_5_star_wav, normalized_rating_max_value=100)
        assert metadata[AppMetadataKey.RATING] == 10

    def test_vorbis_rating_base_100_scenarios(self, rating_vorbis_base_100_5_star_flac):
        """Test Vorbis rating scenarios with base 100 normalization."""
        metadata = get_merged_app_metadata(rating_vorbis_base_100_5_star_flac, normalized_rating_max_value=100)
        assert metadata[AppMetadataKey.RATING] == 10

    def test_rating_normalization_consistency(self, rating_id3v2_base_100_5_star_wav):
        """Test that rating normalization is consistent across different base values."""
        # Base 100 normalization
        metadata_100 = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=100)
        rating_100 = metadata_100[AppMetadataKey.RATING]
        
        # Base 255 normalization
        metadata_255 = get_merged_app_metadata(rating_id3v2_base_100_5_star_wav, normalized_rating_max_value=255)
        rating_255 = metadata_255[AppMetadataKey.RATING]
        
        # Both should represent the same 5-star rating (10/10)
        assert rating_100 == 10
        assert rating_255 == 10

    def test_rating_edge_cases(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test rating edge cases."""
        import shutil
        from audiometa import update_file_metadata
        
        # Test rating 0
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: 0})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata[AppMetadataKey.RATING] == 0
        
        # Test rating 10 (maximum)
        shutil.copy2(metadata_none_flac, temp_audio_file)
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: 10})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata[AppMetadataKey.RATING] == 10
        
        # Test rating 5 (middle)
        shutil.copy2(metadata_none_wav, temp_audio_file)
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: 5})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata[AppMetadataKey.RATING] == 5

    def test_rating_with_different_formats(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test rating with different audio formats."""
        import shutil
        from audiometa import update_file_metadata
        
        # Test MP3 (ID3v2)
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: 8}, normalized_rating_max_value=255)
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=255)
        assert metadata[AppMetadataKey.RATING] == 8
        
        # Test FLAC (Vorbis)
        shutil.copy2(metadata_none_flac, temp_audio_file)
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: 8}, normalized_rating_max_value=100)
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata[AppMetadataKey.RATING] == 8
        
        # Test WAV (RIFF)
        shutil.copy2(metadata_none_wav, temp_audio_file)
        update_file_metadata(temp_audio_file, {AppMetadataKey.RATING: 8}, normalized_rating_max_value=100)
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata[AppMetadataKey.RATING] == 8

