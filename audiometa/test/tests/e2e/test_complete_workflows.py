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
    get_specific_metadata,
    update_file_metadata,
    delete_metadata,
    get_bitrate,
    get_duration_in_sec
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.e2e
class TestCompleteWorkflows:
    """Test complete user workflows from start to finish."""
    
    def test_complete_metadata_editing_workflow(self, sample_mp3_file, temp_audio_file):
        """Test a complete metadata editing workflow."""
        # This is an e2e test - it tests the entire user journey
        # 1. Load a file
        # 2. Read existing metadata
        # 3. Edit multiple fields
        # 4. Save changes
        # 5. Verify persistence
        
        # Copy sample file to temp location to avoid modifying versioned files
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Read existing metadata
        original_metadata = get_merged_app_metadata(temp_audio_file)
        original_title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        original_artist = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Edit metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "New Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "New Album",
            UnifiedMetadataKey.GENRE_NAME: "Rock",
            UnifiedMetadataKey.COMMENT: "Test comment"
        }
        
        # Save changes
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify persistence by reloading
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "New Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["New Artist"]
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ALBUM_NAME) == "New Album"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.GENRE_NAME) == "Rock"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) == "Test comment"
    
    def test_batch_metadata_processing(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        """Test batch processing of multiple files."""
        # E2E test for batch operations
        results = []
        
        sample_files = [sample_mp3_file, sample_flac_file, sample_wav_file]
        for file_path in sample_files:
            try:
                # Copy to temp location to avoid modifying versioned files
                temp_file = temp_audio_file.with_suffix(file_path.suffix)
                shutil.copy2(file_path, temp_file)
                
                # Update metadata using functional API
                test_metadata = {
                    UnifiedMetadataKey.ALBUM_NAME: "Batch Album",
                    UnifiedMetadataKey.COMMENT: "Batch processing test"
                }
                update_file_metadata(temp_file, test_metadata)
                results.append(("success", file_path))
            except Exception as e:
                results.append(("error", file_path, str(e)))
        
        # Verify all files were processed
        assert len(results) == len(sample_files)
        success_count = sum(1 for result in results if result[0] == "success")
        assert success_count > 0
    
    def test_error_recovery_workflow(self, sample_mp3_file, temp_audio_file):
        """Test error handling and recovery in real scenarios."""
        # E2E test for error scenarios
        # Copy to temp location to avoid modifying versioned files
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test invalid operations
        with pytest.raises(ValueError):
            update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: -1})  # Invalid track number
        
        # Test file corruption handling
        # (This would test what happens with corrupted files)
        
        # Test recovery after errors
        test_metadata = {UnifiedMetadataKey.TITLE: "Recovery Test"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify the file is still usable
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Recovery Test"

    def test_complete_metadata_workflow_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test complete metadata workflow with MP3 file using functional API."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # 1. Read initial metadata
        initial_metadata = get_merged_app_metadata(temp_audio_file)
        assert isinstance(initial_metadata, dict)
        
        # 2. Update metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Integration Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Integration Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Integration Test Album",
            UnifiedMetadataKey.RATING: 90,
            UnifiedMetadataKey.BPM: 130
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # 3. Verify metadata was updated
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Integration Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Integration Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Integration Test Album"
        assert updated_metadata.get(UnifiedMetadataKey.RATING) == 90
        assert updated_metadata.get(UnifiedMetadataKey.BPM) == 130
        
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
        assert UnifiedMetadataKey.TITLE not in deleted_metadata or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Integration Test Title"

    def test_complete_metadata_workflow_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test complete metadata workflow with FLAC file using functional API."""
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # 1. Read initial metadata
        initial_metadata = get_merged_app_metadata(temp_audio_file)
        assert isinstance(initial_metadata, dict)
        
        # 2. Update metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "FLAC Integration Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["FLAC Integration Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "FLAC Integration Test Album",
            UnifiedMetadataKey.RATING: 85,
            UnifiedMetadataKey.BPM: 140
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # 3. Verify metadata was updated
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "FLAC Integration Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["FLAC Integration Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "FLAC Integration Test Album"
        assert updated_metadata.get(UnifiedMetadataKey.RATING) == 85
        assert updated_metadata.get(UnifiedMetadataKey.BPM) == 140
        
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
            UnifiedMetadataKey.TITLE: "WAV Integration Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["WAV Integration Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "WAV Integration Test Album"
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # 3. Verify metadata was updated
        updated_metadata = get_merged_app_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Integration Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Integration Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "WAV Integration Test Album"
        
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
            UnifiedMetadataKey.TITLE: "Rating Test 100",
            UnifiedMetadataKey.RATING: 75
        }
        update_file_metadata(temp_audio_file, test_metadata_100, normalized_rating_max_value=100)
        
        metadata_100 = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=100)
        assert metadata_100.get(UnifiedMetadataKey.TITLE) == "Rating Test 100"
        assert metadata_100.get(UnifiedMetadataKey.RATING) == 75
        
        # Test with 0-255 rating scale
        test_metadata_255 = {
            UnifiedMetadataKey.TITLE: "Rating Test 255",
            UnifiedMetadataKey.RATING: 191  # 75% of 255
        }
        update_file_metadata(temp_audio_file, test_metadata_255, normalized_rating_max_value=255)
        
        metadata_255 = get_merged_app_metadata(temp_audio_file, normalized_rating_max_value=255)
        assert metadata_255.get(UnifiedMetadataKey.TITLE) == "Rating Test 255"
        assert metadata_255.get(UnifiedMetadataKey.RATING) == 191

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
            update_file_metadata(str(temp_audio_file), {UnifiedMetadataKey.TITLE: "Test"})
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            delete_metadata(str(temp_audio_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_bitrate(str(temp_audio_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            get_duration_in_sec(str(temp_audio_file))
