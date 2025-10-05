"""Tests for ID3v1 format-specific metadata scenarios."""

import pytest

from audiometa import (
    get_merged_app_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataSingleFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestId3v1Format:
    """Test cases for ID3v1 format-specific scenarios."""

    def test_id3v1_limitations(self, metadata_id3v1_small_mp3, metadata_id3v1_big_mp3):
        """Test ID3v1 format limitations."""
        # Small ID3v1 file
        metadata = get_merged_app_metadata(metadata_id3v1_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit
        
        # Big ID3v1 file (should still be limited)
        metadata = get_merged_app_metadata(metadata_id3v1_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit

    def test_id3v1_metadata_reading(self, metadata_id3v1_small_mp3, metadata_id3v1_small_flac, metadata_id3v1_small_wav):
        """Test reading ID3v1 metadata from various formats."""
        # MP3 with ID3v1
        metadata = get_merged_app_metadata(metadata_id3v1_small_mp3)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30  # ID3v1 title limit
        
        # FLAC with ID3v1
        metadata = get_merged_app_metadata(metadata_id3v1_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # WAV with ID3v1
        metadata = get_merged_app_metadata(metadata_id3v1_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_none_files(self, metadata_none_mp3):
        """Test reading metadata from files with no metadata."""
        # MP3 with no metadata
        metadata = get_merged_app_metadata(metadata_none_mp3)
        assert isinstance(metadata, dict)
        # Should have minimal or no metadata
        assert not metadata.get(UnifiedMetadataKey.TITLE) or metadata.get(UnifiedMetadataKey.TITLE) == ""

    def test_audio_file_object_reading(self, metadata_id3v1_small_mp3):
        """Test reading metadata using AudioFile object."""
        audio_file = AudioFile(metadata_id3v1_small_mp3)
        
        # Test merged metadata
        metadata = get_merged_app_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # Test specific metadata
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
