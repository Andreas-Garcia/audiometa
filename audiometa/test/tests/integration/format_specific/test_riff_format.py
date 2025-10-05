"""Tests for RIFF format-specific metadata scenarios."""

import pytest

from audiometa import (
    get_merged_app_metadata,
    get_single_format_app_metadata,
    update_file_metadata,
    AudioFile
)
import shutil
from audiometa.utils.MetadataSingleFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestRiffFormat:
    """Test cases for RIFF format-specific scenarios."""

    def test_riff_metadata_capabilities(self, metadata_riff_small_wav, metadata_riff_big_wav):
        """Test RIFF metadata capabilities."""
        # Small RIFF file
        metadata = get_merged_app_metadata(metadata_riff_small_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles
        
        # Big RIFF file
        metadata = get_merged_app_metadata(metadata_riff_big_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles

    def test_riff_metadata_reading(self, metadata_riff_small_wav):
        """Test reading RIFF metadata from WAV files."""
        metadata = get_merged_app_metadata(metadata_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # RIFF can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_riff_extraction(self, metadata_riff_small_wav):
        """Test extracting RIFF metadata specifically."""
        riff_metadata = get_single_format_app_metadata(metadata_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        assert UnifiedMetadataKey.TITLE in riff_metadata

    def test_metadata_none_files(self, metadata_none_wav):
        """Test reading metadata from files with no metadata."""
        # WAV with no metadata
        metadata = get_merged_app_metadata(metadata_none_wav)
        assert isinstance(metadata, dict)

    def test_audio_file_object_reading(self, metadata_riff_small_wav):
        """Test reading metadata using AudioFile object."""
        audio_file = AudioFile(metadata_riff_small_wav)
        
        # Test merged metadata
        metadata = get_merged_app_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_writing_wav(self, metadata_none_wav, temp_audio_file):
        """Test writing metadata to WAV with RIFF."""
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title WAV",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist WAV"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album WAV",
            UnifiedMetadataKey.GENRE: "Test Genre WAV",
            UnifiedMetadataKey.RATING: 9
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title WAV"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist WAV"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album WAV"
        assert metadata.get(UnifiedMetadataKey.GENRE) == "Test Genre WAV"
        assert metadata.get(UnifiedMetadataKey.RATING) == 9
