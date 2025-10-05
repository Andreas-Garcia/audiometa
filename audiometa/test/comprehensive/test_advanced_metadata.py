"""Tests for complete advanced metadata workflows."""

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
from audiometa.utils.MetadataSingleFormat import MetadataSingleFormat


@pytest.mark.comprehensive
class TestAdvancedMetadata:
    """Test cases for complete advanced metadata workflows."""

    def test_complete_advanced_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all advanced metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.COVER_ART: b"test_cover_art_data",
            AppMetadataKey.COMPILATION: True,
            AppMetadataKey.MEDIA_TYPE: "Digital Media",
            AppMetadataKey.FILE_OWNER: "Test Owner",
            AppMetadataKey.RECORDING_DATE: "2024-01-15",
            AppMetadataKey.ENCODER_SETTINGS: "VBR 0",
            AppMetadataKey.REPLAYGAIN: "Track Gain: -3.2 dB",
            AppMetadataKey.MUSICBRAINZ_ID: "4a45b00b-273d-40ed-9ecd-42f387f59c22",
            AppMetadataKey.ORIGINAL_DATE: "2020-01-01",
            AppMetadataKey.REMIXER: "Test Remixer",
            AppMetadataKey.CONDUCTOR: "Test Conductor"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.COVER_ART) == b"test_cover_art_data"
        assert metadata.get(AppMetadataKey.COMPILATION) is True
        assert metadata.get(AppMetadataKey.MEDIA_TYPE) == "Digital Media"
        assert metadata.get(AppMetadataKey.FILE_OWNER) == "Test Owner"
        assert metadata.get(AppMetadataKey.RECORDING_DATE) == "2024-01-15"
        assert metadata.get(AppMetadataKey.ENCODER_SETTINGS) == "VBR 0"
        assert metadata.get(AppMetadataKey.REPLAYGAIN) == "Track Gain: -3.2 dB"
        assert metadata.get(AppMetadataKey.MUSICBRAINZ_ID) == "4a45b00b-273d-40ed-9ecd-42f387f59c22"
        assert metadata.get(AppMetadataKey.ORIGINAL_DATE) == "2020-01-01"
        assert metadata.get(AppMetadataKey.REMIXER) == "Test Remixer"
        assert metadata.get(AppMetadataKey.CONDUCTOR) == "Test Conductor"

    def test_advanced_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test advanced metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.COMPILATION: True,
            AppMetadataKey.MEDIA_TYPE: "AudioFile Media",
            AppMetadataKey.CONDUCTOR: "AudioFile Conductor"
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.COMPILATION) is True
        assert metadata.get(AppMetadataKey.MEDIA_TYPE) == "AudioFile Media"
        assert metadata.get(AppMetadataKey.CONDUCTOR) == "AudioFile Conductor"

    def test_empty_advanced_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing advanced metadata."""
        # Test reading from file with no advanced metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific advanced metadata that doesn't exist
        cover_art = get_specific_metadata(sample_mp3_file, AppMetadataKey.COVER_ART)
        assert cover_art is None or isinstance(cover_art, bytes)
        
        compilation = get_specific_metadata(sample_mp3_file, AppMetadataKey.COMPILATION)
        assert compilation is None or isinstance(compilation, bool)
        
        musicbrainz_id = get_specific_metadata(sample_mp3_file, AppMetadataKey.MUSICBRAINZ_ID)
        assert musicbrainz_id is None or isinstance(musicbrainz_id, str)