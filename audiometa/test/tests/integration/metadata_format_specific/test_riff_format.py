"""Tests for RIFF format-specific metadata scenarios."""

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
class TestRiffFormat:

    def test_riff_metadata_capabilities(self, metadata_riff_small_wav, metadata_riff_big_wav):
        # Small RIFF file
        metadata = get_merged_unified_metadata(metadata_riff_small_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles
        
        # Big RIFF file
        metadata = get_merged_unified_metadata(metadata_riff_big_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles

    def test_riff_metadata_reading(self, metadata_riff_small_wav):
        metadata = get_merged_unified_metadata(metadata_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # RIFF can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_riff_extraction(self, metadata_riff_small_wav):
        riff_metadata = get_single_format_app_metadata(metadata_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        assert UnifiedMetadataKey.TITLE in riff_metadata

    def test_metadata_none_files(self, metadata_none_wav):
        # WAV with no metadata
        metadata = get_merged_unified_metadata(metadata_none_wav)
        assert isinstance(metadata, dict)

    def test_audio_file_object_reading(self, metadata_riff_small_wav):
        audio_file = AudioFile(metadata_riff_small_wav)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_writing_wav(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title WAV",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist WAV"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album WAV",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre WAV"
        }
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title WAV"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist WAV"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album WAV"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre WAV"

    def test_wav_with_id3v2_and_riff_metadata(self, metadata_id3v2_and_riff_small_wav):
        """Test reading metadata from WAV file that contains ID3v2 metadata with RIFF structure.
        
        This test explicitly verifies that the RiffManager can handle WAV files that have
        ID3v2 metadata at the beginning followed by RIFF structure. This is a special case
        where the file format is non-standard but still readable by our RIFF manager.
        The file may not have RIFF metadata (INFO chunk), but the RIFF structure should be
        parseable without errors.
        """
        # Test that we can read metadata from a WAV file with ID3v2 metadata and RIFF structure
        metadata = get_merged_unified_metadata(metadata_id3v2_and_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30
        
        # Test that the RIFF manager can process the file without errors
        # Even if there's no RIFF metadata, the manager should handle the structure gracefully
        riff_metadata = get_single_format_app_metadata(metadata_id3v2_and_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        # The file may not have RIFF metadata, so we just verify it returns a dict without errors
        
        # Test that the file can be processed using AudioFile object
        audio_file = AudioFile(metadata_id3v2_and_riff_small_wav)
        metadata_from_audio_file = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata_from_audio_file, dict)
        assert UnifiedMetadataKey.TITLE in metadata_from_audio_file

    def test_multiple_metadata_reading(self, sample_wav_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata commonly supported across formats
            UnifiedMetadataKey.TITLE: "Test Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre"
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre"

    def test_multiple_metadata_writing(self, sample_wav_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {
            # Basic metadata commonly supported across formats
            UnifiedMetadataKey.TITLE: "Written Song Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Written Album",
            UnifiedMetadataKey.GENRE_NAME: "Written Genre"
        }
        
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify all fields were written
        metadata = get_merged_unified_metadata(temp_audio_file, normalized_rating_max_value=10)
        
        # Basic metadata assertions
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Written Genre"

    def test_riff_error_handling(self, temp_audio_file: Path):
        # Test RIFF with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.RIFF)

    def test_none_field_removal_riff(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that setting fields to None removes them from WAV RIFF metadata."""
        # Copy sample file to temp location with correct extension
        temp_wav_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(sample_wav_file, temp_wav_file)
        
        # First, set some metadata (only supported fields for WAV)
        initial_metadata = {
            UnifiedMetadataKey.TITLE: "Test WAV Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test WAV Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test WAV Album"
        }
        update_file_metadata(temp_wav_file, initial_metadata)
        
        # Verify metadata was written
        metadata = get_merged_unified_metadata(temp_wav_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test WAV Title"
        assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test WAV Artist"]
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test WAV Album"
        
        # Now set some fields to None (RiffManager replaces entire INFO chunk, so we need to include fields we want to keep)
        none_metadata = {
            UnifiedMetadataKey.TITLE: None,
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test WAV Artist"],  # Keep this field
            UnifiedMetadataKey.ALBUM_NAME: "Test WAV Album"  # Keep this field
        }
        update_file_metadata(temp_wav_file, none_metadata)
        
        # Verify fields were removed (return None because they don't exist)
        updated_metadata = get_merged_unified_metadata(temp_wav_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
        
        # Verify other fields are still present
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test WAV Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test WAV Album"
        
        # Verify at RIFF level that fields were actually removed
        riff_metadata = get_single_format_app_metadata(temp_wav_file, MetadataFormat.RIFF)
        assert riff_metadata.get(UnifiedMetadataKey.TITLE) is None

    def test_none_vs_empty_string_behavior_riff(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test the difference between None and empty string behavior for WAV RIFF."""
        # Copy sample file to temp location with correct extension
        temp_wav_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(sample_wav_file, temp_wav_file)
        
        # Set a field to empty string - should remove field (same as None)
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.TITLE: ""})
        title = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.TITLE)
        assert title is None  # Empty string removes field in RIFF
        
        # Set the same field to None - should remove field
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.TITLE: None})
        title = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.TITLE)
        assert title is None  # None removes field
        
        # Set it back to empty string - should remove field again
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.TITLE: ""})
        title = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.TITLE)
        assert title is None  # Empty string removes field in RIFF
