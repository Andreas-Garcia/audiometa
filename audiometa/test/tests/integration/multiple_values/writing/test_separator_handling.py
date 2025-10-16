from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata
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
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
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
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist; with, mixed | separators / and \\ slashes" in artists
        assert "Another; Artist, with | mixed / separators \\ and \\ more" in artists
        assert "Complex // Artist \\ with, all; separators | mixed" in artists

    def test_write_multiple_values_with_separators_across_different_fields(self, temp_audio_file: Path):
        # Test separator handling across different multi-value fields
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist; with; semicolons", "Artist, with, commas"],
            UnifiedMetadataKey.COMPOSER: ["Composer / with / slashes", "Composer \\ with \\ backslashes"],
            UnifiedMetadataKey.MUSICIANS: ["Guitar; Lead: Alice", "Bass, Electric: Bob"],
            UnifiedMetadataKey.GENRE_NAME: ["Rock; Alternative", "Jazz, Fusion"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Verify each field preserves separators correctly
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist; with; semicolons" in artists
        assert "Artist, with, commas" in artists
        
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        assert isinstance(composers, list)
        assert len(composers) == 2
        assert "Composer / with / slashes" in composers
        assert "Composer \\ with \\ backslashes" in composers
        
        musicians = unified_metadata.get(UnifiedMetadataKey.MUSICIANS)
        assert isinstance(musicians, list)
        assert len(musicians) == 2
        assert "Guitar; Lead: Alice" in musicians
        assert "Bass, Electric: Bob" in musicians
        
        genres = unified_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        assert isinstance(genres, list)
        assert len(genres) == 2
        assert "Rock; Alternative" in genres
        assert "Jazz, Fusion" in genres
