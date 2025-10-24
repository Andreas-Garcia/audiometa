from pathlib import Path

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleValuesDuplicateValues:
    def test_write_duplicate_values(self, temp_audio_file: Path):
        # Test with duplicate values
        duplicate_values = ["Artist One", "Artist Two", "Artist One", "Artist Three", "Artist Two"]
        metadata = {
            UnifiedMetadataKey.ARTISTS: duplicate_values
        }
        
        update_metadata(temp_audio_file, metadata)
        
        artists = get_unified_metadata_field(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        assert isinstance(artists, list)
        assert len(artists) == 5  # Duplicates should be preserved
        assert artists.count("Artist One") == 2
        assert artists.count("Artist Two") == 2
        assert artists.count("Artist Three") == 1
