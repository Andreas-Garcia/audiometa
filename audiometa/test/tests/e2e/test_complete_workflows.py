"""
End-to-end tests for complete user workflows.

These tests verify that the entire system works as expected for real users,
including file I/O, error handling, and complete metadata editing workflows.
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path

from audiometa import (
    AudioFile,
    get_merged_app_metadata,
    update_file_metadata,
    delete_metadata,
    get_bitrate,
    get_duration_in_sec
)
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.e2e
class TestCompleteWorkflows:
    """Test complete user workflows from start to finish."""
    
    def test_complete_metadata_editing_workflow(self, sample_mp3_file):
        """Test a complete metadata editing workflow."""
        # This is an e2e test - it tests the entire user journey
        # 1. Load a file
        # 2. Read existing metadata
        # 3. Edit multiple fields
        # 4. Save changes
        # 5. Verify persistence
        
        # Load file
        audio_file = AudioFile(sample_mp3_file)
        
        # Read existing metadata
        original_title = audio_file.get_title()
        original_artist = audio_file.get_artist()
        
        # Edit metadata
        audio_file.set_title("New Title")
        audio_file.set_artist("New Artist")
        audio_file.set_album("New Album")
        audio_file.set_genre("Rock")
        audio_file.set_year(2024)
        
        # Save changes
        audio_file.save()
        
        # Verify persistence by reloading
        audio_file_reloaded = AudioFile(sample_mp3_file)
        assert audio_file_reloaded.get_title() == "New Title"
        assert audio_file_reloaded.get_artist() == "New Artist"
        assert audio_file_reloaded.get_album() == "New Album"
        assert audio_file_reloaded.get_genre() == "Rock"
        assert audio_file_reloaded.get_year() == 2024
    
    def test_batch_metadata_processing(self, sample_files):
        """Test batch processing of multiple files."""
        # E2E test for batch operations
        results = []
        
        for file_path in sample_files:
            try:
                audio_file = AudioFile(file_path)
                audio_file.set_album("Batch Album")
                audio_file.set_year(2024)
                audio_file.save()
                results.append(("success", file_path))
            except Exception as e:
                results.append(("error", file_path, str(e)))
        
        # Verify all files were processed
        assert len(results) == len(sample_files)
        success_count = sum(1 for result in results if result[0] == "success")
        assert success_count > 0
    
    def test_error_recovery_workflow(self, sample_mp3_file):
        """Test error handling and recovery in real scenarios."""
        # E2E test for error scenarios
        audio_file = AudioFile(sample_mp3_file)
        
        # Test invalid operations
        with pytest.raises(ValueError):
            audio_file.set_year(-1)  # Invalid year
        
        # Test file corruption handling
        # (This would test what happens with corrupted files)
        
        # Test recovery after errors
        audio_file.set_title("Recovery Test")
        audio_file.save()
        
        # Verify the file is still usable
        reloaded = AudioFile(sample_mp3_file)
        assert reloaded.get_title() == "Recovery Test"

    def test_complete_metadata_workflow_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test complete metadata workflow with MP3 file using functional API."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # 1. Read initial metadata
        initial_metadata = get_merged_app_metadata(temp_audio_file)
        assert isinstance(initial_metadata, dict)
        
        # 2. Update metadata
        test_metadata = {
            AppMetadataKey.TITLE: "Integration Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["Integration Test Artist"],
            AppMetadataKey.ALBUM_NAME: "Integration Test Album",
            AppMetadataKey.RATING: 90,
            AppMetadataKey.BPM: 130
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # 3. Verify metadata was updated
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Integration Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Integration Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Integration Test Album"
        assert updated_metadata.get(AppMetadataKey.RATING) == 90
        assert updated_metadata.get(AppMetadataKey.BPM) == 130
        
        # 4. Test technical information
        bitrate = get_bitrate(temp_audio_file)
        duration = get_duration_in_sec(temp_audio_file)
        assert isinstance(bitrate, int)
        assert isinstance(duration, float)
        assert bitrate > 0
        assert duration > 0
        
        # 5. Delete metadata
        delete_result = delete_metadata(temp_audio_file)
        assert delete_result is True
        
        # 6. Verify metadata was deleted
        deleted_metadata = get_merged_app_metadata(temp_audio_file)
        # After deletion, metadata should be empty or minimal
        assert AppMetadataKey.TITLE not in deleted_metadata or deleted_metadata.get(AppMetadataKey.TITLE) != "Integration Test Title"

    def test_complete_metadata_workflow_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test complete metadata workflow with FLAC file using functional API."""
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # 1. Read initial metadata
        initial_metadata = get_merged_app_metadata(temp_audio_file)
        assert isinstance(initial_metadata, dict)
        
        # 2. Update metadata
        test_metadata = {
            AppMetadataKey.TITLE: "FLAC Integration Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["FLAC Integration Test Artist"],
            AppMetadataKey.ALBUM_NAME: "FLAC Integration Test Album",
            AppMetadataKey.RATING: 85,
            AppMetadataKey.BPM: 140
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # 3. Verify metadata was updated
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "FLAC Integration Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["FLAC Integration Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "FLAC Integration Test Album"
        assert updated_metadata.get(AppMetadataKey.RATING) == 85
        assert updated_metadata.get(AppMetadataKey.BPM) == 140
        
        # 4. Test technical information
        bitrate = get_bitrate(temp_audio_file)
        duration = get_duration_in_sec(temp_audio_file)
        assert isinstance(bitrate, int)
        assert isinstance(duration, float)
        assert bitrate > 0
        assert duration > 0

    def test_complete_metadata_workflow_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test complete metadata workflow with WAV file using functional API."""
        # Copy sample file to temp location
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # 1. Read initial metadata
        initial_metadata = get_merged_app_metadata(temp_audio_file)
        assert isinstance(initial_metadata, dict)
        
        # 2. Update metadata (WAV doesn't support rating or BPM)
        test_metadata = {
            AppMetadataKey.TITLE: "WAV Integration Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["WAV Integration Test Artist"],
            AppMetadataKey.ALBUM_NAME: "WAV Integration Test Album"
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # 3. Verify metadata was updated
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(AppMetadataKey.TITLE) == "WAV Integration Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["WAV Integration Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "WAV Integration Test Album"
        
        # 4. Test technical information
        bitrate = get_bitrate(temp_audio_file)
        duration = get_duration_in_sec(temp_audio_file)
        assert isinstance(bitrate, int)
        assert isinstance(duration, float)
        assert bitrate > 0
        assert duration > 0

    def test_audio_file_context_manager(self, sample_mp3_file: Path):
        """Test AudioFile as context manager."""
        with AudioFile(sample_mp3_file) as audio_file:
            # Test that we can read metadata within context
            metadata = get_merged_app_metadata(audio_file)
            assert isinstance(metadata, dict)
            
            # Test that we can get technical info within context
            bitrate = get_bitrate(audio_file)
            duration = get_duration_in_sec(audio_file)
            assert isinstance(bitrate, int)
            assert isinstance(duration, float)

    def test_metadata_with_different_rating_normalizations(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test metadata handling with different rating normalizations."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test with 0-100 rating scale
        test_metadata_100 = {
            AppMetadataKey.TITLE: "Rating Test 100",
            AppMetadataKey.RATING: 75
        }
        update_file_metadata(temp_audio_file, test_metadata_100, normalized_rating_max_value=100)
        
        metadata_100 = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata_100.get(AppMetadataKey.TITLE) == "Rating Test 100"
        assert metadata_100.get(AppMetadataKey.RATING) == 75
        
        # Test with 0-255 rating scale
        test_metadata_255 = {
            AppMetadataKey.TITLE: "Rating Test 255",
            AppMetadataKey.RATING: 191  # 75% of 255
        }
        update_file_metadata(temp_audio_file, test_metadata_255, normalized_rating_max_value=255)
        
        metadata_255 = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=255)
        assert metadata_255.get(AppMetadataKey.TITLE) == "Rating Test 255"
        assert metadata_255.get(AppMetadataKey.RATING) == 191

    def test_error_handling_workflow(self, temp_audio_file: Path):
        """Test error handling in the complete workflow."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        # All operations should raise FileTypeNotSupportedError
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_merged_app_metadata(str(temp_audio_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            update_file_metadata(str(temp_audio_file), {AppMetadataKey.TITLE: "Test"})
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            delete_metadata(str(temp_audio_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_bitrate(str(temp_audio_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_duration_in_sec(str(temp_audio_file))
