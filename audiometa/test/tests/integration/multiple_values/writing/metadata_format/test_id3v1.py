
from audiometa import update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v1.id3v1_metadata_inspector import ID3v1MetadataInspector
from audiometa.test.helpers.id3v1.id3v1_metadata_setter import ID3v1MetadataSetter


class TestMultipleEntriesId3v1:
    def test_id3v1_artists_concatenation(self):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Three"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Use helper to check the created ID3v1 artist field directly
            inspection = ID3v1MetadataInspector.inspect_artist_field(test_file.path)
            assert inspection['has_data']
            
            # Check that all artists are concatenated with separators
            artist_value = inspection['artist_value']
            assert "Artist One" in artist_value
            assert "Artist Two" in artist_value
            assert "Three" in artist_value
            assert inspection['contains_separators']
            
    
    def test_with_existing_artists_field(self):
        # Start with an existing artist field
        initial_metadata = {"artist": "Existing Artist"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            ID3v1MetadataSetter.set_artist(test_file.path, "Existing 1; Existing 2")
            assert ID3v1MetadataInspector.inspect_artist_field(test_file.path)['has_data']
            
            # Now update with multiple artists
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Existing 1", "New 2"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            inspection = ID3v1MetadataInspector.inspect_artist_field(test_file.path)
            assert inspection['has_data']
            artist_value = inspection['artist_value']
            assert "Existing 1" in artist_value
            assert "New 2" in artist_value
            assert inspection['contains_separators']