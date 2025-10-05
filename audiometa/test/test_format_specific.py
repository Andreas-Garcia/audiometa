"""Tests for format-specific metadata scenarios using test tracks."""

import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_single_format_app_metadata, update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestFormatSpecificScenarios:
    """Test cases for format-specific metadata scenarios."""

    def test_id3v1_limitations(self, metadata_id3v1_small_mp3, metadata_id3v1_big_mp3):
        """Test ID3v1 format limitations."""
        # Small ID3v1 file
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit
        
        # Big ID3v1 file (should still be limited)
        metadata = get_merged_unified_metadata(metadata_id3v1_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit

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

    def test_riff_metadata_capabilities(self, metadata_riff_small_wav, metadata_riff_big_wav):
        """Test RIFF metadata capabilities."""
        # Small RIFF file
        metadata = get_merged_unified_metadata(metadata_riff_small_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles
        
        # Big RIFF file
        metadata = get_merged_unified_metadata(metadata_riff_big_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles

    def test_vorbis_metadata_capabilities(self, metadata_vorbis_small_flac, metadata_vorbis_big_flac):
        """Test Vorbis metadata capabilities."""
        # Small Vorbis file
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # Vorbis can have longer titles
        
        # Big Vorbis file
        metadata = get_merged_unified_metadata(metadata_vorbis_big_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # Vorbis can have longer titles

    def test_single_format_metadata_extraction(self, metadata_id3v2_small_mp3, metadata_vorbis_small_flac, metadata_riff_small_wav):
        """Test extracting metadata from specific formats only."""
        # ID3v2 from MP3
        id3v2_metadata = get_single_format_app_metadata(metadata_id3v2_small_mp3, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        assert UnifiedMetadataKey.TITLE in id3v2_metadata
        
        # Vorbis from FLAC
        vorbis_metadata = get_single_format_app_metadata(metadata_vorbis_small_flac, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        assert UnifiedMetadataKey.TITLE in vorbis_metadata
        
        # RIFF from WAV
        riff_metadata = get_single_format_app_metadata(metadata_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        assert UnifiedMetadataKey.TITLE in riff_metadata

    def test_metadata_writing_format_specific(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing metadata to format-specific scenarios."""
        import shutil
        
        # Test MP3 with ID3v2
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title MP3",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist MP3"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album MP3",
            UnifiedMetadataKey.GENRE: "Test Genre MP3",
            UnifiedMetadataKey.RATING: 8
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=255)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title MP3"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist MP3"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album MP3"
        assert metadata.get(UnifiedMetadataKey.GENRE) == "Test Genre MP3"
        assert metadata.get(UnifiedMetadataKey.RATING) == 8
        
        # Test FLAC with Vorbis
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title FLAC",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist FLAC"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album FLAC",
            UnifiedMetadataKey.GENRE: "Test Genre FLAC",
            UnifiedMetadataKey.RATING: 7
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title FLAC"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist FLAC"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album FLAC"
        assert metadata.get(UnifiedMetadataKey.GENRE) == "Test Genre FLAC"
        assert metadata.get(UnifiedMetadataKey.RATING) == 7
        
        # Test WAV with RIFF
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title WAV",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist WAV"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album WAV",
            UnifiedMetadataKey.GENRE: "Test Genre WAV",
            UnifiedMetadataKey.RATING: 9
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title WAV"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist WAV"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album WAV"
        assert metadata.get(UnifiedMetadataKey.GENRE) == "Test Genre WAV"
        assert metadata.get(UnifiedMetadataKey.RATING) == 9

