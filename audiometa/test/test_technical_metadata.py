"""Tests for technical metadata fields (release date, track number, BPM, language)."""

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


class TestTechnicalMetadata:
    """Test cases for technical metadata fields."""

    def test_release_date_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test release date metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different date formats
        test_dates = ["2024-01-01", "2023-12-25", "2022-06-15"]
        
        for date in test_dates:
            test_metadata = {AppMetadataKey.RELEASE_DATE: date}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_date = get_specific_metadata(temp_audio_file, AppMetadataKey.RELEASE_DATE)
            assert retrieved_date == date

    def test_release_date_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test release date metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.RELEASE_DATE: "2024-03-15"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        date = get_specific_metadata(temp_audio_file, AppMetadataKey.RELEASE_DATE)
        assert date == "2024-03-15"

    def test_track_number_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test track number metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different track numbers
        test_tracks = [1, 5, 10, 15, 99]
        
        for track in test_tracks:
            test_metadata = {AppMetadataKey.TRACK_NUMBER: track}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_track = get_specific_metadata(temp_audio_file, AppMetadataKey.TRACK_NUMBER)
            assert retrieved_track == track

    def test_track_number_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test track number metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.TRACK_NUMBER: 7}
        update_file_metadata(temp_audio_file, test_metadata)
        
        track = get_specific_metadata(temp_audio_file, AppMetadataKey.TRACK_NUMBER)
        assert track == 7

    def test_bpm_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test BPM metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different BPM values
        test_bpms = [120, 140, 160, 180, 200]
        
        for bpm in test_bpms:
            test_metadata = {AppMetadataKey.BPM: bpm}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_bpm = get_specific_metadata(temp_audio_file, AppMetadataKey.BPM)
            assert retrieved_bpm == bpm

    def test_bpm_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test BPM metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.BPM: 128}
        update_file_metadata(temp_audio_file, test_metadata)
        
        bpm = get_specific_metadata(temp_audio_file, AppMetadataKey.BPM)
        assert bpm == 128

    def test_bpm_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that BPM is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support BPM, so this should be ignored
        test_metadata = {AppMetadataKey.BPM: 120}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # BPM should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.BPM not in metadata or metadata.get(AppMetadataKey.BPM) is None

    def test_language_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test language metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different language codes
        test_languages = ["en", "fr", "de", "es", "it"]
        
        for lang in test_languages:
            test_metadata = {AppMetadataKey.LANGUAGE: lang}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_lang = get_specific_metadata(temp_audio_file, AppMetadataKey.LANGUAGE)
            assert retrieved_lang == lang

    def test_language_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test language metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.LANGUAGE: "en"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        language = get_specific_metadata(temp_audio_file, AppMetadataKey.LANGUAGE)
        assert language == "en"

    def test_language_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that language is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support language, so this should be ignored
        test_metadata = {AppMetadataKey.LANGUAGE: "en"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Language should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.LANGUAGE not in metadata or metadata.get(AppMetadataKey.LANGUAGE) is None

    def test_complete_technical_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all technical metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.RELEASE_DATE: "2024-01-15",
            AppMetadataKey.TRACK_NUMBER: 3,
            AppMetadataKey.BPM: 140,
            AppMetadataKey.LANGUAGE: "en"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.RELEASE_DATE) == "2024-01-15"
        assert metadata.get(AppMetadataKey.TRACK_NUMBER) == 3
        assert metadata.get(AppMetadataKey.BPM) == 140
        assert metadata.get(AppMetadataKey.LANGUAGE) == "en"

    def test_technical_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test technical metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.RELEASE_DATE: "2024-02-20",
            AppMetadataKey.TRACK_NUMBER: 5,
            AppMetadataKey.BPM: 128
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.RELEASE_DATE) == "2024-02-20"
        assert metadata.get(AppMetadataKey.TRACK_NUMBER) == 5
        assert metadata.get(AppMetadataKey.BPM) == 128

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
            AppMetadataKey.TRACK_NUMBER: 1,
            AppMetadataKey.BPM: 1
        }
        update_file_metadata(temp_audio_file, test_metadata_min)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TRACK_NUMBER) == 1
        assert metadata.get(AppMetadataKey.BPM) == 1
        
        # Test maximum values
        test_metadata_max = {
            AppMetadataKey.TRACK_NUMBER: 999,
            AppMetadataKey.BPM: 999
        }
        update_file_metadata(temp_audio_file, test_metadata_max)
        
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TRACK_NUMBER) == 999
        assert metadata.get(AppMetadataKey.BPM) == 999

    def test_empty_technical_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing technical metadata."""
        # Test reading from file with no technical metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific technical metadata that doesn't exist
        release_date = get_specific_metadata(sample_mp3_file, AppMetadataKey.RELEASE_DATE)
        assert release_date is None or isinstance(release_date, str)
        
        track_number = get_specific_metadata(sample_mp3_file, AppMetadataKey.TRACK_NUMBER)
        assert track_number is None or isinstance(track_number, int)
        
        bpm = get_specific_metadata(sample_mp3_file, AppMetadataKey.BPM)
        assert bpm is None or isinstance(bpm, int)
        
        language = get_specific_metadata(sample_mp3_file, AppMetadataKey.LANGUAGE)
        assert language is None or isinstance(language, str)



