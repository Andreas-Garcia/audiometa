"""
End-to-end tests for complete user workflows.

These tests verify that the entire system works as expected for real users,
including file I/O, error handling, and complete metadata editing workflows.
"""
import pytest
import os
import tempfile
from pathlib import Path

from audiometa import AudioFile


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
