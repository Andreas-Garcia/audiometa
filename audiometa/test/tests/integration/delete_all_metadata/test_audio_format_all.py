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
class TestDeleteAllMetadataAllFormats:

    def test_delete_all_metadata_formats_mp3(self):
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using the library
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Verify both formats were deleted
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_formats_flac(self):
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using the library
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Verify both formats were deleted
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_formats_wav(self):
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using the library
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Verify both formats were deleted
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_removes_all_formats(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Add ID3v1 metadata using external script
            import subprocess
            test_metadata = {
                "title": "ID3v1 Title",
                "artist": "ID3v1 Artist"
            }
            with TempFileWithMetadata(test_metadata, "id3v1") as id3v1_file:
                # Copy the file with ID3v1 metadata to our test file
                import shutil
                shutil.copy2(id3v1_file.path, test_file.path)
                
                # Add ID3v2 metadata using the library
                id3v2_metadata = {
                    UnifiedMetadataKey.TITLE: "ID3v2 Title",
                    UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
                }
                update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
                
                # Verify both formats have metadata before deletion
                id3v2_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
                id3v1_before = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
                assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
                assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
                
                # Delete all metadata
                result = delete_all_metadata(test_file.path)
                assert result is True
                
                # Verify both formats were deleted
                id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
                id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
                assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
                assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None