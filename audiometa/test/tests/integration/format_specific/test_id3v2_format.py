"""Tests for ID3v2 format-specific metadata scenarios."""

import pytest

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata,
    AudioFile
)
import shutil
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestId3v2Format:
    """Test cases for ID3v2 format-specific scenarios."""

    def test_id3v2_extended_metadata(self, metadata_id3v2_small_mp3, metadata_id3v2_big_mp3):
        """Test ID3v2 extended metadata capabilities."""
        # Small ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles
        
        # Big ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles

    def test_id3v2_metadata_reading(self, metadata_id3v2_small_mp3, metadata_id3v2_small_flac, metadata_id3v2_small_wav):
        """Test reading ID3v2 metadata from various formats."""
        # MP3 with ID3v2
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30
        
        # FLAC with ID3v2
        metadata = get_merged_unified_metadata(metadata_id3v2_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # WAV with ID3v2
        metadata = get_merged_unified_metadata(metadata_id3v2_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_single_format_id3v2_extraction(self, metadata_id3v2_small_mp3):
        """Test extracting ID3v2 metadata specifically."""
        id3v2_metadata = get_single_format_app_metadata(metadata_id3v2_small_mp3, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        assert UnifiedMetadataKey.TITLE in id3v2_metadata

    def test_audio_file_object_reading(self, metadata_id3v2_small_mp3):
        """Test reading metadata using AudioFile object."""
        audio_file = AudioFile(metadata_id3v2_small_mp3)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # Test specific metadata
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        
        # Test single format metadata
        id3v2_metadata = get_single_format_app_metadata(audio_file, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)

    def test_metadata_writing_mp3(self, metadata_none_mp3, temp_audio_file):
        """Test writing metadata to MP3 with ID3v2."""
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title MP3",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist MP3"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album MP3",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre MP3",
            UnifiedMetadataKey.RATING: 10
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title MP3"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist MP3"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album MP3"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre MP3"
        assert metadata.get(UnifiedMetadataKey.RATING) == 1
