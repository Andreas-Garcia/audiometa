"""Tests for multiple format preservation when updating metadata.

This module tests that updating fields in one format with the PRESERVE strategy
does not affect other formats. It covers the main working combinations.
"""

import pytest
from pathlib import Path

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMultipleFormatPreservation:
    """Test that PRESERVE strategy doesn't affect other formats."""

    def test_id3v1_preserves_id3v2(self):
        """Test that updating ID3v1 preserves ID3v2 metadata."""
        with TempFileWithMetadata({"title": "ID3v2 Title", "artist": "ID3v2 Artist"}, "mp3") as test_file:
            # Set up ID3v2 metadata using external tool
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v1 with PRESERVE strategy (no metadata_format specified)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Artist"]
            }
            update_file_metadata(
                test_file.path, 
                id3v1_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v1 was updated and ID3v2 was preserved
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"

    def test_id3v2_preserves_id3v1(self):
        """Test that updating ID3v2 preserves ID3v1 metadata."""
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Verify initial state
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v2 with PRESERVE strategy (no metadata_format specified)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v2 was updated and ID3v1 was preserved
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_riff_preserves_id3v1(self):
        """Test that updating RIFF preserves ID3v1 metadata."""
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "wav") as test_file:
            # Set up ID3v1 metadata using external tool
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            
            # Verify initial state
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            riff_before = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert riff_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update RIFF with PRESERVE strategy (no metadata_format specified)
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"]
            }
            update_file_metadata(
                test_file.path, 
                riff_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify RIFF was updated and ID3v1 was preserved
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v1_preserves_riff(self):
        """Test that updating ID3v1 preserves RIFF metadata."""
        with TempFileWithMetadata({"title": "RIFF Title", "artist": "RIFF Artist"}, "wav") as test_file:
            # Verify initial state
            riff_before = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v1 with PRESERVE strategy (no metadata_format specified)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Artist"]
            }
            update_file_metadata(
                test_file.path, 
                id3v1_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v1 was updated and RIFF was preserved
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"

    def test_riff_preserves_id3v2(self):
        """Test that updating RIFF preserves ID3v2 metadata."""
        with TempFileWithMetadata({"title": "ID3v2 Title", "artist": "ID3v2 Artist"}, "wav") as test_file:
            # Set up ID3v2 metadata using external tool
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            riff_before = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert riff_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update RIFF with PRESERVE strategy (no metadata_format specified)
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"]
            }
            update_file_metadata(
                test_file.path, 
                riff_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify RIFF was updated and ID3v2 was preserved
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v2_preserves_riff(self):
        """Test that updating ID3v2 preserves RIFF metadata."""
        with TempFileWithMetadata({"title": "RIFF Title", "artist": "RIFF Artist"}, "wav") as test_file:
            # Verify initial state
            riff_before = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v2 with PRESERVE strategy (no metadata_format specified)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v2 was updated and RIFF was preserved
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_vorbis_preserves_id3v2(self):
        """Test that updating Vorbis preserves ID3v2 metadata."""
        with TempFileWithMetadata({"title": "ID3v2 Title", "artist": "ID3v2 Artist"}, "flac") as test_file:
            # Set up ID3v2 metadata using external tool
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            vorbis_before = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert vorbis_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update Vorbis with PRESERVE strategy (no metadata_format specified)
            vorbis_metadata = {
                UnifiedMetadataKey.TITLE: "Vorbis Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Vorbis Artist"]
            }
            update_file_metadata(
                test_file.path, 
                vorbis_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify Vorbis was updated and ID3v2 was preserved
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            vorbis_after = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert vorbis_after.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"

    def test_id3v2_preserves_vorbis(self):
        """Test that updating ID3v2 preserves Vorbis metadata."""
        with TempFileWithMetadata({"title": "Vorbis Title", "artist": "Vorbis Artist"}, "flac") as test_file:
            # Verify initial state
            vorbis_before = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert vorbis_before.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v2 with PRESERVE strategy (no metadata_format specified)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v2 was updated and Vorbis was preserved
            vorbis_after = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert vorbis_after.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_multiple_fields_preservation(self):
        """Test that multiple fields are preserved correctly."""
        with TempFileWithMetadata({"title": "Original Title", "artist": "Original Artist"}, "mp3") as test_file:
            # Set up both ID3v1 and ID3v2 metadata
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Update only ID3v2 with multiple fields
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Updated ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Updated ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            update_file_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v2 was updated and ID3v1 was preserved
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Artist"]
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Updated ID3v2 Title"
            assert id3v2_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Updated ID3v2 Artist"]
            assert id3v2_after.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2 Album"

    def test_preserve_strategy_with_none_values(self):
        with TempFileWithMetadata({"title": "Original Title", "artist": "Original Artist"}, "mp3") as test_file:
            # Set up ID3v1 metadata
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            
            # Verify initial state
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Update ID3v2 with None values (should not affect ID3v1)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: None,  # This should not affect ID3v1
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_strategy=MetadataWritingStrategy.PRESERVE
            )
            
            # Verify ID3v1 was preserved
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Artist"]