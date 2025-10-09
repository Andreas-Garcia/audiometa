"""Tests for API consistency across different audio formats.

These tests verify that the audiometa API behaves consistently across
different audio formats and file types.
"""

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestApiConsistency:
    """Test cases for API consistency across formats."""

    def test_cross_audio_format_metadata_consistency(self, sample_mp3_file: Path, sample_flac_file: Path, sample_wav_file: Path):
        """Test that metadata reading is consistent across different formats."""
        files = [sample_mp3_file, sample_flac_file, sample_wav_file]
        
        for file_path in files:
            # All files should return metadata dictionaries
            metadata = get_merged_unified_metadata(file_path)
            assert isinstance(metadata, dict)
            
            # All files should support specific metadata queries
            title = metadata.get(UnifiedMetadataKey.TITLE)
            assert title is None or isinstance(title, str)
            
            # All files should support technical metadata
            artists = metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert artists is None or isinstance(artists, list)

    def test_metadata_manager_integration_mp3(self, sample_mp3_file: Path):
        """Test integration between different metadata managers for MP3."""
        # Test that merged metadata combines multiple sources
        metadata = get_merged_unified_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test single format metadata extraction
        id3v2_metadata = get_single_format_app_metadata(sample_mp3_file, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        
        # Test specific metadata extraction
        title = get_specific_metadata(sample_mp3_file, UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_metadata_manager_integration_flac(self, sample_flac_file: Path):
        """Test integration between different metadata managers for FLAC."""
        # Test that merged metadata combines multiple sources
        metadata = get_merged_unified_metadata(sample_flac_file)
        assert isinstance(metadata, dict)
        
        # Test single format metadata extraction
        vorbis_metadata = get_single_format_app_metadata(sample_flac_file, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        
        # Test specific metadata extraction
        title = get_specific_metadata(sample_flac_file, UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_metadata_manager_integration_wav(self, sample_wav_file: Path):
        """Test integration between different metadata managers for WAV."""
        # Test that merged metadata combines multiple sources
        metadata = get_merged_unified_metadata(sample_wav_file)
        assert isinstance(metadata, dict)
        
        # Test single format metadata extraction
        riff_metadata = get_single_format_app_metadata(sample_wav_file, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        
        # Test specific metadata extraction
        title = get_specific_metadata(sample_wav_file, UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_metadata_consistency_across_formats(self, metadata_id3v2_small_mp3, metadata_id3v2_small_flac, metadata_id3v2_small_wav):
        """Test that metadata reading is consistent across different formats."""
        files = [metadata_id3v2_small_mp3, metadata_id3v2_small_flac, metadata_id3v2_small_wav]
        
        for file_path in files:
            # All files should return metadata dictionaries
            metadata = get_merged_unified_metadata(file_path)
            assert isinstance(metadata, dict)
            
            # All files should support specific metadata queries
            title = metadata.get(UnifiedMetadataKey.TITLE)
            assert title is None or isinstance(title, str)
            
            # All files should support technical metadata
            artists = metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert artists is None or isinstance(artists, list)
