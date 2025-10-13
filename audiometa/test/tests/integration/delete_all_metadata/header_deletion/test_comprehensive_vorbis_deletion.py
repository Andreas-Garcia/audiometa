import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestComprehensiveVorbisDeletion:

    def test_comprehensive_vorbis_header_deletion_flac(self):
        # Create comprehensive metadata with Vorbis supported fields only
        comprehensive_metadata = {
            "title": "Comprehensive FLAC Test Title",
            "artist": "FLAC Artist One",
            "album": "Comprehensive FLAC Test Album",
            "genre": "FLAC Test Genre",
            "year": "2023",
            "comment": "FLAC Test Comment"
        }
        
        temp_file_manager = TempFileWithMetadata(comprehensive_metadata, "flac")
        with temp_file_manager as test_file:
            # Check headers before deletion
            before_headers = temp_file_manager.get_metadata_headers_present()
            print(f"FLAC headers before deletion: {before_headers}")
            assert before_headers['vorbis'], "Vorbis should be present before deletion"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Check headers after deletion
            after_headers = temp_file_manager.get_metadata_headers_present()
            print(f"FLAC headers after deletion: {after_headers}")
            assert not after_headers['vorbis'], "Vorbis should be removed"
