"""Tests for genre metadata."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestGenreMetadata:
    """Test cases for genre metadata."""

    def test_genre_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test genre metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_genre = "Test Genre"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_genre_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test genre metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_genre = "FLAC Genre"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_genre_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test genre metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_genre = "WAV Genre"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_genre_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test genre metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_genre = "AudioFile Genre"
        test_metadata = {UnifiedMetadataKey.GENRE_NAME: test_genre}
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

    def test_genre_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test genre metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test short genre
        short_genre = "A"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.GENRE_NAME: short_genre})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == short_genre
        
        # Test long genre
        long_genre = "A" * 1000
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.GENRE_NAME: long_genre})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) is not None
        assert len(metadata.get(UnifiedMetadataKey.GENRE_NAME)) > 0
        
        # Test empty genre
        empty_genre = ""
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.GENRE_NAME: empty_genre})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == empty_genre

    def test_genre_code_conversion(self, genre_code_id3v1_abstract_mp3, genre_code_id3v1_unknown_mp3):
        # Abstract genre code
        metadata = get_merged_unified_metadata(genre_code_id3v1_abstract_mp3)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Abstract"
        
        # Unknown genre code
        metadata = get_merged_unified_metadata(genre_code_id3v1_unknown_mp3)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Unknown"

    def test_genre_metadata_reading(self, genre_code_id3v1_abstract_mp3, genre_code_id3v1_unknown_mp3):
        """Test reading genre metadata from different formats."""
        # Abstract genre
        metadata = get_merged_unified_metadata(genre_code_id3v1_abstract_mp3)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Abstract"
        
        # Unknown genre
        metadata = get_merged_unified_metadata(genre_code_id3v1_unknown_mp3)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Unknown"

    def test_genre_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing genre metadata to different formats."""
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_genre = "Test Genre MP3"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.GENRE_NAME: test_genre})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_genre = "Test Genre FLAC"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.GENRE_NAME: test_genre})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_genre = "Test Genre WAV"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.GENRE_NAME: test_genre})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == test_genre

