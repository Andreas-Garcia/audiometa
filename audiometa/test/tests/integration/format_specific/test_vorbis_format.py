"""Tests for Vorbis format-specific metadata scenarios."""

import pytest

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    update_file_metadata,
    AudioFile
)
import shutil
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestVorbisFormat:
    """Test cases for Vorbis format-specific scenarios."""

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

    def test_vorbis_metadata_reading(self, metadata_vorbis_small_flac):
        """Test reading Vorbis metadata from FLAC files."""
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Vorbis can have very long titles
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_vorbis_extraction(self, metadata_vorbis_small_flac):
        """Test extracting Vorbis metadata specifically."""
        vorbis_metadata = get_single_format_app_metadata(metadata_vorbis_small_flac, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        assert UnifiedMetadataKey.TITLE in vorbis_metadata

    def test_metadata_none_files(self, metadata_none_flac):
        """Test reading metadata from files with no metadata."""
        # FLAC with no metadata
        metadata = get_merged_unified_metadata(metadata_none_flac)
        assert isinstance(metadata, dict)

    def test_audio_file_object_reading(self, metadata_vorbis_small_flac):
        """Test reading metadata using AudioFile object."""
        audio_file = AudioFile(metadata_vorbis_small_flac)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_writing_flac(self, metadata_none_flac, temp_audio_file):
        """Test writing metadata to FLAC with Vorbis."""
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

    def test_flac_md5_validation(self, sample_flac_file):
        """Test FLAC MD5 validation."""
        audio_file = AudioFile(sample_flac_file)
        
        # This should not raise an exception
        is_valid = audio_file.is_flac_file_md5_valid()
        assert isinstance(is_valid, bool)

    def test_flac_md5_validation_non_flac(self, sample_mp3_file):
        """Test FLAC MD5 validation on non-FLAC file raises error."""
        audio_file = AudioFile(sample_mp3_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            audio_file.is_flac_file_md5_valid()
