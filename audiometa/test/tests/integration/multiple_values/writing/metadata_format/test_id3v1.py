from pathlib import Path

from audiometa import update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v1.id3v1_metadata_inspector import ID3v1MetadataInspector


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

    def test_id3v1_concatenation_with_very_long_values(self):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            long_artists = ["A" * 14, "B" * 15, "C" * 15]
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: long_artists
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Use helper to check the created ID3v1 artist field directly
            inspection = ID3v1MetadataInspector.inspect_artist_field(test_file.path)
            assert inspection['success']
            assert inspection['has_data']
            
            # Check that the field is truncated due to 30-character limit
            assert inspection['is_truncated']
            artist_value = inspection['artist_value']
            # Should contain first two artists but not the third due to length constraint
            assert "A" * 14 in artist_value
            assert "B" * 15 in artist_value
            # The field should be exactly 30 characters (truncated)
            assert len(artist_value) == 30