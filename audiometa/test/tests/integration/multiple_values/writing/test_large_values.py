from pathlib import Path
import time

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleValuesBoundaryConditions:
    def test_write_maximum_multiple_values_per_field(self, temp_audio_file: Path):
        # Test with very large number of values per field
        max_values = 1000
        large_artist_list = [f"Artist {i:04d}" for i in range(max_values)]
        
        metadata = {
            UnifiedMetadataKey.ARTISTS: large_artist_list,
        }
        
        start_time = time.time()
        update_metadata(temp_audio_file, metadata)
        write_time = time.time() - start_time
        
        # Verify all values were written
        artists = get_unified_metadata_field(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        assert isinstance(artists, list)
        assert len(artists) == max_values
        
        # Performance should be reasonable
        assert write_time < 10.0, f"Write took too long: {write_time:.2f}s"

    def test_write_extremely_long_individual_values(self, temp_audio_file: Path):
        # Test with extremely long individual values
        very_long_string = "A" * 50000  # 50KB string
        metadata = {
            UnifiedMetadataKey.ARTISTS: [very_long_string, "Normal Artist"],
            UnifiedMetadataKey.COMMENT: very_long_string
        }
        
        update_metadata(temp_audio_file, metadata)
        
        artists = get_unified_metadata_field(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert very_long_string in artists

    def test_write_mixed_length_values(self, temp_audio_file: Path):
        # Test with mixed length values
        mixed_lengths = [
            "A",  # 1 character
            "AB",  # 2 characters
            "ABC",  # 3 characters
            "A" * 100,  # 100 characters
            "A" * 1000,  # 1000 characters
            "A" * 10000,  # 10000 characters
        ]
        metadata = {
            UnifiedMetadataKey.ARTISTS: mixed_lengths
        }
        
        update_metadata(temp_audio_file, metadata)
        
        artists = get_unified_metadata_field(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        assert isinstance(artists, list)
        assert len(artists) == 6
        for value in mixed_lengths:
            assert value in artists

    def test_write_very_large_metadata_dict(self, temp_audio_file: Path):
        # Test with very large metadata dictionary
        large_metadata = {}
        
        # Add multiple values for each supported multiple-value field
        for i in range(100):
            large_metadata[UnifiedMetadataKey.ARTISTS] = [f"Artist {i:04d}" for i in range(50)]        
        start_time = time.time()
        update_metadata(temp_audio_file, large_metadata)
        write_time = time.time() - start_time
        
        artists = get_unified_metadata_field(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        assert isinstance(artists, list)
        assert len(artists) == 50
        
        # Performance should be reasonable
        assert write_time < 15.0, f"Write took too long: {write_time:.2f}s"