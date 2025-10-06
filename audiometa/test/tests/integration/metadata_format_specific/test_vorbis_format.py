"""Tests for Vorbis format-specific metadata scenarios."""

import pytest
from pathlib import Path

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

    def test_vorbis_metadata_capabilities(self, metadata_vorbis_small_flac, metadata_vorbis_big_flac):
        # Small Vorbis file
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # Vorbis can have longer titles
        
        # Big Vorbis file
        metadata = get_merged_unified_metadata(metadata_vorbis_big_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # Vorbis can have longer titles

    def test_vorbis_metadata_reading(self, metadata_vorbis_small_flac):
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Vorbis can have very long titles
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_vorbis_extraction(self, metadata_vorbis_small_flac):
        vorbis_metadata = get_single_format_app_metadata(metadata_vorbis_small_flac, MetadataFormat.VORBIS)
        assert isinstance(vorbis_metadata, dict)
        assert UnifiedMetadataKey.TITLE in vorbis_metadata

    def test_metadata_none_files(self, metadata_none_flac):
        # FLAC with no metadata
        metadata = get_merged_unified_metadata(metadata_none_flac)
        assert isinstance(metadata, dict)

    def test_audio_file_object_reading(self, metadata_vorbis_small_flac):
        audio_file = AudioFile(metadata_vorbis_small_flac)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_writing_flac(self, metadata_none_flac, temp_audio_file):
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title FLAC",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist FLAC"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album FLAC",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre FLAC",
            UnifiedMetadataKey.RATING: 10
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title FLAC"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist FLAC"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album FLAC"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre FLAC"
        assert metadata.get(UnifiedMetadataKey.RATING) == 1

    def test_flac_md5_validation(self, sample_flac_file):
        audio_file = AudioFile(sample_flac_file)
        
        # This should not raise an exception
        is_valid = audio_file.is_flac_file_md5_valid()
        assert isinstance(is_valid, bool)

    def test_multiple_metadata_reading(self, sample_flac_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata commonly supported across formats
            UnifiedMetadataKey.TITLE: "Test Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre",
            UnifiedMetadataKey.RATING: 8
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre"
        assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_multiple_metadata_writing(self, sample_flac_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata commonly supported across formats
            UnifiedMetadataKey.TITLE: "Written Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Written Album",
            UnifiedMetadataKey.GENRE_NAME: "Written Genre",
            UnifiedMetadataKey.RATING: 9
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields were written
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Written Genre"
        assert metadata.get(UnifiedMetadataKey.RATING) == 0

    def test_flac_md5_validation_non_flac(self, sample_mp3_file):
        audio_file = AudioFile(sample_mp3_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            audio_file.is_flac_file_md5_valid()
