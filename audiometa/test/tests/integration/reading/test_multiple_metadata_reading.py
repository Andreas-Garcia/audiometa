"""Tests for multiple metadata reading functionality."""

import shutil
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_specific_metadata,
    update_file_metadata
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestMultipleMetadataReading:

    def test_multiple_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata
            UnifiedMetadataKey.TITLE: "Test Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre",
            UnifiedMetadataKey.RATING: 8,
            UnifiedMetadataKey.TRACK_NUMBER: 1,
            UnifiedMetadataKey.YEAR: 2024,
            
            # Advanced metadata
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
        metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre"
        assert metadata.get(UnifiedMetadataKey.RATING) == 8
        assert metadata.get(UnifiedMetadataKey.TRACK_NUMBER) == 1
        assert metadata.get(UnifiedMetadataKey.YEAR) == 2024
        
        # Advanced metadata assertions
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

    def test_empty_advanced_metadata_handling(self, sample_mp3_file: Path):
        # Test reading from file with no advanced metadata
        metadata = get_merged_unified_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific advanced metadata that doesn't exist
        cover_art = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.COVER_ART)
        assert cover_art is None or isinstance(cover_art, bytes)
        
        compilation = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.COMPILATION)
        assert compilation is None or isinstance(compilation, bool)
        
        musicbrainz_id = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.MUSICBRAINZ_ID)
        assert musicbrainz_id is None or isinstance(musicbrainz_id, str)
