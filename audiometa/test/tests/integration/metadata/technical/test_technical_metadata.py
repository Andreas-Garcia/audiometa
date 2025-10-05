"""Tests for complete technical metadata workflows."""

import pytest
from pathlib import Path
import shutil

from audiometa import (
    get_merged_app_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestTechnicalMetadata:
    """Test cases for complete technical metadata workflows."""

    def test_complete_technical_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all technical metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.RELEASE_DATE: "2024-01-15",
            UnifiedMetadataKey.TRACK_NUMBER: 3,
            UnifiedMetadataKey.BPM: 140,
            UnifiedMetadataKey.LANGUAGE: "en"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.RELEASE_DATE) == "2024-01-15"
        assert metadata.get(UnifiedMetadataKey.TRACK_NUMBER) == 3
        assert metadata.get(UnifiedMetadataKey.BPM) == 140
        assert metadata.get(UnifiedMetadataKey.LANGUAGE) == "en"

    def test_technical_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test technical metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.RELEASE_DATE: "2024-02-20",
            UnifiedMetadataKey.TRACK_NUMBER: 5,
            UnifiedMetadataKey.BPM: 128
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(UnifiedMetadataKey.RELEASE_DATE) == "2024-02-20"
        assert metadata.get(UnifiedMetadataKey.TRACK_NUMBER) == 5
        assert metadata.get(UnifiedMetadataKey.BPM) == 128

    def test_metadata_reading_with_different_formats(self, sample_mp3_file: Path):
        """Test reading technical metadata from different format managers."""
        from audiometa import get_single_format_app_metadata
        
        # Test ID3v2 format specifically
        metadata_id3v2 = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V2)
        assert isinstance(metadata_id3v2, dict)
        
        # Test ID3v1 format specifically
        metadata_id3v1 = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V1)
        assert isinstance(metadata_id3v1, dict)

    def test_boundary_values(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test boundary values for technical metadata."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test minimum values
        test_metadata_min = {
            UnifiedMetadataKey.TRACK_NUMBER: 1,
            UnifiedMetadataKey.BPM: 1
        }
        update_file_metadata(temp_audio_file, test_metadata_min)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TRACK_NUMBER) == 1
        assert metadata.get(UnifiedMetadataKey.BPM) == 1
        
        # Test maximum values
        test_metadata_max = {
            UnifiedMetadataKey.TRACK_NUMBER: 999,
            UnifiedMetadataKey.BPM: 999
        }
        update_file_metadata(temp_audio_file, test_metadata_max)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TRACK_NUMBER) == 999
        assert metadata.get(UnifiedMetadataKey.BPM) == 999

    def test_empty_technical_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing technical metadata."""
        # Test reading from file with no technical metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific technical metadata that doesn't exist
        release_date = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date is None or isinstance(release_date, str)
        
        track_number = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number is None or isinstance(track_number, int)
        
        bpm = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.BPM)
        assert bpm is None or isinstance(bpm, int)
        
        language = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.LANGUAGE)
        assert language is None or isinstance(language, str)

    def test_technical_metadata_formats(self, bitrate_320_mp3, bitrate_946_flac, bitrate_1411_wav):
        """Test technical metadata across different formats."""
        # MP3 bitrate
        metadata = get_merged_app_metadata(bitrate_320_mp3)
        assert metadata.get(UnifiedMetadataKey.BITRATE) == 320
        
        # FLAC bitrate
        metadata = get_merged_app_metadata(bitrate_946_flac)
        assert metadata.get(UnifiedMetadataKey.BITRATE) == 946
        
        # WAV bitrate
        metadata = get_merged_app_metadata(bitrate_1411_wav)
        assert metadata.get(UnifiedMetadataKey.BITRATE) == 1411

    def test_duration_metadata_formats(self, duration_182s_mp3, duration_335s_flac, duration_472s_wav):
        """Test duration metadata across different formats."""
        # MP3 duration
        metadata = get_merged_app_metadata(duration_182s_mp3)
        assert abs(metadata.get(UnifiedMetadataKey.DURATION) - 182.0) < 1.0
        
        # FLAC duration
        metadata = get_merged_app_metadata(duration_335s_flac)
        assert abs(metadata.get(UnifiedMetadataKey.DURATION) - 335.0) < 1.0
        
        # WAV duration
        metadata = get_merged_app_metadata(duration_472s_wav)
        assert abs(metadata.get(UnifiedMetadataKey.DURATION) - 472.0) < 1.0

    def test_file_size_metadata_formats(self, size_small_mp3, size_big_mp3, size_small_flac, size_big_flac, size_small_wav, size_big_wav):
        """Test file size metadata across different formats."""
        # Small files
        metadata = get_merged_app_metadata(size_small_mp3)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_small_flac)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_small_wav)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        # Big files
        metadata = get_merged_app_metadata(size_big_mp3)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_big_flac)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_big_wav)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0

    def test_technical_metadata_reading(self, bitrate_320_mp3, bitrate_946_flac, bitrate_1411_wav, duration_182s_mp3, duration_335s_flac, duration_472s_wav):
        """Test reading technical metadata from different formats."""
        # Bitrate tests
        metadata = get_merged_app_metadata(bitrate_320_mp3)
        assert metadata.get(UnifiedMetadataKey.BITRATE) == 320
        
        metadata = get_merged_app_metadata(bitrate_946_flac)
        assert metadata.get(UnifiedMetadataKey.BITRATE) == 946
        
        metadata = get_merged_app_metadata(bitrate_1411_wav)
        assert metadata.get(UnifiedMetadataKey.BITRATE) == 1411
        
        # Duration tests
        metadata = get_merged_app_metadata(duration_182s_mp3)
        assert abs(metadata.get(UnifiedMetadataKey.DURATION) - 182.0) < 1.0
        
        metadata = get_merged_app_metadata(duration_335s_flac)
        assert abs(metadata.get(UnifiedMetadataKey.DURATION) - 335.0) < 1.0
        
        metadata = get_merged_app_metadata(duration_472s_wav)
        assert abs(metadata.get(UnifiedMetadataKey.DURATION) - 472.0) < 1.0

    def test_file_size_metadata_reading(self, size_small_mp3, size_big_mp3, size_small_flac, size_big_flac, size_small_wav, size_big_wav):
        """Test reading file size metadata from different formats."""
        # Small files
        metadata = get_merged_app_metadata(size_small_mp3)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_small_flac)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_small_wav)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        # Big files
        metadata = get_merged_app_metadata(size_big_mp3)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_big_flac)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0
        
        metadata = get_merged_app_metadata(size_big_wav)
        assert metadata.get(UnifiedMetadataKey.FILE_SIZE) > 0