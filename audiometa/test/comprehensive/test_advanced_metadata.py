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
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataSingleFormat import MetadataFormat


@pytest.mark.comprehensive
class TestAdvancedMetadata:
    """Test cases for complete advanced metadata workflows."""

    def test_complete_advanced_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all advanced metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.COVER_ART: b"test_cover_art_data",
            UnifiedMetadataKey.COMPILATION: True,
            UnifiedMetadataKey.MEDIA_TYPE: "Digital Media",
            UnifiedMetadataKey.FILE_OWNER: "Test Owner",
            UnifiedMetadataKey.RECORDING_DATE: "2024-01-15",
            UnifiedMetadataKey.ENCODER_SETTINGS: "VBR 0",
            UnifiedMetadataKey.REPLAYGAIN: "Track Gain: -3.2 dB",
            UnifiedMetadataKey.MUSICBRAINZ_ID: "4a45b00b-273d-40ed-9ecd-42f387f59c22",
            UnifiedMetadataKey.ORIGINAL_DATE: "2020-01-01",
            UnifiedMetadataKey.REMIXER: "Test Remixer",
            UnifiedMetadataKey.CONDUCTOR: "Test Conductor"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.COVER_ART) == b"test_cover_art_data"
        assert metadata.get(UnifiedMetadataKey.COMPILATION) is True
        assert metadata.get(UnifiedMetadataKey.MEDIA_TYPE) == "Digital Media"
        assert metadata.get(UnifiedMetadataKey.FILE_OWNER) == "Test Owner"
        assert metadata.get(UnifiedMetadataKey.RECORDING_DATE) == "2024-01-15"
        assert metadata.get(UnifiedMetadataKey.ENCODER_SETTINGS) == "VBR 0"
        assert metadata.get(UnifiedMetadataKey.REPLAYGAIN) == "Track Gain: -3.2 dB"
        assert metadata.get(UnifiedMetadataKey.MUSICBRAINZ_ID) == "4a45b00b-273d-40ed-9ecd-42f387f59c22"
        assert metadata.get(UnifiedMetadataKey.ORIGINAL_DATE) == "2020-01-01"
        assert metadata.get(UnifiedMetadataKey.REMIXER) == "Test Remixer"
        assert metadata.get(UnifiedMetadataKey.CONDUCTOR) == "Test Conductor"

    def test_advanced_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test advanced metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.COMPILATION: True,
            UnifiedMetadataKey.MEDIA_TYPE: "AudioFile Media",
            UnifiedMetadataKey.CONDUCTOR: "AudioFile Conductor"
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(UnifiedMetadataKey.COMPILATION) is True
        assert metadata.get(UnifiedMetadataKey.MEDIA_TYPE) == "AudioFile Media"
        assert metadata.get(UnifiedMetadataKey.CONDUCTOR) == "AudioFile Conductor"

    def test_empty_advanced_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing advanced metadata."""
        # Test reading from file with no advanced metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific advanced metadata that doesn't exist
        cover_art = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.COVER_ART)
        assert cover_art is None or isinstance(cover_art, bytes)
        
        compilation = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.COMPILATION)
        assert compilation is None or isinstance(compilation, bool)
        
        musicbrainz_id = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.MUSICBRAINZ_ID)
        assert musicbrainz_id is None or isinstance(musicbrainz_id, str)