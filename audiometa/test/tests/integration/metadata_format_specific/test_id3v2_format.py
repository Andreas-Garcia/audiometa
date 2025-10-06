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
        # Small ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles
        
        # Big ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles

    def test_id3v2_metadata_reading(self, metadata_id3v2_small_mp3, metadata_id3v2_small_flac, metadata_id3v2_small_wav):
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

    def test_id3v2_error_handling(self, temp_audio_file: Path):
        # Test ID3v2 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)
