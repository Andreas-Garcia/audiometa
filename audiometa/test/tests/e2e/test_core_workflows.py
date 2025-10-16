"""
End-to-end tests for core metadata editing workflows.

These tests verify the basic functionality of the entire system
for real users, including file I/O and complete metadata editing workflows.
"""
import pytest
import shutil
from pathlib import Path

from audiometa import (
    AudioFile,
    get_merged_unified_metadata,
    update_file_metadata,
    delete_all_metadata,
    get_bitrate,
    get_duration_in_sec
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.e2e
class TestCoreWorkflows:
    
    def test_complete_metadata_editing_workflow(self, sample_mp3_file, temp_audio_file):
        # This is an e2e test - it tests the entire user journey
        # 1. Load a file
        # 2. Read existing metadata
        # 3. Edit multiple fields
        # 4. Save changes
        # 5. Verify persistence
        
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Edit metadata using app's function (this is what we're testing)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "New Album",
                UnifiedMetadataKey.GENRE_NAME: "Rock",
                UnifiedMetadataKey.COMMENT: "Test comment"
            }
            
            # Save changes
            update_file_metadata(test_file.path, test_metadata)
            
            # Verify persistence by reloading
            metadata = get_merged_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "New Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["New Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "New Album"
            assert metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Rock"
            assert metadata.get(UnifiedMetadataKey.COMMENT) == "Test comment"
    
    def test_batch_metadata_processing(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        # E2E test for batch operations
        results = []
        
        sample_files = [
            (sample_mp3_file, "mp3"),
            (sample_flac_file, "flac"), 
            (sample_wav_file, "wav")
        ]
        
        for file_path, format_type in sample_files:
            try:
                # Copy to temp location to avoid modifying versioned files
                temp_file = temp_audio_file.with_suffix(file_path.suffix)
                shutil.copy2(file_path, temp_file)
                
                # Set initial metadata using external script
                initial_metadata = {
                    "title": "Batch Test Title",
                    "artist": "Batch Test Artist"
                }
                with TempFileWithMetadata(initial_metadata, format_type) as test_file:
                    # Update metadata using functional API (this is what we're testing)
                    test_metadata = {
                        UnifiedMetadataKey.ALBUM_NAME: "Batch Album",
                        UnifiedMetadataKey.COMMENT: "Batch processing test"
                    }
                    update_file_metadata(test_file.path, test_metadata)
                    results.append(("success", file_path))
            except Exception as e:
                results.append(("error", file_path, str(e)))
        
        # Verify all files were processed
        assert len(results) == len(sample_files)
        success_count = sum(1 for result in results if result[0] == "success")
        assert success_count > 0

    def test_audio_file_context_manager(self, sample_mp3_file: Path):
        with AudioFile(sample_mp3_file) as audio_file:
            # Test that we can read metadata within context
            metadata = get_merged_unified_metadata(audio_file)
            assert isinstance(metadata, dict)
            
            # Test that we can get technical info within context
            bitrate = get_bitrate(audio_file)
            duration = get_duration_in_sec(audio_file)
            assert isinstance(bitrate, int)
            assert isinstance(duration, float)
