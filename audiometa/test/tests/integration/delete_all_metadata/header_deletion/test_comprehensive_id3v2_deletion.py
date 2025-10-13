import pytest
import tempfile
import shutil
from pathlib import Path

from audiometa import delete_all_metadata, update_file_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
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
                result = delete_all_metadata(test_file.test_file)
                assert result is True
                
                # Verify ID3v2 header is completely removed
                assert not test_file.has_id3v2_header(), f"ID3v2.{version[1]} header should be completely removed"
                
                # Verify all headers are removed using comprehensive check
                after_headers = test_file.get_metadata_headers_present()
                assert not after_headers['id3v2'], f"ID3v2.{version[1]} should be confirmed as removed"

    def _create_test_file_with_id3v2_version(self, id3v2_version):
        """Create a test file with specific ID3v2 version using the library's update_file_metadata function."""
        return TempFileWithId3v2Version(id3v2_version)


class TempFileWithId3v2Version:
    """Context manager for test files with specific ID3v2 version and automatic cleanup."""
    
    def __init__(self, id3v2_version):
        self.id3v2_version = id3v2_version
        self.test_file = None
    
    def __enter__(self) -> Path:
        """Create the test file with specific ID3v2 version and return its path."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            self.test_file = Path(tmp_file.name)
        
        # Copy from template file
        template_file = Path(__file__).parent.parent.parent.parent.parent / "data" / "audio_files" / "metadata=none.mp3"
        shutil.copy2(template_file, self.test_file)
        
        # Create comprehensive metadata with ID3v2 supported fields only
        comprehensive_metadata = {
            UnifiedMetadataKey.TITLE: "Comprehensive Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Primary Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Comprehensive Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre",
            UnifiedMetadataKey.RELEASE_DATE: "2023",
            UnifiedMetadataKey.COMMENT: "This is a comprehensive test comment"
        }
        
        # Use the library's update_file_metadata function with specific ID3v2 version
        update_file_metadata(self.test_file, comprehensive_metadata, id3v2_version=self.id3v2_version)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test file when exiting the context."""
        if self.test_file and self.test_file.exists():
            self.test_file.unlink()
    
    def has_id3v2_header(self) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes."""
        if not self.test_file:
            return False
        try:
            with open(self.test_file, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False
    
    def get_metadata_headers_present(self) -> dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file."""
        if not self.test_file:
            return {}
        return {
            'id3v2': self.has_id3v2_header(),
            'id3v1': False,  # We're not testing ID3v1 in this context
            'vorbis': False,  # We're not testing Vorbis in this context
            'riff': False   # We're not testing RIFF in this context
        }


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
            header_checker.test_file = test_file
            
            # Verify comprehensive headers before deletion
            before_headers = header_checker.get_metadata_headers_present()
            print(f"Mixed format headers before deletion: {before_headers}")
            
            # Should have ID3v2
            assert before_headers['id3v2'], "Should have ID3v2 header"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify comprehensive headers after deletion
            after_headers = header_checker.get_metadata_headers_present()
            print(f"Mixed format headers after deletion: {after_headers}")
            
            # Should not have any headers
            assert not after_headers['id3v2'], "ID3v2 should be removed"
