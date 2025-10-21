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
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Use helper to check the created ID3v1 artist field directly
            inspection = ID3v1MetadataInspector.inspect_raw_field(test_file.path, 'artist')
            raw_output = inspection['raw_output']
            assert "Artist 1;Artist 2" in raw_output or "Artist 2;Artist 1" in raw_output
            
    
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
    
    def test_id3v1_separator_priority(self):
        # Each test case: values, expected separator
        test_cases = [
            (['A1', 'A2', 'A3'], ','),
            (['A,1', 'A2', 'A3'], ';'),
            (['A,1', 'A;2', 'A3'], '|'),
            (['A,1', 'A;2', 'A|3'], '·'),
            (['A,1', 'A;2', 'A|3', 'A·4'], '/'),
            (['A,1', 'A;2', 'A|3', 'A·4', 'A/5'], ','),
        ]
        for values, expected_sep in test_cases:
            initial_metadata = {"title": "Test Song"}
            with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
                metadata = {
                    UnifiedMetadataKey.ARTISTS_NAMES: values
                }
                update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
                inspection = ID3v1MetadataInspector.inspect_artist_field(test_file.path)
                assert inspection['has_data']
                artist_value = inspection['artist_value']
                # Check that the expected separator is used
                assert expected_sep in artist_value
                # Check that all values are present as substrings
                for v in values:
                    assert v in artist_value