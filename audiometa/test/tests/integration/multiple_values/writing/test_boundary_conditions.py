from pathlib import Path
import time

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleValuesBoundaryConditions:
    def test_write_maximum_multiple_values_per_field(self, temp_audio_file: Path):
        # Test with very large number of values per field
        max_values = 1000
        large_artist_list = [f"Artist {i:04d}" for i in range(max_values)]
        large_composer_list = [f"Composer {i:04d}" for i in range(max_values)]
        
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: large_artist_list,
            UnifiedMetadataKey.COMPOSERS: large_composer_list
        }
        
        start_time = time.time()
        update_file_metadata(temp_audio_file, metadata)
        write_time = time.time() - start_time
        
        # Verify all values were written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSERS)
        
        assert isinstance(artists, list)
        assert len(artists) == max_values
        assert isinstance(composers, list)
        assert len(composers) == max_values
        
        # Performance should be reasonable
        assert write_time < 10.0, f"Write took too long: {write_time:.2f}s"

    def test_write_extremely_long_individual_values(self, temp_audio_file: Path):
        # Test with extremely long individual values
        very_long_string = "A" * 50000  # 50KB string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [very_long_string, "Normal Artist"],
            UnifiedMetadataKey.COMMENT: very_long_string
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        comment = unified_metadata.get(UnifiedMetadataKey.COMMENT)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert very_long_string in artists
        assert comment == very_long_string

    def test_write_single_character_values(self, temp_audio_file: Path):
        # Test with single character values
        single_chars = ["A", "B", "C", "1", "2", "3", "!", "@", "#"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: single_chars
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 9
        for char in single_chars:
            assert char in artists

    def test_write_very_short_list(self, temp_audio_file: Path):
        # Test with very short list (single element)
        single_artist = ["Single Artist"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: single_artist
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Single Artist" in artists

    def test_write_duplicate_values(self, temp_audio_file: Path):
        # Test with duplicate values
        duplicate_values = ["Artist One", "Artist Two", "Artist One", "Artist Three", "Artist Two"]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: duplicate_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 5  # Duplicates should be preserved
        assert artists.count("Artist One") == 2
        assert artists.count("Artist Two") == 2
        assert artists.count("Artist Three") == 1

    def test_write_all_empty_strings(self, temp_audio_file: Path):
        # Test with all empty strings
        empty_values = ["", "", "", ""]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: empty_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should remove the field entirely
        assert artists is None

    def test_write_all_whitespace_strings(self, temp_audio_file: Path):
        # Test with all whitespace strings
        whitespace_values = ["   ", "\t\t\t", "\n\n\n", "   \t\n   "]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: whitespace_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should remove the field entirely
        assert artists is None

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
            UnifiedMetadataKey.ARTISTS_NAMES: mixed_lengths
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 6
        for value in mixed_lengths:
            assert value in artists

    def test_write_very_large_metadata_dict(self, temp_audio_file: Path):
        # Test with very large metadata dictionary
        large_metadata = {}
        
        # Add multiple values for each supported multiple-value field
        for i in range(100):
            large_metadata[UnifiedMetadataKey.ARTISTS_NAMES] = [f"Artist {i:04d}" for i in range(50)]
            large_metadata[UnifiedMetadataKey.ALBUM_ARTISTS_NAMES] = [f"Album Artist {i:04d}" for i in range(50)]
            large_metadata[UnifiedMetadataKey.COMPOSERS] = [f"Composer {i:04d}" for i in range(50)]
            large_metadata[UnifiedMetadataKey.INVOLVED_PEOPLE] = [f"Person {i:04d}: Role {i:04d}" for i in range(50)]
            large_metadata[UnifiedMetadataKey.MUSICIANS] = [f"Musician {i:04d}: Instrument {i:04d}" for i in range(50)]
            large_metadata[UnifiedMetadataKey.KEYWORDS] = [f"keyword{i:04d}" for i in range(50)]
        
        start_time = time.time()
        update_file_metadata(temp_audio_file, large_metadata)
        write_time = time.time() - start_time
        
        # Verify all data was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Check multiple value fields
        for field in [UnifiedMetadataKey.ARTISTS_NAMES, UnifiedMetadataKey.ALBUM_ARTISTS_NAMES, 
                     UnifiedMetadataKey.COMPOSERS, UnifiedMetadataKey.INVOLVED_PEOPLE,
                     UnifiedMetadataKey.MUSICIANS, UnifiedMetadataKey.KEYWORDS]:
            values = unified_metadata.get(field)
            assert isinstance(values, list)
            assert len(values) == 50
        
        # Performance should be reasonable
        assert write_time < 15.0, f"Write took too long: {write_time:.2f}s"

    def test_write_metadata_with_special_boundary_values(self, temp_audio_file: Path):
        # Test with special boundary values
        boundary_values = [
            "",  # Empty string
            " ",  # Single space
            "\t",  # Single tab
            "\n",  # Single newline
            "\r",  # Single carriage return
            "\0",  # Null character
            "A" * 255,  # 255 characters (common limit)
            "A" * 256,  # 256 characters
            "A" * 1024,  # 1KB
            "A" * 10240,  # 10KB
        ]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: boundary_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty/whitespace values
        assert isinstance(artists, list)
        assert len(artists) == 7  # Should filter out empty, space, tab, newline, carriage return
        assert "A" * 255 in artists
        assert "A" * 256 in artists
        assert "A" * 1024 in artists
        assert "A" * 10240 in artists

    def test_write_metadata_with_unicode_boundary_values(self, temp_audio_file: Path):
        # Test with Unicode boundary values
        unicode_boundary_values = [
            "A",  # Single ASCII character
            "中",  # Single Chinese character
            "🎵",  # Single emoji
            "A" * 1000,  # 1000 ASCII characters
            "中" * 1000,  # 1000 Chinese characters
            "🎵" * 1000,  # 1000 emojis
            "A中🎵" * 1000,  # Mixed Unicode characters
        ]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: unicode_boundary_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 7
        for value in unicode_boundary_values:
            assert value in artists

    def test_write_metadata_with_separator_boundary_values(self, temp_audio_file: Path):
        # Test with separator boundary values
        separator_boundary_values = [
            "Artist;with;semicolons",
            "Artist,with,commas",
            "Artist|with|pipes",
            "Artist/with/slashes",
            "Artist\\with\\backslashes",
            "Artist//with//double//slashes",
            "Artist\\\\with\\\\double\\\\backslashes",
            "Artist;with,mixed|separators/and\\slashes",
        ]
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: separator_boundary_values
        }
        
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 8
        for value in separator_boundary_values:
            assert value in artists
