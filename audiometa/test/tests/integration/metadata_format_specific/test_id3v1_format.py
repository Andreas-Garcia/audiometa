"""Tests for ID3v1 format-specific metadata scenarios."""

import pytest
from pathlib import Path

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
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestId3v1Format:

    def test_id3v1_limitations(self, metadata_id3v1_small_mp3, metadata_id3v1_big_mp3):
        # Small ID3v1 file
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit
        
        # Big ID3v1 file (should still be limited)
        metadata = get_merged_unified_metadata(metadata_id3v1_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit

    def test_id3v1_metadata_reading(self, metadata_id3v1_small_mp3, metadata_id3v1_small_flac, metadata_id3v1_small_wav):
        # MP3 with ID3v1
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30  # ID3v1 title limit
        
        # FLAC with ID3v1
        metadata = get_merged_unified_metadata(metadata_id3v1_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # WAV with ID3v1
        metadata = get_merged_unified_metadata(metadata_id3v1_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_none_files(self, metadata_none_mp3):
        # MP3 with no metadata
        metadata = get_merged_unified_metadata(metadata_none_mp3)
        assert isinstance(metadata, dict)
        # Should have minimal or no metadata
        assert not metadata.get(UnifiedMetadataKey.TITLE) or metadata.get(UnifiedMetadataKey.TITLE) == ""

    def test_audio_file_object_reading(self, metadata_id3v1_small_mp3):
        audio_file = AudioFile(metadata_id3v1_small_mp3)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # Test specific metadata
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)

    def test_multiple_metadata_reading(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
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

    def test_multiple_metadata_writing(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
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

    def test_id3v1_error_handling(self, temp_audio_file: Path):
        # Test ID3v1 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V1)
