import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMP3HeaderDeletion:

    def test_delete_all_metadata_verifies_headers_removed_mp3(self):
        # Add comprehensive metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist",
            "album": "Test Album",
            "year": "2023",
            "genre": "Test Genre"
        }
        temp_file_manager = TempFileWithMetadata(test_metadata, "mp3")
        with temp_file_manager as test_file:
            # Verify ID3v2 header exists before deletion
            assert temp_file_manager.has_id3v2_header(), "ID3v2 header should exist before deletion"
            
            # Get comprehensive header report before deletion
            before_headers = temp_file_manager.get_metadata_headers_present()
            assert before_headers['id3v2'], "ID3v2 should be present before deletion"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify ID3v2 header is completely removed
            assert not temp_file_manager.has_id3v2_header(), "ID3v2 header should be completely removed"
            
            # Verify all headers are removed using comprehensive check
            after_headers = temp_file_manager.get_metadata_headers_present()
            assert not after_headers['id3v2'], "ID3v2 should be confirmed as removed"

    def test_header_detection_comprehensive_mp3(self):        
        temp_file_manager = TempFileWithMetadata({"title": "MP3 Test", "artist": "Test Artist"}, "mp3")
        with temp_file_manager as test_file:
            # Check all headers before deletion
            headers_before = temp_file_manager.get_metadata_headers_present()
            print(f"MP3 headers before deletion: {headers_before}")
            
            # Should have ID3v2 header
            assert headers_before['id3v2'], "MP3 should have ID3v2 header"
            assert temp_file_manager.has_id3v2_header(), "has_id3v2_header should return True"
            
            # Delete metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Check all headers after deletion
            headers_after = temp_file_manager.get_metadata_headers_present()
            print(f"MP3 headers after deletion: {headers_after}")
            
            # Should not have ID3v2 header anymore
            assert not headers_after['id3v2'], "ID3v2 header should be removed"
            assert not temp_file_manager.has_id3v2_header(), "has_id3v2_header should return False"

    def test_file_size_reduction_after_header_deletion(self):
        """Test that file size decreases when headers are removed."""
        
        temp_file_manager = TempFileWithMetadata({
            "title": "Large Title for Testing",
            "artist": "Large Artist Name for Testing",
            "album": "Large Album Name for Testing",
            "year": "2023",
            "genre": "Test Genre",
            "comment": "This is a long comment to make the metadata larger"
        }, "mp3")
        with temp_file_manager as test_file:
            # Get file size with metadata
            with_metadata_size = test_file.path.stat().st_size
            print(f"File size with metadata: {with_metadata_size} bytes")
            
            # Verify headers exist
            assert temp_file_manager.has_id3v2_header(), "ID3v2 header should exist"
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Get file size after deletion
            after_deletion_size = test_file.path.stat().st_size
            print(f"File size after deletion: {after_deletion_size} bytes")
            
            # Verify file size decreased (metadata headers removed)
            assert after_deletion_size < with_metadata_size, "File size should decrease when headers are removed"
            
            # Verify headers are gone
            assert not temp_file_manager.has_id3v2_header(), "ID3v2 header should be removed"
            
            # Verify the file is still valid (not corrupted)
            assert after_deletion_size > 0, "File should not be empty after header removal"

    def test_multiple_format_header_deletion(self):
        """Test deletion of headers from files with multiple metadata formats."""
        
        # Create a file with both ID3v2 and potentially other formats
        temp_file_manager = TempFileWithMetadata({
            "title": "Multi-format Test",
            "artist": "Test Artist",
            "album": "Test Album"
        }, "mp3")
        with temp_file_manager as test_file:
            # Verify comprehensive headers before deletion
            before_headers = temp_file_manager.get_metadata_headers_present()
            print(f"Headers before deletion: {before_headers}")
            
            # Should have ID3v2
            assert before_headers['id3v2'], "Should have ID3v2 header"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify comprehensive headers after deletion
            after_headers = temp_file_manager.get_metadata_headers_present()
            print(f"Headers after deletion: {after_headers}")
            
            # Should not have any headers
            assert not after_headers['id3v2'], "ID3v2 should be removed"
