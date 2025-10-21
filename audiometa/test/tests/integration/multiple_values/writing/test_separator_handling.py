from pathlib import Path

from audiometa import update_file_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestSeparatorHandling:
    def test_write_multiple_values_with_all_separator_types(self, temp_audio_file: Path):
        # Test all separator types that are recognized by the library
        # Based on METADATA_MULTI_VALUE_SEPARATORS = ("//", "\\\\", ";", "\\", "/", ",")
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [
                "Artist; with; semicolons",
                "Artist, with, commas", 
                "Artist / with / slashes",
                "Artist \\ with \\ backslashes",
                "Artist // with // double slashes",
                "Artist \\\\ with \\\\ double backslashes"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 6
        assert "Artist; with; semicolons" in artists
        assert "Artist, with, commas" in artists
        assert "Artist / with / slashes" in artists
        assert "Artist \\ with \\ backslashes" in artists
        assert "Artist // with // double slashes" in artists
        assert "Artist \\\\ with \\\\ double backslashes" in artists

    def test_write_multiple_values_with_mixed_separators(self, temp_audio_file: Path):
        # Test entries that contain multiple separator types within the same value
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [
                "Artist; with, mixed | separators / and \\ slashes",
                "Another; Artist, with | mixed / separators \\ and \\ more",
                "Complex // Artist \\ with, all; separators | mixed"
            ]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist; with, mixed | separators / and \\ slashes" in artists
        assert "Another; Artist, with | mixed / separators \\ and \\ more" in artists
        assert "Complex // Artist \\ with, all; separators | mixed" in artists

    def test_write_multiple_values_with_separators_across_different_fields(self, temp_audio_file: Path):
        # Test separator handling across different multi-value fields
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist; with; semicolons", "Artist, with, commas"],
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist; with; semicolons" in artists
        assert "Artist, with, commas" in artists