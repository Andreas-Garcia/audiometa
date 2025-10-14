import pytest
from pathlib import Path

from audiometa import delete_all_metadata, update_file_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.tests.test_version_helpers import TempFileWithId3v2Version
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestComprehensiveID3v2Deletion:

    def test_comprehensive_id3v2_header_deletion_mp3(self):
        # Test both ID3v2.3 and ID3v2.4 versions
        for version in [(2, 3, 0), (2, 4, 0)]:
            with self._create_test_file_with_id3v2_version(version) as test_file:
                # Verify ID3v2 header exists before deletion
                assert test_file.has_id3v2_header(), f"ID3v2.{version[1]} header should exist before deletion"
                
                # Get comprehensive header report before deletion
                before_headers = test_file.get_metadata_headers_present()
                assert before_headers['id3v2'], f"ID3v2.{version[1]} should be present before deletion"
                
                # Delete all metadata
                result = delete_all_metadata(test_file.path)
                assert result is True
                
                # Verify ID3v2 header is completely removed
                assert not test_file.has_id3v2_header(), f"ID3v2.{version[1]} header should be completely removed"
                
                # Verify all headers are removed using comprehensive check
                after_headers = test_file.get_metadata_headers_present()
                assert not after_headers['id3v2'], f"ID3v2.{version[1]} should be confirmed as removed"

    def _create_test_file_with_id3v2_version(self, id3v2_version):
        """Create a test file with specific ID3v2 version using the library's update_file_metadata function."""
        return TempFileWithId3v2Version(id3v2_version)


@pytest.mark.integration
class TestMixedFormatComprehensiveHeaderDeletion:

    def test_mixed_format_comprehensive_header_deletion(self):
        # Create a file with comprehensive metadata
        comprehensive_metadata = {
            "title": "Mixed Format Test Title",
            "artist": "Mixed Artist One",
            "album": "Mixed Format Test Album",
            "genre": "Mixed Test Genre",
            "year": "2023",
            "comment": "This is a mixed format test comment"
        }
        
        with TempFileWithMetadata(comprehensive_metadata, "mp3") as test_file:
            # Create a helper object to check headers
            header_checker = TempFileWithId3v2Version((2, 3, 0))
            header_checker.test_file = test_file.path
            
            # Verify comprehensive headers before deletion
            before_headers = header_checker.get_metadata_headers_present()
            print(f"Mixed format headers before deletion: {before_headers}")
            
            # Should have ID3v2
            assert before_headers['id3v2'], "Should have ID3v2 header"
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Verify comprehensive headers after deletion
            after_headers = header_checker.get_metadata_headers_present()
            print(f"Mixed format headers after deletion: {after_headers}")
            
            # Should not have any headers
            assert not after_headers['id3v2'], "ID3v2 should be removed"
