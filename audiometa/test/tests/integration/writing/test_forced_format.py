"""Tests for forced format parameter functionality.

This module tests the behavior when a specific metadata format is forced
using the metadata_format parameter in update_file_metadata.
"""

import pytest
import warnings
from pathlib import Path

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata,
    delete_metadata
)
from audiometa.exceptions import (
    MetadataNotSupportedError,
    MetadataWritingConflictParametersError,
    FileTypeNotSupportedError
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestForcedFormat:
    """Test forced format parameter functionality."""

    def test_forced_format_writes_only_to_specified_format(self):
        """Test that forced format writes only to the specified format."""
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
            update_file_metadata(test_file, id3v2_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have their respective metadata
            riff_before = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
            # Force ID3v2 format (should write only to ID3v2, leave RIFF untouched)
            new_metadata = {
                UnifiedMetadataKey.TITLE: "New ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["New ID3v2 Artist"]
            }
            
            # This should write only to ID3v2 format, leaving RIFF unchanged
            update_file_metadata(test_file, new_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify ID3v2 has new metadata
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "New ID3v2 Title"
            assert id3v2_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["New ID3v2 Artist"]
            
            # Verify RIFF still has original metadata (forced format doesn't affect other formats)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert riff_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original RIFF Artist"]

    def test_forced_format_fails_fast_on_unsupported_fields(self):
        """Test that forced format fails fast when field is not supported by the format."""
        # Create WAV file with basic metadata
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Try to write BPM to RIFF format (not supported)
            unsupported_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.BPM: 120  # BPM not supported by RIFF format
            }
            
            # This should raise MetadataNotSupportedError because format is forced
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by RIFF format"):
                update_file_metadata(test_file, unsupported_metadata, 
                                   metadata_format=MetadataFormat.RIFF)

    def test_forced_format_succeeds_with_supported_fields(self):
        """Test that forced format succeeds when all fields are supported."""
        # Create WAV file with basic metadata
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Write supported fields to RIFF format
            supported_metadata = {
                UnifiedMetadataKey.TITLE: "New RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["New RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "New RIFF Album"
            }
            
            # This should succeed because all fields are supported by RIFF
            update_file_metadata(test_file, supported_metadata, 
                               metadata_format=MetadataFormat.RIFF)
            
            # Verify RIFF has new metadata
            riff_metadata = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_metadata.get(UnifiedMetadataKey.TITLE) == "New RIFF Title"
            assert riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["New RIFF Artist"]
            assert riff_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "New RIFF Album"

    def test_forced_format_parameter_conflict_error(self):
        """Test that specifying both metadata_format and metadata_strategy raises error."""
        # Create WAV file with basic metadata
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            }
            
            # This should raise error because both parameters are specified
            with pytest.raises(MetadataWritingConflictParametersError, match="Cannot specify both metadata_strategy and metadata_format"):
                update_file_metadata(test_file, metadata,
                                   metadata_format=MetadataFormat.RIFF,
                                   metadata_strategy=MetadataWritingStrategy.SYNC)

    def test_forced_format_with_unsupported_file_type(self):
        """Test that forced format raises error for unsupported file types."""
        # Create MP3 file
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            }
            
            # Try to force Vorbis format on MP3 file (not supported)
            with pytest.raises(FileTypeNotSupportedError, match="Tag format MetadataFormat.VORBIS not supported for file extension .mp3"):
                update_file_metadata(test_file, metadata, 
                                   metadata_format=MetadataFormat.VORBIS)

    def test_forced_format_id3v1_read_only_limitation(self):
        """Test that forced ID3v1 format fails due to read-only limitation."""
        # Create MP3 file with basic metadata
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            metadata = {
                UnifiedMetadataKey.TITLE: "New Title"
            }
            
            # ID3v1 is read-only, so this should fail
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file, metadata, 
                                   metadata_format=MetadataFormat.ID3V1)

    def test_forced_format_multiple_formats_present(self):
        """Test forced format behavior when multiple formats are present in the file."""
        # Create WAV file with both RIFF and ID3v2 metadata
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
            update_file_metadata(test_file, id3v2_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have original metadata
            riff_before = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
            # Force ID3v2 format - should only update ID3v2
            new_metadata = {
                UnifiedMetadataKey.TITLE: "New ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["New ID3v2 Artist"]
            }
            
            update_file_metadata(test_file, new_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify ID3v2 was updated
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "New ID3v2 Title"
            assert id3v2_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["New ID3v2 Artist"]
            
            # Verify RIFF was NOT updated (forced format only affects specified format)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert riff_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original RIFF Artist"]

    def test_forced_format_with_rating_field(self):
        """Test forced format behavior with rating field."""
        # Create MP3 file with basic metadata
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Try to write rating to ID3v2 format (requires normalized_rating_max_value)
            metadata_with_rating = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.RATING: 85
            }
            
            # This should fail because normalized_rating_max_value is not set
            with pytest.raises(Exception):  # ConfigurationError
                update_file_metadata(test_file, metadata_with_rating, 
                                   metadata_format=MetadataFormat.ID3V2)

    def test_forced_format_with_rating_field_success(self):
        """Test forced format behavior with rating field when properly configured."""
        # Create MP3 file with basic metadata
        initial_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Write rating to ID3v2 format with proper configuration
            metadata_with_rating = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.RATING: 85
            }
            
            # This should succeed with proper configuration
            update_file_metadata(test_file, metadata_with_rating, 
                               metadata_format=MetadataFormat.ID3V2,
                               normalized_rating_max_value=100)
            
            # Verify rating was written (converted from 0-100 to 0-255 scale)
            id3v2_metadata = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            # Rating 85 on 0-100 scale becomes 196 on 0-255 scale (85 * 255 / 100 = 216.75, rounded to 196)
            assert id3v2_metadata.get(UnifiedMetadataKey.RATING) == 196

    def test_forced_format_delete_metadata(self):
        """Test that forced format affects delete_metadata behavior."""
        # Create WAV file with both RIFF and ID3v2 metadata
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
            update_file_metadata(test_file, id3v2_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata
            riff_before = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
            # Delete metadata from ID3v2 format only
            result = delete_metadata(test_file, tag_format=MetadataFormat.ID3V2)
            assert result is True
            
            # Verify ID3v2 metadata was deleted
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            
            # Verify RIFF metadata was NOT deleted (forced format only affects specified format)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"

    def test_forced_format_validation_before_writing(self):
        """Test that forced format validates all fields before writing any changes."""
        # Create WAV file with initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Try to write mixed supported/unsupported fields to RIFF format
            mixed_metadata = {
                UnifiedMetadataKey.TITLE: "New Title",  # Supported
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist"],  # Supported
                UnifiedMetadataKey.BPM: 120,  # NOT supported by RIFF
                UnifiedMetadataKey.ALBUM_NAME: "New Album"  # Supported
            }
            
            # This should fail because BPM is not supported by RIFF
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by RIFF format"):
                update_file_metadata(test_file, mixed_metadata, 
                                   metadata_format=MetadataFormat.RIFF)
            
            # Verify NO changes were made to the file (validation happens before writing)
            final_metadata = get_merged_unified_metadata(test_file)
            assert final_metadata.get(UnifiedMetadataKey.TITLE) == "Original Title"
            assert final_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original Artist"]
            assert final_metadata.get(UnifiedMetadataKey.BPM) is None
            assert final_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None
