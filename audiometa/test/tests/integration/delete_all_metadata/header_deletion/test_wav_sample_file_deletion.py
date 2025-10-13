import pytest
from pathlib import Path

from audiometa import delete_all_metadata, get_merged_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestWAVSampleFileDeletion:
    """Test deletion of all metadata from WAV sample files with both ID3v2 and RIFF metadata."""

    def test_delete_all_metadata_from_sample_file_with_both_formats(self, metadata_id3v2_and_riff_small_wav: Path):
        """Test that delete_all_metadata removes both ID3v2 and RIFF metadata from the sample file."""
        # Create a copy of the sample file to avoid modifying the original
        with TempFileWithMetadata({}, "wav") as temp_file:
            # Copy the sample file content
            with open(metadata_id3v2_and_riff_small_wav, 'rb') as src:
                with open(temp_file.path, 'wb') as dst:
                    dst.write(src.read())
            
            # Verify the file has both formats before deletion
            before_headers = temp_file.get_metadata_headers_present()
            print(f"Sample file headers before deletion: {before_headers}")
            
            # Verify we can read metadata from both formats
            merged_before = get_merged_unified_metadata(temp_file.path)
            print(f"Sample file metadata before deletion: {merged_before}")
            assert merged_before.get(UnifiedMetadataKey.TITLE) is not None, "Should have metadata before deletion"
            
            # Delete all metadata
            result = delete_all_metadata(temp_file)
            assert result is True
            
            # Verify both formats were deleted
            after_headers = temp_file.get_metadata_headers_present()
            print(f"Sample file headers after deletion: {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            assert not after_headers['riff'], "RIFF metadata should be removed"
            
            # Verify no metadata can be read after deletion
            merged_after = get_merged_unified_metadata(temp_file.path)
            print(f"Sample file metadata after deletion: {merged_after}")
            assert merged_after.get(UnifiedMetadataKey.TITLE) is None, "Should have no metadata after deletion"
