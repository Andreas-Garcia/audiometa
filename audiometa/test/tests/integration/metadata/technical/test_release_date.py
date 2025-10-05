"""Tests for release date metadata."""

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
class TestReleaseDateMetadata:
    """Test cases for release date metadata."""

    def test_release_date_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test release date metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: "2024-03-15"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert date == "2024-03-15"

    def test_release_date_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test release date metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: "2024-03-15"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert date == "2024-03-15"

    def test_release_date_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test release date metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: "2024-03-15"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert date == "2024-03-15"

    def test_release_date_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test release date metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.RELEASE_DATE: "2024-03-15"}
        update_file_metadata(audio_file, test_metadata)
        
        date = get_specific_metadata(audio_file, UnifiedMetadataKey.RELEASE_DATE)
        assert date == "2024-03-15"

    def test_release_date_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test release date metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different date formats
        test_dates = ["2024-03-15", "2024-12-31", "2020-01-01"]
        for date in test_dates:
            test_metadata = {UnifiedMetadataKey.RELEASE_DATE: date}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_date = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RELEASE_DATE)
            assert retrieved_date == date

