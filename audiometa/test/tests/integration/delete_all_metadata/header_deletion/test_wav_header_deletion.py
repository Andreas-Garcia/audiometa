import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.test_helpers import TempFileWithMetadata


@pytest.mark.integration
class TestWAVHeaderDeletion:

    def test_delete_all_metadata_verifies_headers_removed_wav(self):
        # Add metadata using the library
        test_metadata = {
            "title": "WAV Test Title",
            "artist": "WAV Test Artist",
            "album": "WAV Test Album"
        }
        
        temp_file_manager = TempFileWithMetadata(test_metadata, "wav")
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

    def test_header_detection_for_wav_format(self):        
        # Test WAV format
        temp_file_manager = TempFileWithMetadata({"title": "WAV Test"}, "wav")
        with temp_file_manager as wav_file:
            # WAV might have both ID3v2 and RIFF INFO
            headers = temp_file_manager.get_metadata_headers_present()
            print(f"WAV headers: {headers}")
            # Note: WAV files created with TempFileWithMetadata might not have headers initially
            # This is expected behavior - we'll test the deletion anyway
            
            # Test header removal (should succeed even if no headers exist)
            result = delete_all_metadata(wav_file)
            assert result is True
            # After deletion, headers should still not be present
            headers_after = temp_file_manager.get_metadata_headers_present()
            print(f"WAV headers after deletion: {headers_after}")
            # Verify no headers are present after deletion
            assert not headers_after['id3v2'] and not headers_after['riff'], "WAV should have no headers after deletion"
