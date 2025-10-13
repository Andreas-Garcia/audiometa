import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestComprehensiveRiffDeletion:

    def test_comprehensive_riff_header_deletion_wav(self):        
        # Create comprehensive metadata with RIFF supported fields only
        comprehensive_metadata = {
            "title": "Comprehensive WAV Test Title",
            "artist": "WAV Artist One",
            "album": "Comprehensive WAV Test Album",
            "genre": "WAV Test Genre",
            "year": "2023",
            "comment": "WAV Test Comment"
        }
        
        temp_file_manager = TempFileWithMetadata(comprehensive_metadata, "wav")
        with temp_file_manager as test_file:
            # Check headers before deletion
            before_headers = temp_file_manager.get_metadata_headers_present()
            print(f"WAV headers before deletion: {before_headers}")
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Check headers after deletion
            after_headers = temp_file_manager.get_metadata_headers_present()
            print(f"WAV headers after deletion: {after_headers}")
            # Verify no RIFF headers remain after deletion
            assert not after_headers['riff'], "RIFF should be removed"
