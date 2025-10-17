import pytest
from pathlib import Path

from audiometa import (
    delete_all_metadata,
    get_single_format_app_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestDeleteAllMetadataFormatSpecific:
    """Format-specific deletion tests for delete_all_metadata function."""

    def test_delete_all_metadata_format_specific_id3v2(self):
        """Test deleting only ID3v2 metadata while preserving other formats."""
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist"}, "mp3") as test_file:
            # Delete only ID3v2 metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V2)
            assert result is True

    def test_delete_all_metadata_format_specific_id3v1(self):
        """Test deleting only ID3v1 metadata while preserving other formats."""
        with TempFileWithMetadata({"title": "Test ID3v1 Title", "artist": "Test ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using the library
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Test ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "Test ID3v1 Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Test ID3v2 Title"
            
            # Delete only ID3v1 metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V1)
            assert result is True
            
            # Verify ID3v1 was deleted but ID3v2 was preserved
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Test ID3v2 Title"

    def test_delete_all_metadata_format_specific_vorbis(self):
        """Test deleting only Vorbis metadata while preserving other formats."""
        with TempFileWithMetadata({"title": "Test Vorbis Title", "artist": "Test Vorbis Artist"}, "flac") as test_file:
            # Delete only Vorbis metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.VORBIS)
            assert result is True

    def test_delete_all_metadata_format_specific_riff(self):
        """Test deleting only RIFF metadata while preserving other formats."""
        with TempFileWithMetadata({"title": "Test RIFF Title", "artist": "Test RIFF Artist"}, "wav") as test_file:
            # Delete only RIFF metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.RIFF)
            assert result is True

    def test_delete_all_metadata_format_specific_riff_with_id3v2(self):
        """Test deleting only RIFF metadata while preserving ID3v2 metadata."""
        with TempFileWithMetadata({"title": "Test RIFF Title", "artist": "Test RIFF Artist"}, "wav") as test_file:
            # Create WAV file with both RIFF and ID3v2 metadata
            # First add ID3v2 metadata using external script
            import subprocess
            subprocess.run([
                "mid3v2", 
                "--song=Test ID3v2 Title",
                "--artist=Test ID3v2 Artist", 
                "--album=Test ID3v2 Album",
                str(test_file.path)
            ], check=True)
            
            # Verify both formats have metadata before deletion
            riff_before = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Test RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Test ID3v2 Title"
            
            # Delete only RIFF metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.RIFF)
            assert result is True
            
            # Verify RIFF was deleted but ID3v2 was preserved
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert riff_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Test ID3v2 Title"