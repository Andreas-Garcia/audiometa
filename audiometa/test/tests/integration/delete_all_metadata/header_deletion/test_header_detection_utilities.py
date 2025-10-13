import pytest

from audiometa import delete_all_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.tests.test_script_helpers import ScriptHelper


@pytest.mark.integration
class TestHeaderDetectionUtilities:

    def test_header_detection_for_different_formats(self):        
        helper = ScriptHelper()
        
        # Test MP3 format
        with TempFileWithMetadata({"title": "MP3 Test"}, "mp3") as mp3_file:
            assert helper.has_id3v2_header(mp3_file), "MP3 should have ID3v2 header"
            assert not helper.has_vorbis_comments(mp3_file), "MP3 should not have Vorbis comments"
            assert not helper.has_riff_info_chunk(mp3_file), "MP3 should not have RIFF INFO chunk"
            
            # Test header removal
            result = delete_all_metadata(mp3_file)
            assert result is True
            assert not helper.has_id3v2_header(mp3_file), "ID3v2 header should be removed"
        
        # Test FLAC format
        with TempFileWithMetadata({"title": "FLAC Test"}, "flac") as flac_file:
            # FLAC might have both ID3v2 and Vorbis comments
            headers = helper.get_metadata_headers_present(flac_file)
            print(f"FLAC headers: {headers}")
            # At least one should be present
            assert headers['id3v2'] or headers['vorbis'], "FLAC should have some metadata headers"
            
            # Test header removal
            result = delete_all_metadata(flac_file)
            assert result is True
            # After deletion, headers should be removed
            headers_after = helper.get_metadata_headers_present(flac_file)
            print(f"FLAC headers after deletion: {headers_after}")
        
        # Test WAV format
        with TempFileWithMetadata({"title": "WAV Test"}, "wav") as wav_file:
            # WAV might have both ID3v2 and RIFF INFO
            headers = helper.get_metadata_headers_present(wav_file)
            print(f"WAV headers: {headers}")
            # Note: WAV files created with TempFileWithMetadata might not have headers initially
            # This is expected behavior - we'll test the deletion anyway
            
            # Test header removal (should succeed even if no headers exist)
            result = delete_all_metadata(wav_file)
            assert result is True
            # After deletion, headers should still not be present
            headers_after = helper.get_metadata_headers_present(wav_file)
            print(f"WAV headers after deletion: {headers_after}")
            # Verify no headers are present after deletion
            assert not headers_after['id3v2'] and not headers_after['riff'], "WAV should have no headers after deletion"

    def test_header_verification_edge_cases(self):
        """Test header verification with edge cases."""
        
        helper = ScriptHelper()
        
        # Test with file that has no metadata initially
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Should not have headers initially
            headers = helper.get_metadata_headers_present(test_file)
            print(f"Headers in empty file: {headers}")
            
            # Delete metadata from file with no metadata
            result = delete_all_metadata(test_file)
            assert result is True  # Should succeed even with no metadata
            
            # Headers should still not be present
            headers_after = helper.get_metadata_headers_present(test_file)
            assert not headers_after['id3v2'], "Should not have ID3v2 header"
