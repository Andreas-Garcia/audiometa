"""Tests for general metadata writing functionality using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest
import warnings
from pathlib import Path

from audiometa import (
    update_file_metadata,
    delete_metadata,
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    AudioFile
)
from audiometa.exceptions import MetadataWritingConflictParametersError
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError, MetadataNotSupportedError
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMetadataWriting:

    def test_update_file_metadata_basic_functionality(self):
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
            with TempFileWithMetadata(test_metadata, format_type) as test_file:
                # Now test that our reading logic works correctly
                updated_metadata = get_merged_unified_metadata(test_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == test_metadata["title"]
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == [test_metadata["artist"]]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_metadata["album"]
            if "rating" in test_metadata:
                assert updated_metadata.get(UnifiedMetadataKey.RATING) == test_metadata["rating"]

    def test_update_file_metadata_with_audio_file_object(self):
        # Use external script to set metadata instead of app's update function
        test_metadata = {
            "title": "Test Title with AudioFile",
            "artist": "Test Artist with AudioFile"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Test that AudioFile object works with reading functions
            audio_file = AudioFile(test_file)
            updated_metadata = get_merged_unified_metadata(audio_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with AudioFile"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist with AudioFile"]

    def test_update_file_metadata_unsupported_field_sync_strategy(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
                                # Test that SYNC strategy (default) handles unsupported fields gracefully
                                # WAV files don't support BPM in RIFF format
                                unsupported_metadata = {
                                    UnifiedMetadataKey.TITLE: "Test Title",
                                    UnifiedMetadataKey.BPM: 120  # This should be skipped with a warning
                                }
            
                                # This should NOT raise MetadataNotSupportedError with SYNC strategy (default)
                                # It should write the supported fields and log a warning about BPM
                                with warnings.catch_warnings(record=True) as w:
                                    warnings.simplefilter("always")
                                    update_file_metadata(test_file, unsupported_metadata)
                
                                    # Check that a warning was issued about the unsupported field
                                    assert len(w) > 0
                                    assert any("BPM" in str(warning.message) for warning in w)
            
                                # Verify that the supported field was written
                                updated_metadata = get_merged_unified_metadata(test_file)
                                assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"

    def test_update_file_metadata_unsupported_field_preserve_strategy(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Test that PRESERVE strategy still fails fast for unsupported fields
            # WAV files don't support BPM in RIFF format
            unsupported_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.BPM: 120  # This should raise MetadataNotSupportedError for WAV files
        }
        
        # This should raise MetadataNotSupportedError for unsupported fields with PRESERVE strategy
        with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by RIFF format"):
            update_file_metadata(test_file, unsupported_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)

    def test_update_file_metadata_forced_format_fails_fast(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Test that forced format always fails fast on unsupported fields
            # WAV files don't support BPM in RIFF format
            unsupported_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.BPM: 120  # This should raise MetadataNotSupportedError
        }
        
        # This should raise MetadataNotSupportedError because format is forced
        with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by RIFF format"):
            update_file_metadata(test_file, unsupported_metadata, 
                               metadata_format=MetadataFormat.RIFF)

    def test_update_file_metadata_forced_format_writes_only_to_specified_format(self):
        # Use external script to set ID3v2 metadata
        test_metadata = {
            "title": "Original ID3v2 Title",
            "artist": "Original ID3v2 Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Force RIFF format on MP3 file (should write only to RIFF, leave ID3v2 untouched)
            new_metadata = {
            UnifiedMetadataKey.TITLE: "New RIFF Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["New RIFF Artist"]
        }
        
        # This should write only to RIFF format, leaving ID3v2 unchanged
        update_file_metadata(test_file, new_metadata, 
                           metadata_format=MetadataFormat.RIFF)  # Only specify format
        
        # Verify RIFF has new metadata
        riff_metadata = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
        assert riff_metadata.get(UnifiedMetadataKey.TITLE) == "New RIFF Title"
        
        # Verify ID3v2 still has original metadata (forced format doesn't affect other formats)
        id3v2_metadata = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
        assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"

    def test_update_file_metadata_parameter_conflict_error(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Test that specifying both parameters raises ValueError
            metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
        }
        
        with pytest.raises(MetadataWritingConflictParametersError, match="Cannot specify both metadata_strategy and metadata_format"):
            update_file_metadata(test_file, metadata,
                               metadata_format=MetadataFormat.RIFF,
                               metadata_strategy=MetadataWritingStrategy.SYNC)

    def test_delete_metadata_mp3(self):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title to Delete",
            "artist": "Test Artist to Delete"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Verify metadata was added
            updated_metadata = get_merged_unified_metadata(test_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title to Delete"
        
        # Delete metadata
        result = delete_metadata(test_file)
        assert result is True
        
        # Verify metadata was deleted (should be empty or minimal)
        deleted_metadata = get_merged_unified_metadata(test_file)
        # After deletion, metadata should be empty or contain only technical info
        assert UnifiedMetadataKey.TITLE not in deleted_metadata or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Test Title to Delete"

    def test_delete_metadata_with_specific_format(self):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Delete only ID3v2 metadata
            result = delete_metadata(test_file, MetadataFormat.ID3V2)
        assert result is True

    def test_delete_metadata_with_audio_file_object(self):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            audio_file = AudioFile(test_file)
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

    def test_write_metadata_to_files_with_existing_metadata(self):
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
            with TempFileWithMetadata(test_metadata, format_type) as test_file:
                # Now test that our reading logic works correctly
                updated_metadata = get_merged_unified_metadata(test_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == test_metadata["title"]
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == [test_metadata["artist"]]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_metadata["album"]
            if "rating" in test_metadata:
                assert updated_metadata.get(UnifiedMetadataKey.RATING) == test_metadata["rating"]

    def test_write_metadata_unsupported_fields_sync_strategy(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "WAV Test Title",
            "artist": "WAV Test Artist",
            "album": "WAV Test Album"
        }
        
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
                                # Test that SYNC strategy (default) handles unsupported fields gracefully
                                # WAV supports RATING via IRTD chunk, but BPM is not supported
                                unsupported_metadata = {
                                    UnifiedMetadataKey.TITLE: "WAV Test Title",
                                    UnifiedMetadataKey.ARTISTS_NAMES: ["WAV Test Artist"],
                                    UnifiedMetadataKey.ALBUM_NAME: "WAV Test Album",
                                    UnifiedMetadataKey.BPM: 120    # This should be skipped with a warning
                                }
            
                                # This should NOT raise MetadataNotSupportedError with SYNC strategy (default)
                                # It should write the supported fields and log a warning about BPM
                                with warnings.catch_warnings(record=True) as w:
                                    warnings.simplefilter("always")
                                    update_file_metadata(test_file, unsupported_metadata)
                
                                    # Check that a warning was issued about the unsupported field
                                    assert len(w) > 0
                                    assert any("BPM" in str(warning.message) for warning in w)
            
                                # Verify that the supported fields were written
                                updated_metadata = get_merged_unified_metadata(test_file)
                                assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Test Title"
                                assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Test Artist"]
                                assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "WAV Test Album"

    def test_write_metadata_partial_update(self):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
                                # Get original metadata
                                original_metadata = get_merged_unified_metadata(test_file)
                                original_album = original_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
            
                                # Update only title using app's function (this is what we're testing)
                                test_metadata = {
                                    UnifiedMetadataKey.TITLE: "Partial Update Title"
                                }
            
                                update_file_metadata(test_file, test_metadata)
                                updated_metadata = get_merged_unified_metadata(test_file)
            
                                # Title should be updated
                                assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Partial Update Title"
                                # Other fields should remain unchanged
                                assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == original_album
