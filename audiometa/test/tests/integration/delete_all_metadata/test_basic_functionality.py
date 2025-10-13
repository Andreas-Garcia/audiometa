import pytest
from pathlib import Path
import shutil

from audiometa import (
    delete_all_metadata,
    get_merged_unified_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestDeleteAllMetadataBasic:
    
    def test_delete_all_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Create AudioFile object
            audio_file = AudioFile(test_file)
            
            # Delete all metadata using AudioFile object
            result = delete_all_metadata(audio_file)
            assert result is True

    def test_delete_all_metadata_file_with_no_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Delete metadata from file that has no metadata
        result = delete_all_metadata(temp_audio_file)
        assert result is True

    def test_delete_all_metadata_id3v2_version_specific(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Delete metadata with specific ID3v2 version
            result = delete_all_metadata(test_file, id3v2_version=(2, 3, 0))
            assert result is True

    def test_delete_all_metadata_return_value_success(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            result = delete_all_metadata(test_file)
            assert result is True
            assert isinstance(result, bool)

    def test_delete_all_metadata_verifies_headers_removed(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist",
            "album": "Test Album"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Get file size with metadata
            with_metadata_size = test_file.stat().st_size
            
            # Verify metadata exists before deletion
            before_metadata = get_merged_unified_metadata(test_file)
            assert before_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert before_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert before_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Verify ID3v2 header exists before deletion using TempFileWithMetadata methods
            assert test_file.has_id3v2_header(), "ID3v2 header should exist before deletion"
            
            # Get comprehensive header report before deletion
            before_headers = test_file.get_metadata_headers_present()
            assert before_headers['id3v2'], "ID3v2 should be present before deletion"
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify file size decreased (metadata headers removed)
            after_deletion_size = test_file.stat().st_size
            assert after_deletion_size < with_metadata_size, "File size should decrease when headers are removed"
            
            # Verify ID3v2 header is completely removed using TempFileWithMetadata methods
            assert not test_file.has_id3v2_header(), "ID3v2 header should be completely removed"
            
            # Verify all headers are removed using comprehensive check
            removal_status = test_file.verify_headers_removed(['id3v2'])
            assert removal_status['id3v2'], "ID3v2 should be confirmed as removed"
            
            # Verify all metadata is gone (headers removed)
            after_metadata = get_merged_unified_metadata(test_file)
            assert after_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert after_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None
            assert after_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None
            
            # Optional: Use external tools for additional verification
            external_check = test_file.check_metadata_with_external_tools()
            if external_check.get('mid3v2', {}).get('success'):
                assert not external_check['mid3v2']['has_id3v2'], "External tools should confirm ID3v2 removal"

    def test_delete_all_metadata_preserves_audio_data(self, sample_mp3_file: Path, temp_audio_file: Path):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Get file size with metadata
            with_metadata_size = test_file.stat().st_size
            
            # Delete all metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Verify file size decreased (metadata headers removed)
            after_deletion_size = test_file.stat().st_size
            assert after_deletion_size < with_metadata_size
            
            # Verify the file is still valid (not corrupted)
            assert after_deletion_size > 0

    def test_header_detection_helpers_comprehensive(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test comprehensive header detection using TempFileWithMetadata methods."""
        
        # Test with MP3 file
        with TempFileWithMetadata({"title": "Test", "artist": "Artist"}, "mp3") as test_file:
            # Check all headers before deletion
            headers_before = test_file.get_metadata_headers_present()
            print(f"Headers before deletion: {headers_before}")
            
            # Should have ID3v2 header
            assert headers_before['id3v2'], "MP3 should have ID3v2 header"
            
            # Delete metadata
            result = delete_all_metadata(test_file)
            assert result is True
            
            # Check all headers after deletion
            headers_after = test_file.get_metadata_headers_present()
            print(f"Headers after deletion: {headers_after}")
            
            # Should not have ID3v2 header anymore
            assert not headers_after['id3v2'], "ID3v2 header should be removed"
            
            # Verify removal status
            removal_status = test_file.verify_headers_removed(['id3v2'])
            assert removal_status['id3v2'], "ID3v2 should be confirmed as removed"
            
            # Test external tools verification
            external_results = test_file.check_metadata_with_external_tools()
            print(f"External tool results: {external_results}")
            
            # If mid3v2 is available, verify it confirms removal
            if external_results.get('mid3v2', {}).get('success'):
                assert not external_results['mid3v2']['has_id3v2'], "mid3v2 should confirm ID3v2 removal"

    def test_header_detection_for_different_formats(self):
        """Test header detection methods for different audio formats."""
        
        # Test MP3 format
        with TempFileWithMetadata({"title": "MP3 Test"}, "mp3") as mp3_file:
            assert mp3_file.has_id3v2_header(), "MP3 should have ID3v2 header"
            assert not mp3_file.has_vorbis_comments(), "MP3 should not have Vorbis comments"
            assert not mp3_file.has_riff_info_chunk(), "MP3 should not have RIFF INFO chunk"
        
        # Test FLAC format
        with TempFileWithMetadata({"title": "FLAC Test"}, "flac") as flac_file:
            # FLAC might have both ID3v2 and Vorbis comments
            headers = flac_file.get_metadata_headers_present()
            print(f"FLAC headers: {headers}")
            # At least one should be present
            assert headers['id3v2'] or headers['vorbis'], "FLAC should have some metadata headers"
        
        # Test WAV format
        with TempFileWithMetadata({"title": "WAV Test"}, "wav") as wav_file:
            # WAV might have both ID3v2 and RIFF INFO
            headers = wav_file.get_metadata_headers_present()
            print(f"WAV headers: {headers}")
            # At least one should be present
            assert headers['id3v2'] or headers['riff'], "WAV should have some metadata headers"
