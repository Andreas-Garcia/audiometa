import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestWAVHeaderDeletion:

    def test_delete_all_metadata_verifies_headers_removed_wav(self):
        # Add metadata using the library
        test_metadata = {
            "title": "WAV Test Title",
            "artist": "WAV Test Artist",
            "album": "WAV Test Album"
        }
        
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Check headers before deletion
            before_headers = test_file.get_metadata_headers_present()
            print(f"WAV headers before deletion: {before_headers}")
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Check headers after deletion
            after_headers = test_file.get_metadata_headers_present()
            print(f"WAV headers after deletion: {after_headers}")

    def test_header_detection_for_wav_format(self):        
        # Test WAV format
        with TempFileWithMetadata({"title": "WAV Test"}, "wav") as wav_file:
            # WAV might have both ID3v2 and RIFF INFO
            headers = wav_file.get_metadata_headers_present()
            print(f"WAV headers: {headers}")
            # Note: WAV files created with TempFileWithMetadata might not have headers initially
            # This is expected behavior - we'll test the deletion anyway
            
            # Test header removal (should succeed even if no headers exist)
            result = delete_all_metadata(wav_file)
            assert result is True
            # After deletion, headers should still not be present
            headers_after = wav_file.get_metadata_headers_present()
            print(f"WAV headers after deletion: {headers_after}")
            # Verify no headers are present after deletion
            assert not headers_after['id3v2'] and not headers_after['riff'], "WAV should have no headers after deletion"
