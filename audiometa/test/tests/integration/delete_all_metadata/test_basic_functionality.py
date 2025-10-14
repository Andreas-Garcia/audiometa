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
            audio_file = AudioFile(test_file.path)
            
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
            result = delete_all_metadata(test_file.path, id3v2_version=(2, 3, 0))
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
            result = delete_all_metadata(test_file.path)
            assert result is True
            assert isinstance(result, bool)


    def test_delete_all_metadata_preserves_audio_data(self, sample_mp3_file: Path, temp_audio_file: Path):
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Get file size with metadata
            with_metadata_size = test_file.path.stat().st_size
            
            # Delete all metadata
            result = delete_all_metadata(test_file.path)
            assert result is True
            
            # Verify file size decreased (metadata headers removed)
            after_deletion_size = test_file.path.stat().st_size
            assert after_deletion_size < with_metadata_size
            
            # Verify the file is still valid (not corrupted)
            assert after_deletion_size > 0


    def test_header_detection_for_different_formats(self):
        """Test header detection methods for different audio formats."""
        
        # Test MP3 format
        with TempFileWithMetadata({"title": "MP3 Test"}, "mp3") as mp3_manager:
            assert mp3_manager.has_id3v2_header(), "MP3 should have ID3v2 header"
            assert not mp3_manager.has_vorbis_comments(), "MP3 should not have Vorbis comments"
            assert not mp3_manager.has_riff_info_chunk(), "MP3 should not have RIFF INFO chunk"
        
        # Test FLAC format
        with TempFileWithMetadata({"title": "FLAC Test"}, "flac") as flac_manager:
            # FLAC might have both ID3v2 and Vorbis comments
            headers = flac_manager.get_metadata_headers_present()
            print(f"FLAC headers: {headers}")
            # At least one should be present
            assert headers['id3v2'] or headers['vorbis'], "FLAC should have some metadata headers"
        
        # Test WAV format
        with TempFileWithMetadata({"title": "WAV Test"}, "wav") as wav_manager:
            # WAV might have both ID3v2 and RIFF INFO
            headers = wav_manager.get_metadata_headers_present()
            print(f"WAV headers: {headers}")
            # At least one should be present
            assert headers['id3v2'] or headers['riff'], "WAV should have some metadata headers"
