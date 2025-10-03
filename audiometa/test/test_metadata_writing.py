"""Tests for metadata writing functionality."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    update_file_metadata,
    delete_metadata,
    get_merged_app_metadata,
    AudioFile
)
from audiometa.utils.TagFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError, MetadataNotSupportedError


class TestMetadataWriting:
    """Test cases for metadata writing functionality."""

    def test_update_file_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata in MP3 file."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Prepare test metadata
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            AppMetadataKey.ALBUM_NAME: "Test Album",
            AppMetadataKey.RATING: 85
        }
        
        # Update metadata
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was written
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test Album"
        assert updated_metadata.get(AppMetadataKey.RATING) == 85

    def test_update_file_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test updating metadata in FLAC file."""
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # Prepare test metadata
        test_metadata = {
            AppMetadataKey.TITLE: "Test FLAC Title",
            AppMetadataKey.ARTISTS_NAMES: ["Test FLAC Artist"],
            AppMetadataKey.ALBUM_NAME: "Test FLAC Album"
        }
        
        # Update metadata
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was written
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test FLAC Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test FLAC Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test FLAC Album"

    def test_update_file_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test updating metadata in WAV file."""
        # Copy sample file to temp location
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # Prepare test metadata
        test_metadata = {
            AppMetadataKey.TITLE: "Test WAV Title",
            AppMetadataKey.ARTISTS_NAMES: ["Test WAV Artist"],
            AppMetadataKey.ALBUM_NAME: "Test WAV Album"
        }
        
        # Update metadata
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was written
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test WAV Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test WAV Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Test WAV Album"

    def test_update_file_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata using AudioFile object."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title with AudioFile",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist with AudioFile"]
        }
        
        # Update metadata
        update_file_metadata(audio_file, test_metadata)
        
        # Verify metadata was written
        updated_metadata = get_merged_app_metadata(audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title with AudioFile"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Test Artist with AudioFile"]

    def test_update_file_metadata_with_rating_normalization(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata with rating normalization."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title with Rating",
            AppMetadataKey.RATING: 75
        }
        
        # Update metadata with normalized rating
        update_file_metadata(temp_audio_file, test_metadata, normalized_rating_max_value=100)
        
        # Verify metadata was written
        updated_metadata = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title with Rating"
        assert updated_metadata.get(AppMetadataKey.RATING) == 75

    def test_update_file_metadata_unsupported_field(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test updating metadata with unsupported field for format."""
        # Copy sample file to temp location
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support BPM in RIFF format
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title",
            AppMetadataKey.BPM: 120  # This should be ignored for WAV files
        }
        
        # This should not raise an error, but BPM should be ignored
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify only supported metadata was written
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title"
        # BPM should not be present for WAV files
        assert AppMetadataKey.BPM not in updated_metadata

    def test_delete_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test deleting metadata from MP3 file."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata
        test_metadata = {
            AppMetadataKey.TITLE: "Test Title to Delete",
            AppMetadataKey.ARTISTS_NAMES: ["Test Artist to Delete"]
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was added
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Test Title to Delete"
        
        # Delete metadata
        result = delete_metadata(temp_audio_file)
        assert result is True
        
        # Verify metadata was deleted (should be empty or minimal)
        deleted_metadata = get_merged_app_metadata(temp_audio_file)
        # After deletion, metadata should be empty or contain only technical info
        assert AppMetadataKey.TITLE not in deleted_metadata or deleted_metadata.get(AppMetadataKey.TITLE) != "Test Title to Delete"

    def test_delete_metadata_with_specific_format(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test deleting metadata with specific format."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Delete only ID3v2 metadata
        result = delete_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert result is True

    def test_delete_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test deleting metadata using AudioFile object."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        result = delete_metadata(audio_file)
        assert result is True

    def test_update_metadata_unsupported_file_type(self, temp_audio_file: Path):
        """Test updating metadata on unsupported file type raises error."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        test_metadata = {AppMetadataKey.TITLE: "Test Title"}
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), test_metadata)

    def test_delete_metadata_unsupported_file_type(self, temp_audio_file: Path):
        """Test deleting metadata from unsupported file type raises error."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_metadata(str(temp_audio_file))



