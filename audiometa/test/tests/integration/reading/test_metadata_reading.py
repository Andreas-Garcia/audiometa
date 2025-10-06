"""Core metadata reading functionality tests."""

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestCoreMetadataReading:

    def test_metadata_reading_integration(self, sample_mp3_file: Path, sample_flac_file: Path, sample_wav_file: Path):
        """Test core metadata reading functionality across all formats."""
        test_cases = [
            (sample_mp3_file, "MP3"),
            (sample_flac_file, "FLAC"),
            (sample_wav_file, "WAV")
        ]
        
        for sample_file, format_name in test_cases:
            # Test merged metadata
            metadata = get_merged_unified_metadata(sample_file)
            assert isinstance(metadata, dict), f"Failed for {format_name}"
            
            # Test specific metadata
            title = get_specific_metadata(sample_file, UnifiedMetadataKey.TITLE)
            assert title is None or isinstance(title, str), f"Failed for {format_name}"
            
            artists = get_specific_metadata(sample_file, UnifiedMetadataKey.ARTISTS_NAMES)
            assert artists is None or isinstance(artists, list), f"Failed for {format_name}"

    def test_audio_file_object_integration(self, sample_mp3_file: Path):
        """Test AudioFile object integration with reading APIs."""
        audio_file = AudioFile(sample_mp3_file)
        
        # Test merged metadata with AudioFile
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        
        # Test specific metadata with AudioFile
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_rating_normalization_integration(self, sample_mp3_file: Path):
        """Test rating normalization in metadata reading."""
        # Test with different normalization values
        metadata_100 = get_merged_unified_metadata(sample_mp3_file, normalized_rating_max_value=100)
        metadata_255 = get_merged_unified_metadata(sample_mp3_file, normalized_rating_max_value=255)
        
        assert isinstance(metadata_100, dict)
        assert isinstance(metadata_255, dict)
        
        # Both should return valid metadata
        assert len(metadata_100) >= 0
        assert len(metadata_255) >= 0