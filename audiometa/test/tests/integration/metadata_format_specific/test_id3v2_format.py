"""Tests for ID3v2 format-specific metadata scenarios."""

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
class TestId3v2Format:
    """Test cases for ID3v2 format-specific scenarios."""

    def test_id3v2_extended_metadata(self, metadata_id3v2_small_mp3, metadata_id3v2_big_mp3):
        # Small ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles
        
        # Big ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles

    def test_id3v2_metadata_reading_mp3(self, metadata_id3v2_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_id3v2_metadata_reading_flac(self, metadata_id3v2_small_flac):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_id3v2_metadata_reading_wav(self, metadata_id3v2_small_wav):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_single_format_id3v2_extraction(self, metadata_id3v2_small_mp3):
        id3v2_metadata = get_single_format_app_metadata(metadata_id3v2_small_mp3, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        assert UnifiedMetadataKey.TITLE in id3v2_metadata

    def test_audio_file_object_reading(self, metadata_id3v2_small_mp3):
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

    def test_wav_with_id3v2_and_riff_metadata(self, metadata_id3v2_and_riff_small_wav):
        # Test that we can read metadata from a WAV file with both ID3v2 and RIFF metadata
        metadata = get_merged_unified_metadata(metadata_id3v2_and_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30
        
        # Test that the file can be processed without errors
        # This verifies that our fix for handling ID3v2 metadata in WAV files works correctly
        audio_file = AudioFile(metadata_id3v2_and_riff_small_wav)
        metadata_from_audio_file = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata_from_audio_file, dict)
        assert UnifiedMetadataKey.TITLE in metadata_from_audio_file

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

    def test_id3v2_error_handling(self, temp_audio_file: Path):
        # Test ID3v2 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)

    def test_none_field_removal_id3v2(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test that setting fields to None removes them from MP3 ID3v2 metadata."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First, set some metadata (without rating to avoid configuration issues)
        initial_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.BPM: 120
        }
        update_file_metadata(temp_audio_file, initial_metadata)
        
        # Verify metadata was written
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        assert metadata.get(UnifiedMetadataKey.BPM) == 120
        
        # Now set some fields to None
        none_metadata = {
            UnifiedMetadataKey.TITLE: None,
            UnifiedMetadataKey.BPM: None
        }
        update_file_metadata(temp_audio_file, none_metadata)
        
        # Verify fields were removed (return None because they don't exist)
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
        assert updated_metadata.get(UnifiedMetadataKey.BPM) is None
        
        # Verify other fields are still present
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        
        # Verify at ID3v2 level that frames were actually deleted
        id3v2_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) is None
        assert id3v2_metadata.get(UnifiedMetadataKey.BPM) is None

    def test_none_vs_empty_string_behavior_id3v2(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test the difference between None and empty string behavior for MP3 ID3v2.
        Note: mutagen automatically removes empty frames, so empty strings behave like None."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Set a field to empty string - mutagen removes empty frames, so field is removed
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: ""})
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title is None  # Empty string removes field (mutagen removes empty frames)
        
        # Set the same field to None - should remove field
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: None})
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title is None  # None removes field
        
        # Set it back to empty string - should remove field again
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: ""})
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title is None  # Empty string removes field (mutagen removes empty frames)
