"""
End-to-end tests for real user scenarios.

These tests simulate how actual users would interact with the library
in real-world applications.
"""
import pytest
from audiometa import AudioFile


@pytest.mark.e2e
class TestUserScenarios:
    """Test real-world user scenarios."""
    
    def test_music_library_organization(self, sample_files):
        """Test organizing a music library with metadata."""
        # Simulate a user organizing their music library
        
        for i, file_path in enumerate(sample_files[:3]):  # Test with first 3 files
            audio_file = AudioFile(file_path)
            
            # Set consistent metadata for organization
            audio_file.set_album("My Music Library")
            audio_file.set_year(2024)
            audio_file.set_genre("Various")
            
            # Set unique track info
            audio_file.set_track_number(i + 1)
            audio_file.set_title(f"Track {i + 1}")
            
            audio_file.save()
            
            # Verify the organization worked
            reloaded = AudioFile(file_path)
            assert reloaded.get_album() == "My Music Library"
            assert reloaded.get_track_number() == i + 1
    
    def test_metadata_import_export_workflow(self, sample_mp3_file):
        """Test importing and exporting metadata."""
        # Simulate a user importing metadata from external source
        
        # Export current metadata
        audio_file = AudioFile(sample_mp3_file)
        metadata = {
            'title': audio_file.get_title(),
            'artist': audio_file.get_artist(),
            'album': audio_file.get_album(),
            'year': audio_file.get_year(),
            'genre': audio_file.get_genre()
        }
        
        # Simulate external metadata update
        metadata['title'] = "Updated Title"
        metadata['artist'] = "Updated Artist"
        
        # Apply updated metadata
        audio_file.set_title(metadata['title'])
        audio_file.set_artist(metadata['artist'])
        audio_file.set_album(metadata['album'])
        audio_file.set_year(metadata['year'])
        audio_file.set_genre(metadata['genre'])
        audio_file.save()
        
        # Verify the import worked
        reloaded = AudioFile(sample_mp3_file)
        assert reloaded.get_title() == "Updated Title"
        assert reloaded.get_artist() == "Updated Artist"
    
    def test_cross_format_compatibility(self, sample_files):
        """Test metadata consistency across different audio formats."""
        # Test that metadata works consistently across MP3, FLAC, etc.
        
        test_metadata = {
            'title': 'Cross Format Test',
            'artist': 'Test Artist',
            'album': 'Test Album',
            'year': 2024,
            'genre': 'Test'
        }
        
        for file_path in sample_files:
            audio_file = AudioFile(file_path)
            
            # Set metadata
            audio_file.set_title(test_metadata['title'])
            audio_file.set_artist(test_metadata['artist'])
            audio_file.set_album(test_metadata['album'])
            audio_file.set_year(test_metadata['year'])
            audio_file.set_genre(test_metadata['genre'])
            audio_file.save()
            
            # Verify metadata was set correctly
            reloaded = AudioFile(file_path)
            assert reloaded.get_title() == test_metadata['title']
            assert reloaded.get_artist() == test_metadata['artist']
            assert reloaded.get_album() == test_metadata['album']
            assert reloaded.get_year() == test_metadata['year']
            assert reloaded.get_genre() == test_metadata['genre']
