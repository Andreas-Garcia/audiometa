import pytest
from pathlib import Path

from audiometa import delete_all_metadata, update_file_metadata, get_merged_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestComprehensiveMixedFormatsDeletion:
    """Comprehensive tests for deletion of all metadata from files with multiple metadata formats."""

    def test_delete_all_metadata_wav_with_both_id3v2_and_riff(self):
        """Test that delete_all_metadata removes both ID3v2 and RIFF metadata from WAV files."""
        # Create WAV file with RIFF metadata first
        riff_metadata = {
            "title": "RIFF Title",
            "artists_names": ["RIFF Artist"],
            "album": "RIFF Album"
        }
        
        with TempFileWithMetadata(riff_metadata, "wav") as test_file:
            # Add ID3v2 metadata to the same file
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"WAV headers before deletion: {before_headers}")
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            assert before_headers['riff'], "RIFF metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both formats were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"WAV headers after deletion: {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            assert not after_headers['riff'], "RIFF metadata should be removed"

    def test_delete_all_metadata_mp3_with_id3v1_and_id3v2(self):
        """Test that delete_all_metadata removes ID3v2 metadata from MP3 files (ID3v1 is read-only)."""
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
            # ID3v1 may or may not be present depending on TempFileWithMetadata implementation
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify ID3v2 was deleted (ID3v1 is read-only and cannot be removed)
            after_headers = test_file.get_metadata_headers_present()
            print(f"MP3 headers after deletion: {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            # Note: ID3v1 is read-only and may still be present

    def test_delete_all_metadata_flac_with_vorbis_and_id3v2(self):
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

    def test_delete_all_metadata_reverse_order_scenarios(self):
        """Test deletion when metadata is added in different orders."""
        # Test WAV with ID3v2 first, then RIFF
        with TempFileWithMetadata({}, "wav") as test_file:
            # Add ID3v2 metadata first
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Add RIFF metadata second
            riff_metadata = {
                "title": "RIFF Title",
                "artists_names": ["RIFF Artist"]
            }
            update_file_metadata(test_file.path, riff_metadata, metadata_format=MetadataFormat.RIFF)
            
            # Verify both formats have metadata before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"WAV reverse order headers before deletion: {before_headers}")
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            assert before_headers['riff'], "RIFF metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify both formats were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"WAV reverse order headers after deletion: {after_headers}")
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
            assert not after_headers['riff'], "RIFF metadata should be removed"

    def test_delete_all_metadata_comprehensive_scenarios(self):
        """Test deletion with comprehensive metadata across different formats."""
        # Test MP3 with comprehensive metadata
        comprehensive_mp3_metadata = {
            "title": "Comprehensive MP3 Title",
            "artist": "Comprehensive MP3 Artist",
            "album": "Comprehensive MP3 Album",
            "year": "2023",
            "genre": "Test Genre",
            "comment": "Comprehensive MP3 Comment"
        }
        
        with TempFileWithMetadata(comprehensive_mp3_metadata, "mp3") as test_file:
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
            # ID3v1 may or may not be present depending on TempFileWithMetadata implementation
            assert before_headers['id3v2'], "ID3v2 metadata should be present"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify all formats were deleted
            after_headers = test_file.get_metadata_headers_present()
            print(f"MP3 comprehensive headers after deletion: {after_headers}")
            # ID3v1 may not be removable (read-only), but ID3v2 should be removed
            assert not after_headers['id3v2'], "ID3v2 metadata should be removed"
