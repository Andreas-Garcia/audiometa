"""
End-to-end tests for real user scenarios.

These tests simulate how actual users would interact with the library
in real-world applications.
"""
import pytest
import shutil
from pathlib import Path
from audiometa import AudioFile, get_merged_app_metadata, get_specific_metadata, update_file_metadata
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.e2e
class TestUserScenarios:
    """Test real-world user scenarios."""
    
    def test_music_library_organization(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        """Test organizing a music library with metadata."""
        # Simulate a user organizing their music library
        
        sample_files = [sample_mp3_file, sample_flac_file, sample_wav_file]
        for i, file_path in enumerate(sample_files[:3]):  # Test with first 3 files
            # Copy to temp location to avoid modifying versioned files
            temp_file = temp_audio_file.with_suffix(file_path.suffix)
            shutil.copy2(file_path, temp_file)
            
            # Set consistent metadata for organization
            test_metadata = {
                AppMetadataKey.ALBUM_NAME: "My Music Library",
                AppMetadataKey.TITLE: f"Track {i + 1}"
            }
            update_file_metadata(temp_file, test_metadata)
            
            # Verify the organization worked
            assert get_specific_metadata(temp_file, AppMetadataKey.ALBUM_NAME) == "My Music Library"
            assert get_specific_metadata(temp_file, AppMetadataKey.TITLE) == f"Track {i + 1}"
    
    def test_metadata_import_export_workflow(self, sample_mp3_file, temp_audio_file):
        """Test importing and exporting metadata."""
        # Simulate a user importing metadata from external source
        # Copy to temp location to avoid modifying versioned files
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Export current metadata
        metadata = {
            'title': get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE),
            'artist': get_specific_metadata(temp_audio_file, AppMetadataKey.ARTISTS_NAMES),
            'album': get_specific_metadata(temp_audio_file, AppMetadataKey.ALBUM_NAME)
        }
        
        # Simulate external metadata update
        metadata['title'] = "Updated Title"
        metadata['artist'] = ["Updated Artist"]
        
        # Apply updated metadata
        test_metadata = {
            AppMetadataKey.TITLE: metadata['title'],
            AppMetadataKey.ARTISTS_NAMES: metadata['artist'],
            AppMetadataKey.ALBUM_NAME: metadata['album']
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify the import worked
        assert get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE) == "Updated Title"
        assert get_specific_metadata(temp_audio_file, AppMetadataKey.ARTISTS_NAMES) == ["Updated Artist"]
    
    def test_cross_format_compatibility(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        """Test metadata consistency across different audio formats."""
        # Test that metadata works consistently across MP3, FLAC, etc.
        
        test_metadata = {
            AppMetadataKey.TITLE: 'Cross Format Test',
            AppMetadataKey.ARTISTS_NAMES: ['Test Artist'],
            AppMetadataKey.ALBUM_NAME: 'Test Album'
        }
        
        sample_files = [sample_mp3_file, sample_flac_file, sample_wav_file]
        for file_path in sample_files:
            # Copy to temp location to avoid modifying versioned files
            temp_file = temp_audio_file.with_suffix(file_path.suffix)
            shutil.copy2(file_path, temp_file)
            
            # Set metadata
            update_file_metadata(temp_file, test_metadata)
            
            # Verify metadata was set correctly
            assert get_specific_metadata(temp_file, AppMetadataKey.TITLE) == test_metadata[AppMetadataKey.TITLE]
            assert get_specific_metadata(temp_file, AppMetadataKey.ARTISTS_NAMES) == test_metadata[AppMetadataKey.ARTISTS_NAMES]
            assert get_specific_metadata(temp_file, AppMetadataKey.ALBUM_NAME) == test_metadata[AppMetadataKey.ALBUM_NAME]
