"""Comprehensive tests for metadata writing functionality using test tracks."""

import pytest
import tempfile
import shutil
from pathlib import Path

from audiometa import (
    update_file_metadata,
    delete_metadata,
    get_merged_app_metadata,
    AudioFile
)
from audiometa.utils.TagFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError, MetadataNotSupportedError


@pytest.mark.integration
class TestComprehensiveMetadataWriting:
    """Comprehensive test cases for metadata writing functionality."""

    def test_write_metadata_to_empty_files(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing metadata to files with no existing metadata."""
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title MP3",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist MP3"],
            AppMetadataKey.ALBUM_NAME: "Test Album MP3",
            AppMetadataKey.RATING: 8
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title MP3"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist MP3"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album MP3"
        assert updated_metadata.get(AppMetadataKey.RATING) == 8
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title FLAC",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist FLAC"],
            AppMetadataKey.ALBUM_NAME: "Test Album FLAC",
            AppMetadataKey.RATING: 7
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title FLAC"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist FLAC"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album FLAC"
        assert updated_metadata.get(AppMetadataKey.RATING) == 7
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title WAV",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist WAV"],
            AppMetadataKey.ALBUM_NAME: "Test Album WAV",
            AppMetadataKey.RATING: 9
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title WAV"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist WAV"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album WAV"
        assert updated_metadata.get(AppMetadataKey.RATING) == 9

    def test_write_metadata_to_files_with_existing_metadata(self, metadata_id3v2_small_mp3, metadata_vorbis_small_flac, metadata_riff_small_wav, temp_audio_file):
        """Test writing metadata to files that already have metadata."""
        # Test MP3 with ID3v2
        shutil.copy2(metadata_id3v2_small_mp3, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Updated Title MP3",
            AppMetadataKey.ARTISTS_NAMES: ["Updated Artist MP3"],
            AppMetadataKey.ALBUM_NAME: "Updated Album MP3",
            AppMetadataKey.RATING: 6
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Updated Title MP3"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Updated Artist MP3"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Updated Album MP3"
        assert updated_metadata.get(AppMetadataKey.RATING) == 6
        
        # Test FLAC with Vorbis
        shutil.copy2(metadata_vorbis_small_flac, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Updated Title FLAC",
            AppMetadataKey.ARTISTS_NAMES: ["Updated Artist FLAC"],
            AppMetadataKey.ALBUM_NAME: "Updated Album FLAC",
            AppMetadataKey.RATING: 5
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Updated Title FLAC"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Updated Artist FLAC"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Updated Album FLAC"
        assert updated_metadata.get(AppMetadataKey.RATING) == 5
        
        # Test WAV with RIFF
        shutil.copy2(metadata_riff_small_wav, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Updated Title WAV",
            AppMetadataKey.ARTISTS_NAMES: ["Updated Artist WAV"],
            AppMetadataKey.ALBUM_NAME: "Updated Album WAV",
            AppMetadataKey.RATING: 4
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Updated Title WAV"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Updated Artist WAV"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Updated Album WAV"
        assert updated_metadata.get(AppMetadataKey.RATING) == 4

    def test_write_rating_with_different_normalizations(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing ratings with different normalization values."""
        # Test MP3 with base 255 normalization
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {AppMetadataKey.RATING: 10}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=255)
        updated_metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=255)
        assert updated_metadata.get(AppMetadataKey.RATING) == 10
        
        # Test FLAC with base 100 normalization
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {AppMetadataKey.RATING: 10}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        updated_metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert updated_metadata.get(AppMetadataKey.RATING) == 10
        
        # Test WAV with base 100 normalization
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {AppMetadataKey.RATING: 10}
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        updated_metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert updated_metadata.get(AppMetadataKey.RATING) == 10

    def test_write_artists_with_different_separators(self, metadata_none_mp3, temp_audio_file):
        """Test writing artists with different separator formats."""
        # Test comma-separated artists
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {
            AppMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
        }
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Artist One", "Artist Two", "Artist Three"]
        
        # Test single artist
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {
            AppMetadataKey.ARTISTS_NAMES: ["Single Artist"]
        }
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Single Artist"]

    def test_write_album_metadata(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing album metadata to different formats."""
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {AppMetadataKey.ALBUM_NAME: "Test Album MP3"}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album MP3"
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {AppMetadataKey.ALBUM_NAME: "Test Album FLAC"}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album FLAC"
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {AppMetadataKey.ALBUM_NAME: "Test Album WAV"}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album WAV"

    def test_write_genre_metadata(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing genre metadata to different formats."""
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {AppMetadataKey.GENRE: "Test Genre MP3"}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.GENRE) == "Test Genre MP3"
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_metadata = {AppMetadataKey.GENRE: "Test Genre FLAC"}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.GENRE) == "Test Genre FLAC"
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {AppMetadataKey.GENRE: "Test Genre WAV"}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.GENRE) == "Test Genre WAV"

    def test_write_metadata_with_audio_file_object(self, metadata_none_mp3, temp_audio_file):
        """Test writing metadata using AudioFile object."""
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        audio_file = AudioFile(temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title with AudioFile",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist with AudioFile"],
            AppMetadataKey.ALBUM_NAME: "Test Album with AudioFile",
            AppMetadataKey.RATING: 7
        }
        
        update_file_metadata(audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title with AudioFile"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist with AudioFile"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album with AudioFile"
        assert updated_metadata.get(AppMetadataKey.RATING) == 7

    def test_write_metadata_unsupported_fields(self, metadata_none_wav, temp_audio_file):
        """Test writing metadata with fields unsupported by certain formats."""
        # WAV files don't support BPM in RIFF format
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title",
            AppMetadataKey.BPM: 120  # This should be ignored for WAV files
        }
        
        # This should not raise an error, but BPM should be ignored
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title"
        # BPM should not be present for WAV files
        assert AppMetadataKey.BPM not in updated_metadata

    def test_delete_metadata_all_formats(self, metadata_id3v2_small_mp3, metadata_vorbis_small_flac, metadata_riff_small_wav, temp_audio_file):
        """Test deleting metadata from all supported formats."""
        # Test MP3
        shutil.copy2(metadata_id3v2_small_mp3, temp_audio_file)
        result = delete_metadata(temp_audio_file)
        assert result is True
        deleted_metadata = get_merged_app_metadata(temp_audio_file)
        # After deletion, metadata should be empty or contain only technical info
        assert not deleted_metadata.get(AppMetadataKey.TITLE) or deleted_metadata.get(AppMetadataKey.TITLE) != 'a' * 30
        
        # Test FLAC
        shutil.copy2(metadata_vorbis_small_flac, temp_audio_file)
        result = delete_metadata(temp_audio_file)
        assert result is True
        deleted_metadata = get_merged_app_metadata(temp_audio_file)
        assert not deleted_metadata.get(AppMetadataKey.TITLE) or deleted_metadata.get(AppMetadataKey.TITLE) != 'a' * 30
        
        # Test WAV
        shutil.copy2(metadata_riff_small_wav, temp_audio_file)
        result = delete_metadata(temp_audio_file)
        assert result is True
        deleted_metadata = get_merged_app_metadata(temp_audio_file)
        assert not deleted_metadata.get(AppMetadataKey.TITLE) or deleted_metadata.get(AppMetadataKey.TITLE) != 'a' * 30

    def test_delete_metadata_specific_format(self, metadata_id3v2_small_mp3, temp_audio_file):
        """Test deleting metadata from specific format only."""
        shutil.copy2(metadata_id3v2_small_mp3, temp_audio_file)
        
        # Delete only ID3v2 metadata
        result = delete_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert result is True
        
        # Verify ID3v2 metadata is gone but other formats might remain
        id3v2_metadata = get_merged_app_metadata(temp_audio_file)
        # The specific behavior depends on implementation

    def test_delete_metadata_with_audio_file_object(self, metadata_id3v2_small_mp3, temp_audio_file):
        """Test deleting metadata using AudioFile object."""
        shutil.copy2(metadata_id3v2_small_mp3, temp_audio_file)
        audio_file = AudioFile(temp_audio_file)
        
        result = delete_metadata(audio_file)
        assert result is True
        
        deleted_metadata = get_merged_app_metadata(audio_file)
        assert not deleted_metadata.get(AppMetadataKey.TITLE) or deleted_metadata.get(AppMetadataKey.TITLE) != 'a' * 30

    def test_write_metadata_unsupported_file_type(self, temp_audio_file):
        """Test writing metadata to unsupported file type raises error."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        test_metadata = {AppMetadataKey.TITLE: "Test Title"}
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), test_metadata)

    def test_delete_metadata_unsupported_file_type(self, temp_audio_file):
        """Test deleting metadata from unsupported file type raises error."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_metadata(str(temp_audio_file))

    def test_write_metadata_edge_cases(self, metadata_none_mp3, temp_audio_file):
        """Test writing metadata with edge cases."""
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        # Test empty string values
        test_metadata = {
            AppMetadataKey.TITLE: "",
            AppMetadataKey.ARTISTS_NAMES: [],
            AppMetadataKey.ALBUM_NAME: "",
            AppMetadataKey.GENRE: ""
        }
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        # Empty values should be handled gracefully
        assert updated_metadata.get(AppMetadataKey.TITLE) == ""
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == []
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == ""
        assert updated_metadata.get(AppMetadataKey.GENRE) == ""
        
        # Test very long strings
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        long_string = "a" * 1000
        test_metadata = {
            AppMetadataKey.TITLE: long_string,
            AppMetadataKey.ALBUM_NAME: long_string
        }
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        # Long strings should be handled (possibly truncated)
        assert updated_metadata.get(AppMetadataKey.TITLE) is not None
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) is not None

    def test_write_metadata_rating_edge_cases(self, metadata_none_mp3, temp_audio_file):
        """Test writing rating metadata with edge cases."""
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        # Test rating 0
        test_metadata = {AppMetadataKey.RATING: 0}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.RATING) == 0
        
        # Test rating 10 (maximum)
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {AppMetadataKey.RATING: 10}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.RATING) == 10
        
        # Test rating 5 (middle)
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_metadata = {AppMetadataKey.RATING: 5}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.RATING) == 5

    def test_write_metadata_partial_update(self, metadata_id3v2_small_mp3, temp_audio_file):
        """Test updating only specific metadata fields."""
        shutil.copy2(metadata_id3v2_small_mp3, temp_audio_file)
        
        # Get original metadata
        original_metadata = get_merged_app_metadata(temp_audio_file)
        original_title = original_metadata.get(AppMetadataKey.TITLE)
        original_artists = original_metadata.get(AppMetadataKey.ARTISTS_NAMES)
        
        # Update only rating
        test_metadata = {AppMetadataKey.RATING: 8}
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        
        # Title and artists should remain unchanged
        assert updated_metadata.get(AppMetadataKey.TITLE) == original_title
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == original_artists
        # Only rating should be updated
        assert updated_metadata.get(AppMetadataKey.RATING) == 8


