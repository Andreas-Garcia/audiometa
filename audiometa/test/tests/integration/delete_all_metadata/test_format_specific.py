import pytest

from audiometa import delete_all_metadata, get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
from audiometa.test.helpers.id3v1 import ID3v1MetadataSetter


@pytest.mark.integration
class TestDeleteAllMetadataFormatSpecific:

    def test_delete_all_metadata_format_specific_id3v2(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "Test ID3v2 Title", "artist": "Test ID3v2 Artist"})

            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V2)
            assert result is True
            
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_after.get(UnifiedMetadataKey.ARTISTS) in [None, []]

    def test_delete_all_metadata_format_specific_id3v1(self):
        with TempFileWithMetadata({"title": "Test ID3v1 Title", "artist": "Test ID3v1 Artist"}, "id3v1") as test_file:
            ID3v1MetadataSetter.set_metadata(test_file.path, {"title": "Test ID3v1 Title", "artist": "Test ID3v1 Artist"})
            
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V1)
            assert result is True
            
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v1_after.get(UnifiedMetadataKey.ARTISTS) in [None, []]

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
            # Add ID3v2 metadata using TempFileWithMetadata methods
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "Test ID3v2 Title", "artist": "Test ID3v2 Artist", "album": "Test ID3v2 Album"})
            
            # Verify both formats have metadata before deletion
            riff_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            id3v2_before = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Test RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Test ID3v2 Title"
            
            # Delete only RIFF metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.RIFF)
            assert result is True
            
            # Verify RIFF was deleted but ID3v2 was preserved
            riff_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert riff_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Test ID3v2 Title"