import pytest

from audiometa import delete_all_metadata, update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMP3MixedFormatsDeletion:
    """Test deletion of all metadata from MP3 files with multiple metadata formats."""

    def test_delete_all_metadata_mp3_with_id3v1_and_id3v2(self):
        """Test that delete_all_metadata removes both ID3v1 and ID3v2 metadata from MP3 files."""
        # Create MP3 file with ID3v1 metadata first
        id3v1_metadata = {
            "title": "ID3v1 Title",
            "artist": "ID3v1 Artist",
            "album": "ID3v1 Album",
            "year": "2023",
            "genre": "Rock"
        }
        
        with TempFileWithMetadata(id3v1_metadata, "mp3") as test_file:
            # Add ID3v2 metadata to the same file
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album",
                UnifiedMetadataKey.RELEASE_DATE: "2024"
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"MP3 headers before deletion: {before_headers}")
            assert before_headers['id3v1'], "ID3v1 metadata should be present"
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both ID3v1 and ID3v2 were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"MP3 headers after deletion: {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            assert not after_headers['id3v1'], "ID3v1 metadata should be removed"

    def test_delete_all_metadata_mp3_with_id3v2_first_then_id3v1(self):
        """Test deletion when ID3v2 is added first, then ID3v1."""
        # Create MP3 file with ID3v2 metadata first
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Add ID3v2 metadata first
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Add ID3v1 metadata programmatically
            id3v1_metadata = {
                "title": "ID3v1 Title",
                "artist": "ID3v1 Artist",
                "album": "ID3v1 Album",
                "year": "2023",
                "genre": "Rock"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Verify both formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"MP3 headers before deletion (ID3v2 first): {before_headers}")
            assert before_headers['id3v1'], "ID3v1 metadata should be present"
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both ID3v1 and ID3v2 were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"MP3 headers after deletion (ID3v2 first): {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            assert not after_headers['id3v1'], "ID3v1 metadata should be removed"

    def test_delete_all_metadata_mp3_with_all_formats(self):
        """Test deletion when MP3 has ID3v1, ID3v2, and potentially other formats."""
        # Create MP3 file with comprehensive metadata
        comprehensive_metadata = {
            "title": "Comprehensive MP3 Title",
            "artist": "Comprehensive MP3 Artist",
            "album": "Comprehensive MP3 Album",
            "year": "2023",
            "genre": "Test Genre",
            "comment": "Comprehensive MP3 Comment"
        }
        
        with TempFileWithMetadata(comprehensive_metadata, "mp3") as test_file:
            # Add additional ID3v2 metadata
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Additional ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Additional ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Additional ID3v2 Album"
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify multiple formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"MP3 comprehensive headers before deletion: {before_headers}")
            assert before_headers['id3v1'], "ID3v1 metadata should be present"
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both ID3v1 and ID3v2 were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"MP3 comprehensive headers after deletion: {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            assert not after_headers['id3v1'], "ID3v1 metadata should be removed"
