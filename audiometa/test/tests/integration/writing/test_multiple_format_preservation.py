"""Tests for multiple format preservation when updating metadata.

This module tests that updating fields in one format with the PRESERVE strategy
does not affect other formats. It covers the main working combinations.
"""

import pytest

from audiometa import (
    update_metadata,
    get_unified_metadata,
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMultipleFormatPreservation:
    
    def test_id3v1_preserves_id3v2(self):
        with TempFileWithMetadata({"title": "ID3v2 Title", "artist": "ID3v2 Artist"}, "mp3") as test_file:

            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v1 with PRESERVE strategy (specify ID3v1 format)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v1 Artist"]
            }
            update_metadata(
                test_file.path, 
                id3v1_metadata, 
                metadata_format=MetadataFormat.ID3V1
            )
            
            # Verify ID3v1 was updated and ID3v2 was preserved
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"

    def test_id3v2_preserves_id3v1(self):
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Verify initial state
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) is None
            
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v2 Artist"]
            }
            update_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_format=MetadataFormat.ID3V2
            )
            
            # Verify ID3v2 was updated and ID3v1 was preserved
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_riff_preserves_id3v1(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            
            # Verify initial state
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            riff_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert riff_before.get(UnifiedMetadataKey.TITLE) is None
            
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS: ["RIFF Artist"]
            }
            update_metadata(
                test_file.path, 
                riff_metadata, 
                metadata_format=MetadataFormat.RIFF
            )
            
            # Verify RIFF was updated and ID3v1 was preserved
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            riff_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v1_preserves_riff(self):
        with TempFileWithMetadata({"title": "RIFF Title", "artist": "RIFF Artist"}, "wav") as test_file:
            # Verify initial state
            riff_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v1 with PRESERVE strategy (specify ID3v1 format)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v1 Artist"]
            }
            update_metadata(
                test_file.path, 
                id3v1_metadata, 
                metadata_format=MetadataFormat.ID3V1
            )
            
            # Verify ID3v1 was updated and RIFF was preserved
            riff_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"

    def test_riff_preserves_id3v2(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            riff_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert riff_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update RIFF with PRESERVE strategy (specify RIFF format)
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS: ["RIFF Artist"]
            }
            update_metadata(
                test_file.path, 
                riff_metadata, 
                metadata_format=MetadataFormat.RIFF
            )
            
            # Verify RIFF was updated and ID3v2 was preserved
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            riff_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v2_preserves_riff(self):
        with TempFileWithMetadata({"title": "RIFF Title", "artist": "RIFF Artist"}, "wav") as test_file:
            # Verify initial state
            riff_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v2 with PRESERVE strategy (specify ID3v2 format)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v2 Artist"]
            }
            update_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_format=MetadataFormat.ID3V2
            )
            
            # Verify ID3v2 was updated and RIFF was preserved
            riff_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_vorbis_preserves_id3v2(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            vorbis_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert vorbis_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update Vorbis with PRESERVE strategy (specify Vorbis format)
            vorbis_metadata = {
                UnifiedMetadataKey.TITLE: "Vorbis Title",
                UnifiedMetadataKey.ARTISTS: ["Vorbis Artist"]
            }
            update_metadata(
                test_file.path, 
                vorbis_metadata, 
                metadata_format=MetadataFormat.VORBIS
            )
            
            # Verify Vorbis was updated and ID3v2 was preserved
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            vorbis_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert vorbis_after.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"

    def test_id3v2_preserves_vorbis(self):
        with TempFileWithMetadata({"title": "Vorbis Title", "artist": "Vorbis Artist"}, "flac") as test_file:
            # Verify initial state
            vorbis_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert vorbis_before.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) is None
            
            # Update ID3v2 with PRESERVE strategy (specify ID3v2 format)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v2 Artist"]
            }
            update_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_format=MetadataFormat.ID3V2
            )
            
            # Verify ID3v2 was updated and Vorbis was preserved
            vorbis_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert vorbis_after.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_multiple_fields_preservation(self):
        with TempFileWithMetadata({"title": "Original Title", "artist": "Original Artist"}, "mp3") as test_file:
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Verify initial state
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Update only ID3v2 with multiple fields
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Updated ID3v2 Title",
                UnifiedMetadataKey.ARTISTS: ["Updated ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM: "ID3v2 Album"
            }
            update_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_format=MetadataFormat.ID3V2
            )
            
            # Verify ID3v2 was updated and ID3v1 was preserved
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_after.get(UnifiedMetadataKey.ARTISTS) == ["ID3v1 Artist"]
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Updated ID3v2 Title"
            assert id3v2_after.get(UnifiedMetadataKey.ARTISTS) == ["Updated ID3v2 Artist"]
            assert id3v2_after.get(UnifiedMetadataKey.ALBUM) == "ID3v2 Album"

    def test_preserve_strategy_with_none_values(self):
        with TempFileWithMetadata({"title": "Original Title", "artist": "Original Artist"}, "mp3") as test_file:
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            
            # Verify initial state
            id3v1_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Update ID3v2 with None values (should not affect ID3v1)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: None,  # This should not affect ID3v1
                UnifiedMetadataKey.ARTISTS: ["ID3v2 Artist"]
            }
            update_metadata(
                test_file.path, 
                id3v2_metadata, 
                metadata_format=MetadataFormat.ID3V2
            )
            
            # Verify ID3v1 was preserved
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_after.get(UnifiedMetadataKey.ARTISTS) == ["ID3v1 Artist"]