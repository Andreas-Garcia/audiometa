"""Tests for publisher metadata across all metadata formats.

This module tests publisher metadata functionality across ID3v1, ID3v2, RIFF, and Vorbis
metadata formats, ensuring consistent behavior regardless of the underlying format.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    get_specific_metadata,
    get_single_format_app_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestPublisherMetadata:
    """Test cases for publisher metadata across all metadata formats."""

    def test_publisher_id3v1_reading(self, metadata_id3v1_mp3):
        """Test reading publisher metadata from ID3v1 format (ID3v1 is read-only)."""
        # ID3v1 is read-only, so we can only test reading from existing files
        if metadata_id3v1_mp3:
            # Test merged metadata reading
            merged_metadata = get_merged_unified_metadata(metadata_id3v1_mp3)
            # Publisher may or may not be present in ID3v1, but should not cause errors
            publisher = merged_metadata.get(UnifiedMetadataKey.PUBLISHER)
            assert publisher is None or isinstance(publisher, str)
            
            # Test specific metadata extraction
            publisher = get_specific_metadata(metadata_id3v1_mp3, UnifiedMetadataKey.PUBLISHER)
            assert publisher is None or isinstance(publisher, str)
            
            # Test single format extraction
            id3v1_metadata = get_single_format_app_metadata(metadata_id3v1_mp3, MetadataFormat.ID3V1)
            publisher = id3v1_metadata.get(UnifiedMetadataKey.PUBLISHER)
            assert publisher is None or isinstance(publisher, str)

    def test_publisher_id3v2_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test publisher metadata in ID3v2 format for MP3."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "ID3v2 Publisher"}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Test merged metadata
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "ID3v2 Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "ID3v2 Publisher"
        
        # Test single format extraction
        id3v2_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert id3v2_metadata.get(UnifiedMetadataKey.PUBLISHER) == "ID3v2 Publisher"

    def test_publisher_id3v2_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test publisher metadata in ID3v2 format for FLAC."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "ID3v2 FLAC Publisher"}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Test merged metadata
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "ID3v2 FLAC Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "ID3v2 FLAC Publisher"

    def test_publisher_vorbis_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test publisher metadata in Vorbis format for FLAC."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "Vorbis FLAC Publisher"}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        
        # Test merged metadata
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "Vorbis FLAC Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "Vorbis FLAC Publisher"
        
        # Test single format extraction
        vorbis_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.VORBIS)
        assert vorbis_metadata.get(UnifiedMetadataKey.PUBLISHER) == "Vorbis FLAC Publisher"

    def test_publisher_riff_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test publisher metadata in RIFF format for WAV."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "RIFF WAV Publisher"}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        
        # Test merged metadata
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "RIFF WAV Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "RIFF WAV Publisher"
        
        # Test single format extraction
        riff_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.RIFF)
        assert riff_metadata.get(UnifiedMetadataKey.PUBLISHER) == "RIFF WAV Publisher"

    def test_publisher_id3v2_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test publisher metadata in ID3v2 format for WAV."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "ID3v2 WAV Publisher"}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Test merged metadata
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "ID3v2 WAV Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "ID3v2 WAV Publisher"

    def test_publisher_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test publisher metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "AudioFile Publisher"}
        update_file_metadata(audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Test merged metadata
        merged_metadata = get_merged_unified_metadata(audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "AudioFile Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "AudioFile Publisher"

    def test_publisher_cross_format_consistency(self, sample_mp3_file: Path, sample_flac_file: Path, sample_wav_file: Path, temp_audio_file: Path):
        """Test that publisher metadata behaves consistently across audio formats."""
        test_publisher = "Cross Format Publisher"
        test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        
        # Test MP3 with ID3v2
        shutil.copy2(sample_mp3_file, temp_audio_file)
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher
        
        # Test FLAC with Vorbis
        shutil.copy2(sample_flac_file, temp_audio_file)
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher
        
        # Test WAV with ID3v2
        shutil.copy2(sample_wav_file, temp_audio_file)
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == test_publisher

    def test_publisher_metadata_precedence(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test publisher metadata precedence when multiple formats are present."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Since ID3v1 is read-only, test precedence between writable formats
        # Test ID3v2 vs RIFF precedence (ID3v2 should win)
        riff_metadata = {UnifiedMetadataKey.PUBLISHER: "RIFF Publisher"}
        id3v2_metadata = {UnifiedMetadataKey.PUBLISHER: "ID3v2 Publisher"}
        
        update_file_metadata(temp_audio_file, riff_metadata, metadata_format=MetadataFormat.RIFF)
        update_file_metadata(temp_audio_file, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Merged metadata should prefer ID3v2
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.PUBLISHER) == "ID3v2 Publisher"
        
        # Test specific metadata extraction
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "ID3v2 Publisher"

    def test_publisher_metadata_reading_from_existing_files(self, metadata_id3v2_small_mp3, metadata_vorbis_small_flac):
        """Test reading publisher metadata from files with existing metadata."""
        # Test ID3v2 file
        if metadata_id3v2_small_mp3:
            metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
            # Publisher may or may not be present, but should not cause errors
            publisher = metadata.get(UnifiedMetadataKey.PUBLISHER)
            assert publisher is None or isinstance(publisher, str)
        
        # Test Vorbis file
        if metadata_vorbis_small_flac:
            metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
            # Publisher may or may not be present, but should not cause errors
            publisher = metadata.get(UnifiedMetadataKey.PUBLISHER)
            assert publisher is None or isinstance(publisher, str)
