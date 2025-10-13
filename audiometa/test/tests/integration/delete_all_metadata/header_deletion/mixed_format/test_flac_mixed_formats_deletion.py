import pytest

from audiometa import delete_all_metadata, update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestFLACMixedFormatsDeletion:
    """Test deletion of all metadata from FLAC files with multiple metadata formats."""

    def test_delete_all_metadata_flac_with_vorbis_and_id3v2(self):
        """Test that delete_all_metadata removes both Vorbis and ID3v2 metadata from FLAC files."""
        # Create FLAC file with Vorbis metadata first
        vorbis_metadata = {
            "title": "Vorbis Title",
            "artist": "Vorbis Artist",
            "album": "Vorbis Album",
            "year": "2023",
            "genre": "Test Genre"
        }
        
        with TempFileWithMetadata(vorbis_metadata, "flac") as test_file:
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
            print(f"FLAC headers before deletion: {before_headers}")
            assert before_headers['vorbis'], "Vorbis metadata should be present"
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both formats were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"FLAC headers after deletion: {after_headers}")
            assert not after_headers['vorbis'], "Vorbis metadata should be removed"
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"

    def test_delete_all_metadata_flac_with_id3v2_first_then_vorbis(self):
        """Test deletion when ID3v2 is added first, then Vorbis."""
        # Create FLAC file with ID3v2 metadata first
        with TempFileWithMetadata({}, "flac") as test_file:
            # Add ID3v2 metadata first
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Add Vorbis metadata second
            vorbis_metadata = {
                "title": "Vorbis Title",
                "artists_names": ["Vorbis Artist"]
            }
            update_file_metadata(test_file.path, vorbis_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify both formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"FLAC headers before deletion (ID3v2 first): {before_headers}")
            assert before_headers['vorbis'], "Vorbis metadata should be present"
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both formats were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"FLAC headers after deletion (ID3v2 first): {after_headers}")
            assert not after_headers['vorbis'], "Vorbis metadata should be removed"
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"

    def test_delete_all_metadata_flac_with_all_formats(self):
        """Test deletion when FLAC has Vorbis, ID3v2, and potentially other formats."""
        # Create FLAC file with comprehensive metadata
        comprehensive_metadata = {
            "title": "Comprehensive FLAC Title",
            "artist": "Comprehensive FLAC Artist",
            "album": "Comprehensive FLAC Album",
            "year": "2023",
            "genre": "Test Genre",
            "comment": "Comprehensive FLAC Comment"
        }
        
        with TempFileWithMetadata(comprehensive_metadata, "flac") as test_file:
            # Add additional ID3v2 metadata
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Additional ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Additional ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Additional ID3v2 Album"
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify multiple formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"FLAC comprehensive headers before deletion: {before_headers}")
            assert before_headers['vorbis'], "Vorbis metadata should be present"
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify all formats were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"FLAC comprehensive headers after deletion: {after_headers}")
            assert not after_headers['vorbis'], "Vorbis metadata should be removed"
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
