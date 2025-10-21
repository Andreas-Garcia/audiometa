"""
End-to-end tests for real user scenarios using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.

These tests simulate how actual users would interact with the library
in real-world applications.
"""
import pytest
from audiometa import get_unified_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


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
            # Set basic metadata using external script
            basic_metadata = {
                "title": f"Original Track {i + 1}",
                "artist": "Original Artist"
            }
            with TempFileWithMetadata(basic_metadata, format_type) as test_file:
                # Set consistent metadata for organization using app's function (this is what we're testing)
                test_metadata = {
                    UnifiedMetadataKey.ALBUM_NAME: "My Music Library",
                    UnifiedMetadataKey.TITLE: f"Track {i + 1}"
                }
                update_metadata(test_file.path, test_metadata)
                
                # Verify the organization worked
                metadata = get_unified_metadata(test_file.path)
                assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "My Music Library"
                assert metadata.get(UnifiedMetadataKey.TITLE) == f"Track {i + 1}"
    
    def test_metadata_import_export_workflow(self, sample_mp3_file):
        # Simulate a user importing metadata from external source
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Export current metadata
            current_metadata = get_unified_metadata(test_file.path)
            metadata = {
                'title': current_metadata.get(UnifiedMetadataKey.TITLE),
                'artist': current_metadata.get(UnifiedMetadataKey.ARTISTS),
                'album': current_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
            }
            
            # Simulate external metadata update
            metadata['title'] = "Updated Title"
            metadata['artist'] = ["Updated Artist"]
            
            # Apply updated metadata using app's function (this is what we're testing)
            test_metadata = {
                UnifiedMetadataKey.TITLE: metadata['title'],
                UnifiedMetadataKey.ARTISTS: metadata['artist'],
                UnifiedMetadataKey.ALBUM_NAME: metadata['album']
            }
            update_metadata(test_file.path, test_metadata)
            
            # Verify the import worked
            updated_metadata = get_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Updated Title"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Updated Artist"]
    
    def test_metadata_privacy_cleanup_workflow(self, sample_mp3_file):
        # Simulate a user cleaning up metadata for privacy before sharing files
        initial_metadata = {
            "title": "Personal Music Track",
            "artist": "Personal Artist",
            "album": "Personal Album",
            "comment": "Personal comment with sensitive info"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # 1. Verify initial metadata exists
            initial_metadata_result = get_unified_metadata(test_file)
            assert initial_metadata_result.get(UnifiedMetadataKey.TITLE) == "Personal Music Track"
            assert initial_metadata_result.get(UnifiedMetadataKey.COMMENT) == "Personal comment with sensitive info"
            
            # 2. User decides to clean up sensitive metadata
            cleanup_metadata = {
                UnifiedMetadataKey.COMMENT: None,  # Remove personal comment
                UnifiedMetadataKey.ALBUM_NAME: "Generic Album"  # Replace personal album
            }
            update_metadata(test_file.path, cleanup_metadata)
            
            # 3. Verify sensitive data was removed
            cleaned_metadata = get_unified_metadata(test_file)
            assert cleaned_metadata.get(UnifiedMetadataKey.COMMENT) is None
            assert cleaned_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Generic Album"
            assert cleaned_metadata.get(UnifiedMetadataKey.TITLE) == "Personal Music Track"  # Title remains
            
            # 4. User decides to remove all metadata for complete privacy
            delete_result = delete_all_metadata(test_file)
            assert delete_result is True
            
            # 5. Verify all metadata is removed
            final_metadata = get_unified_metadata(test_file)
            assert final_metadata.get(UnifiedMetadataKey.TITLE) is None or final_metadata.get(UnifiedMetadataKey.TITLE) != "Personal Music Track"
            assert final_metadata.get(UnifiedMetadataKey.COMMENT) is None

    def test_metadata_correction_workflow(self, sample_mp3_file):
        # Simulate a user correcting incorrect metadata
        initial_metadata = {
            "title": "Wrong Title",
            "artist": "Wrong Artist",
            "album": "Wrong Album"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # 1. Verify initial incorrect metadata
            initial_metadata_result = get_unified_metadata(test_file)
            assert initial_metadata_result.get(UnifiedMetadataKey.TITLE) == "Wrong Title"
            
            # 2. User realizes the metadata is wrong and wants to start fresh
            # Delete all metadata first
            delete_result = delete_all_metadata(test_file)
            assert delete_result is True
            
            # 3. Verify metadata was deleted
            deleted_metadata = get_unified_metadata(test_file)
            assert deleted_metadata.get(UnifiedMetadataKey.TITLE) is None or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Wrong Title"
            
            # 4. Add correct metadata
            correct_metadata = {
                UnifiedMetadataKey.TITLE: "Correct Title",
                UnifiedMetadataKey.ARTISTS: ["Correct Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Correct Album"
            }
            update_metadata(test_file.path, correct_metadata)
            
            # 5. Verify correct metadata was added
            final_metadata = get_unified_metadata(test_file)
            assert final_metadata.get(UnifiedMetadataKey.TITLE) == "Correct Title"
            assert final_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Correct Artist"]
            assert final_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Correct Album"
    
    def test_cross_format_compatibility(self, sample_mp3_file, sample_flac_file, sample_wav_file, temp_audio_file):
        # Test that metadata works consistently across MP3, FLAC, etc.
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: 'Cross Format Test',
            UnifiedMetadataKey.ARTISTS: ['Test Artist'],
            UnifiedMetadataKey.ALBUM_NAME: 'Test Album'
        }
        
        sample_files = [
            (sample_mp3_file, "mp3"),
            (sample_flac_file, "flac"),
            (sample_wav_file, "wav")
        ]
        
        for file_path, format_type in sample_files:
            # Set basic metadata using external script
            basic_metadata = {
                "title": "Original Title",
                "artist": "Original Artist"
            }
            with TempFileWithMetadata(basic_metadata, format_type) as test_file:
                # Set metadata using app's function (this is what we're testing)
                update_metadata(test_file.path, test_metadata)
                
                # Verify metadata was set correctly
                metadata = get_unified_metadata(test_file.path)
                assert metadata.get(UnifiedMetadataKey.TITLE) == test_metadata[UnifiedMetadataKey.TITLE]
                assert metadata.get(UnifiedMetadataKey.ARTISTS) == test_metadata[UnifiedMetadataKey.ARTISTS]
                assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_metadata[UnifiedMetadataKey.ALBUM_NAME]