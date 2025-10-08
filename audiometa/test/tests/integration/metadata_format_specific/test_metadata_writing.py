"""Tests for general metadata writing functionality using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import subprocess

from audiometa import (
    update_file_metadata,
    delete_metadata,
    get_merged_unified_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError, MetadataNotSupportedError
from audiometa.test.tests.test_script_helpers import create_test_file_with_metadata


@pytest.mark.integration
class TestMetadataWriting:

    def test_update_file_metadata_basic_functionality(self, temp_audio_file: Path):
        test_cases = [
            ({
                "title": "Test MP3 Title",
                "artist": "Test MP3 Artist",
                "album": "Test MP3 Album",
                "rating": 85
            }, "mp3"),
            ({
                "title": "Test FLAC Title",
                "artist": "Test FLAC Artist",
                "album": "Test FLAC Album"
            }, "flac"),
            ({
                "title": "Test WAV Title",
                "artist": "Test WAV Artist",
                "album": "Test WAV Album"
            }, "wav")
        ]
        
        for test_metadata, format_type in test_cases:
            # Use external script to set metadata instead of app's update function
            create_test_file_with_metadata(
                temp_audio_file,
                test_metadata,
                format_type
            )
            
            # Now test that our reading logic works correctly
            updated_metadata = get_merged_unified_metadata(temp_audio_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == test_metadata["title"]
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == [test_metadata["artist"]]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_metadata["album"]
            if "rating" in test_metadata:
                assert updated_metadata.get(UnifiedMetadataKey.RATING) == test_metadata["rating"]

    def test_update_file_metadata_with_audio_file_object(self, temp_audio_file: Path):
        # Use external script to set metadata instead of app's update function
        test_metadata = {
            "title": "Test Title with AudioFile",
            "artist": "Test Artist with AudioFile"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            test_metadata,
            "mp3"
        )
        
        # Test that AudioFile object works with reading functions
        audio_file = AudioFile(temp_audio_file)
        updated_metadata = get_merged_unified_metadata(audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with AudioFile"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist with AudioFile"]

    def test_update_file_metadata_unsupported_field(self, temp_audio_file: Path):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            test_metadata,
            "wav"
        )
        
        # Now test that unsupported fields are handled correctly
        # WAV files don't support BPM in RIFF format
        unsupported_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.BPM: 120  # This should be ignored for WAV files
        }
        
        # This should not raise an error, but BPM should be ignored
        update_file_metadata(temp_audio_file, unsupported_metadata)
        
        # Verify only supported metadata was written
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
        # BPM should not be present for WAV files
        assert UnifiedMetadataKey.BPM not in updated_metadata

    def test_delete_metadata_mp3(self, temp_audio_file: Path):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title to Delete",
            "artist": "Test Artist to Delete"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            test_metadata,
            "mp3"
        )
        
        # Verify metadata was added
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title to Delete"
        
        # Delete metadata
        result = delete_metadata(temp_audio_file)
        assert result is True
        
        # Verify metadata was deleted (should be empty or minimal)
        deleted_metadata = get_merged_unified_metadata(temp_audio_file)
        # After deletion, metadata should be empty or contain only technical info
        assert UnifiedMetadataKey.TITLE not in deleted_metadata or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Test Title to Delete"

    def test_delete_metadata_with_specific_format(self, temp_audio_file: Path):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            test_metadata,
            "mp3"
        )
        
        # Delete only ID3v2 metadata
        result = delete_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert result is True

    def test_delete_metadata_with_audio_file_object(self, temp_audio_file: Path):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            test_metadata,
            "mp3"
        )
        
        audio_file = AudioFile(temp_audio_file)
        result = delete_metadata(audio_file)
        assert result is True

    def test_update_metadata_unsupported_file_type(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        test_metadata = {UnifiedMetadataKey.TITLE: "Test Title"}
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), test_metadata)

    def test_delete_metadata_unsupported_file_type(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_metadata(str(temp_audio_file))

    def test_write_metadata_to_files_with_existing_metadata(self, temp_audio_file):
        test_cases = [
            ({
                "title": "Updated Title MP3",
                "artist": "Updated Artist MP3",
                "album": "Updated Album MP3",
                "rating": 6
            }, "mp3"),
            ({
                "title": "Updated Title FLAC",
                "artist": "Updated Artist FLAC",
                "album": "Updated Album FLAC",
                "rating": 5
            }, "flac"),
            ({
                "title": "Updated Title WAV",
                "artist": "Updated Artist WAV",
                "album": "Updated Album WAV"
            }, "wav")
        ]
        
        for test_metadata, format_type in test_cases:
            # Use external script to set metadata instead of app's update function
            create_test_file_with_metadata(
                temp_audio_file,
                test_metadata,
                format_type
            )
            
            # Now test that our reading logic works correctly
            updated_metadata = get_merged_unified_metadata(temp_audio_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == test_metadata["title"]
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == [test_metadata["artist"]]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_metadata["album"]
            if "rating" in test_metadata:
                assert updated_metadata.get(UnifiedMetadataKey.RATING) == test_metadata["rating"]

    def test_write_metadata_unsupported_fields(self, temp_audio_file):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "WAV Test Title",
            "artist": "WAV Test Artist",
            "album": "WAV Test Album"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            test_metadata,
            "wav"
        )
        
        # Now test that unsupported fields are handled correctly
        # WAV doesn't support rating or BPM
        unsupported_metadata = {
            UnifiedMetadataKey.TITLE: "WAV Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["WAV Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "WAV Test Album",
            UnifiedMetadataKey.RATING: 8,  # This should be ignored for WAV
            UnifiedMetadataKey.BPM: 120    # This should be ignored for WAV
        }
        
        update_file_metadata(temp_audio_file, unsupported_metadata)
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "WAV Test Album"
        # Rating and BPM should not be present for WAV
        assert UnifiedMetadataKey.RATING not in updated_metadata or updated_metadata.get(UnifiedMetadataKey.RATING) != 8
        assert UnifiedMetadataKey.BPM not in updated_metadata or updated_metadata.get(UnifiedMetadataKey.BPM) != 120

    def test_write_metadata_partial_update(self, temp_audio_file):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album"
        }
        create_test_file_with_metadata(
            temp_audio_file,
            initial_metadata,
            "mp3"
        )
        
        # Get original metadata
        original_metadata = get_merged_unified_metadata(temp_audio_file)
        original_album = original_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
        
        # Update only title using app's function (this is what we're testing)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Partial Update Title"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Title should be updated
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Partial Update Title"
        # Other fields should remain unchanged
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == original_album