"""
End-to-end tests for real user scenarios using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.

These tests simulate how actual users would interact with the library
in real-world applications.
"""
import pytest
import shutil
from pathlib import Path
from audiometa import AudioFile, get_merged_unified_metadata, get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.test_script_helpers import create_test_file_with_specific_metadata


@pytest.mark.e2e
class TestUserScenarios:
    
    def test_music_library_organization(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        # Simulate a user organizing their music library
        
        sample_files = [
            (sample_mp3_file, "mp3"),
            (sample_flac_file, "flac"),
            (sample_wav_file, "wav")
        ]
        
        for i, (file_path, format_type) in enumerate(sample_files[:3]):  # Test with first 3 files
            # Copy to temp location to avoid modifying versioned files
            temp_file = temp_audio_file.with_suffix(file_path.suffix)
            shutil.copy2(file_path, temp_file)
            
            # Set basic metadata using external script
            basic_metadata = {
                "title": f"Original Track {i + 1}",
                "artist": "Original Artist"
            }
            create_test_file_with_specific_metadata(
                file_path,
                temp_file,
                basic_metadata,
                format_type
            )
            
            # Set consistent metadata for organization using app's function (this is what we're testing)
            test_metadata = {
                UnifiedMetadataKey.ALBUM_NAME: "My Music Library",
                UnifiedMetadataKey.TITLE: f"Track {i + 1}"
            }
            update_file_metadata(temp_file, test_metadata)
            
            # Verify the organization worked
            assert get_specific_metadata(temp_file, UnifiedMetadataKey.ALBUM_NAME) == "My Music Library"
            assert get_specific_metadata(temp_file, UnifiedMetadataKey.TITLE) == f"Track {i + 1}"
    
    def test_metadata_import_export_workflow(self, sample_mp3_file, temp_audio_file):
        # Simulate a user importing metadata from external source
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album"
        }
        create_test_file_with_specific_metadata(
            sample_mp3_file,
            temp_audio_file,
            initial_metadata,
            "mp3"
        )
        
        # Export current metadata
        metadata = {
            'title': get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE),
            'artist': get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES),
            'album': get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ALBUM_NAME)
        }
        
        # Simulate external metadata update
        metadata['title'] = "Updated Title"
        metadata['artist'] = ["Updated Artist"]
        
        # Apply updated metadata using app's function (this is what we're testing)
        test_metadata = {
            UnifiedMetadataKey.TITLE: metadata['title'],
            UnifiedMetadataKey.ARTISTS_NAMES: metadata['artist'],
            UnifiedMetadataKey.ALBUM_NAME: metadata['album']
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify the import worked
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Updated Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Updated Artist"]
    
    def test_cross_format_compatibility(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        # Test that metadata works consistently across MP3, FLAC, etc.
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: 'Cross Format Test',
            UnifiedMetadataKey.ARTISTS_NAMES: ['Test Artist'],
            UnifiedMetadataKey.ALBUM_NAME: 'Test Album'
        }
        
        sample_files = [
            (sample_mp3_file, "mp3"),
            (sample_flac_file, "flac"),
            (sample_wav_file, "wav")
        ]
        
        for file_path, format_type in sample_files:
            # Copy to temp location to avoid modifying versioned files
            temp_file = temp_audio_file.with_suffix(file_path.suffix)
            shutil.copy2(file_path, temp_file)
            
            # Set basic metadata using external script
            basic_metadata = {
                "title": "Original Title",
                "artist": "Original Artist"
            }
            create_test_file_with_specific_metadata(
                file_path,
                temp_file,
                basic_metadata,
                format_type
            )
            
            # Set metadata using app's function (this is what we're testing)
            update_file_metadata(temp_file, test_metadata)
            
            # Verify metadata was set correctly
            assert get_specific_metadata(temp_file, UnifiedMetadataKey.TITLE) == test_metadata[UnifiedMetadataKey.TITLE]
            assert get_specific_metadata(temp_file, UnifiedMetadataKey.ARTISTS_NAMES) == test_metadata[UnifiedMetadataKey.ARTISTS_NAMES]
            assert get_specific_metadata(temp_file, UnifiedMetadataKey.ALBUM_NAME) == test_metadata[UnifiedMetadataKey.ALBUM_NAME]