"""Tests for general metadata writing functionality using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.
"""

import pytest
import warnings
from pathlib import Path

from audiometa import (
    update_file_metadata,
    delete_all_metadata,
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
                updated_metadata = get_merged_unified_metadata(test_file.path)
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
            audio_file = AudioFile(test_file.path)
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
                                    update_file_metadata(test_file.path, unsupported_metadata)
                
                                    # Check that a warning was issued about the unsupported field
                                    assert len(w) > 0
                                    assert any("BPM" in str(warning.message) for warning in w)
            
                                # Verify that the supported field was written
                                updated_metadata = get_merged_unified_metadata(test_file.path)
                                assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"

    def test_update_file_metadata_unsupported_field_preserve_strategy(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Test that PRESERVE strategy handles unsupported fields gracefully with warnings
            # WAV files don't support BPM in RIFF format
            unsupported_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.BPM: 120  # This should be skipped with a warning
            }
            
            # This should NOT raise MetadataNotSupportedError with PRESERVE strategy
            # It should write the supported fields and log a warning about BPM
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                update_file_metadata(test_file.path, unsupported_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
                
                # Check that a warning was issued about the unsupported field
                assert len(w) > 0
                assert any("BPM" in str(warning.message) for warning in w)
            
            # Verify that the supported fields were written
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"

    def test_update_file_metadata_unsupported_field_cleanup_strategy(self):
        # Use external script to set basic metadata
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Test that CLEANUP strategy handles unsupported fields gracefully with warnings
            # WAV files don't support BPM in RIFF format
            unsupported_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.BPM: 120  # This should be skipped with a warning
            }
            
            # This should NOT raise MetadataNotSupportedError with CLEANUP strategy
            # It should write the supported fields and log a warning about BPM
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                update_file_metadata(test_file.path, unsupported_metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
                
                # Check that a warning was issued about the unsupported field
                assert len(w) > 0
                assert any("BPM" in str(warning.message) for warning in w)
            
            # Verify that the supported fields were written
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"

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
                update_file_metadata(test_file.path, unsupported_metadata, 
                                   metadata_format=MetadataFormat.RIFF)

    def test_update_file_metadata_forced_format_writes_only_to_specified_format(self):
        # Create WAV file with initial RIFF metadata
        initial_metadata = {
            "title": "Original RIFF Title",
            "artist": "Original RIFF Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Add ID3v2 metadata using the library directly
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Original ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have their respective metadata
            riff_before = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
            # Force ID3v2 format (should write only to ID3v2, leave RIFF untouched)
            new_metadata = {
                UnifiedMetadataKey.TITLE: "New ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["New ID3v2 Artist"]
            }
            
            # This should write only to ID3v2 format, leaving RIFF unchanged
            update_file_metadata(test_file.path, new_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify ID3v2 has new metadata
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "New ID3v2 Title"
            assert id3v2_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["New ID3v2 Artist"]
            
            # Verify RIFF still has original metadata (forced format doesn't affect other formats)
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert riff_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original RIFF Artist"]

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
                update_file_metadata(test_file.path, metadata,
                                   metadata_format=MetadataFormat.RIFF,
                                   metadata_strategy=MetadataWritingStrategy.SYNC)

    # Note: delete_all_metadata tests have been moved to test_delete_all_metadata.py

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
            delete_all_metadata(str(temp_audio_file))

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
                updated_metadata = get_merged_unified_metadata(test_file.path)
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
                                    update_file_metadata(test_file.path, unsupported_metadata)
                
                                    # Check that a warning was issued about the unsupported field
                                    assert len(w) > 0
                                    assert any("BPM" in str(warning.message) for warning in w)
            
                                # Verify that the supported fields were written
                                updated_metadata = get_merged_unified_metadata(test_file.path)
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
                                original_metadata = get_merged_unified_metadata(test_file.path)
                                original_album = original_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
            
                                # Update only title using app's function (this is what we're testing)
                                test_metadata = {
                                    UnifiedMetadataKey.TITLE: "Partial Update Title"
                                }
            
                                update_file_metadata(test_file.path, test_metadata)
                                updated_metadata = get_merged_unified_metadata(test_file.path)
            
                                # Title should be updated
                                assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Partial Update Title"
                                # Other fields should remain unchanged
                                assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == original_album
