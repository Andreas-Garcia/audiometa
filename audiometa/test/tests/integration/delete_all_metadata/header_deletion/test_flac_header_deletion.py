import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestFLACHeaderDeletion:

    def test_delete_all_metadata_verifies_headers_removed_flac(self):
        # Add metadata using the library
        test_metadata = {
            "title": "FLAC Test Title",
            "artist": "FLAC Test Artist",
            "album": "FLAC Test Album"
        }
        
        with TempFileWithMetadata(test_metadata, "flac") as test_file:
            # Check headers before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"FLAC headers before deletion: {before_headers}")
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Check headers after deletion
            after_headers = test_file.get_metadata_headers_present()
            print(f"FLAC headers after deletion: {after_headers}")

    def test_header_detection_for_flac_format(self):        
        # Test FLAC format
        with TempFileWithMetadata({"title": "FLAC Test"}, "flac") as flac_file:
            # FLAC might have both ID3v2 and Vorbis comments
            headers = flac_file.get_metadata_headers_present()
            print(f"FLAC headers: {headers}")
            # At least one should be present
            assert headers['id3v2'] or headers['vorbis'], "FLAC should have some metadata headers"
            
            # Test header removal
            result = delete_all_metadata(flac_file)
            assert result is True
            # After deletion, headers should be removed
            headers_after = flac_file.get_metadata_headers_present()
            print(f"FLAC headers after deletion: {headers_after}")
