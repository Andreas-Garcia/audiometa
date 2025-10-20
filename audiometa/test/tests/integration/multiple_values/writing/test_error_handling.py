from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleValuesErrorHandling:
    def test_write_invalid_data_types_in_list(self, temp_audio_file: Path):
        # Test with invalid data types in multiple value lists
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [1, 2, 3]  # Numbers instead of strings
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Should convert numbers to strings
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "1" in artists
        assert "2" in artists
        assert "3" in artists

    def test_write_mixed_data_types_in_list(self, temp_audio_file: Path):
        # Test with mixed data types in multiple value lists
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", 123, None, "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Should filter out None values and convert others to strings
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3  # None is filtered out
        assert "Artist One" in artists
        assert "123" in artists
        assert "Artist Two" in artists

    def test_write_none_values_in_list(self, temp_audio_file: Path):
        # Test with None values in multiple value lists
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", None, "Artist Two", None]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Should filter out None values
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist One" in artists
        assert "Artist Two" in artists

    def test_write_very_large_metadata_dict(self, temp_audio_file: Path):
        # Test writing very large metadata dictionary
        large_metadata = {}
        
        # Create a very large list for each multi-value field
        for i in range(1000):
            large_metadata[UnifiedMetadataKey.ARTISTS_NAMES] = [f"Artist {i:04d}" for i in range(100)]
            large_metadata[UnifiedMetadataKey.COMPOSERS] = [f"Composer {i:04d}" for i in range(100)]
            large_metadata[UnifiedMetadataKey.MUSICIANS] = [f"Musician {i:04d}" for i in range(100)]
        
        # Should handle large metadata gracefully
        update_file_metadata(temp_audio_file, large_metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert isinstance(unified_metadata, dict)

    def test_write_metadata_with_very_long_strings(self, temp_audio_file: Path):
        # Test writing metadata with very long strings
        very_long_string = "A" * 100000  # 100KB string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [very_long_string, "Normal Artist"],
            UnifiedMetadataKey.COMMENT: very_long_string
        }
        
        # Should handle long strings gracefully
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert very_long_string in artists

    def test_write_metadata_with_unicode_edge_cases(self, temp_audio_file: Path):
        # Test writing metadata with Unicode edge cases
        unicode_values = [
            "Artist with emoji 🎵🎶",
            "Artist with accents: José María",
            "Artist with Chinese: 艺术家",
            "Artist with Arabic: فنان",
            "Artist with mixed: José 🎵 艺术家 فنان"
        ]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: unicode_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 5
        for unicode_artist in unicode_values:
            assert unicode_artist in artists

    def test_write_metadata_with_empty_strings_mixed(self, temp_audio_file: Path):
        # Test writing metadata with mixed empty and valid strings
        mixed_values = ["", "Valid Artist", "", "Another Valid Artist", ""]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: mixed_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2  # Should filter out empty strings
        assert "Valid Artist" in artists
        assert "Another Valid Artist" in artists

