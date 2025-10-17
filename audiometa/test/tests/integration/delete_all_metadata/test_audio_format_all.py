import pytest

from audiometa import (
    delete_all_metadata,
    get_single_format_app_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestDeleteAllMetadataAllFormats:

    def test_delete_all_metadata_formats_mp3(self):
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using external tools for proper test isolation
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
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
            # Add ID3v2 metadata using external tools for proper test isolation
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
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
            # Add ID3v2 metadata using external tools for proper test isolation
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
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
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using external tools for proper test isolation
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
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