
from pathlib import Path

from audiometa import update_metadata, get_unified_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestNoneEmptyWhitespaceHandling:
    def test_none_removes_fields(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["Artist One", "Artist Two"]
        }
        update_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        assert artists is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS: None
        }
        update_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        assert artists is None
        
    def test_write_empty_list_removes_field(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["Artist One", "Artist Two"]
        }
        update_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        assert artists is not None
        
        # Now write empty list (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS: []
        }
        update_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        assert artists is None

    def test_write_empty_strings_in_list(self, temp_audio_file: Path):
        # Write list with empty strings
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["", "Valid Artist", ""]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        # Should filter out empty strings
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Valid Artist" in artists

    def test_write_whitespace_only_strings(self, temp_audio_file: Path):
        # Write list with whitespace-only strings
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["   ", "Valid Artist", "\t\n"]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        # Should filter out whitespace-only strings
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Valid Artist" in artists

    def test_write_mixed_empty_and_valid_entries(self, temp_audio_file: Path):
        # Write list with mix of empty, whitespace, and valid entries
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["", "   ", "Valid Artist 1", "\t", "Valid Artist 2", "\n"]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        # Should filter out empty and whitespace-only strings
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Valid Artist 1" in artists
        assert "Valid Artist 2" in artists

    def test_write_all_empty_strings_removes_field(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["", "   ", "\t\n"]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        assert artists == None

    def test_write_single_empty_string_removes_field(self, temp_audio_file: Path):
        # Write single empty string
        metadata = {
            UnifiedMetadataKey.ARTISTS: [""]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        # Should remove the field entirely (None for single empty string)
        assert artists is None

    def test_write_single_whitespace_string_removes_field(self, temp_audio_file: Path):
        # Write single whitespace string
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["   "]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        assert artists is None

    def test_write_trimmed_whitespace_preserved(self, temp_audio_file: Path):
        # Write strings with leading/trailing whitespace that should be preserved
        metadata = {
            UnifiedMetadataKey.ARTISTS: ["  Artist with spaces  ", "Another Artist"]
        }
        update_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS)
        
        # Whitespace is trimmed by the implementation
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist with spaces" in artists
        assert "Another Artist" in artists

    def test_write_empty_metadata_dict(self, temp_audio_file: Path):
        # Write empty metadata dictionary
        metadata = {}
        update_metadata(temp_audio_file, metadata)
        
        # Should not raise an error
        unified_metadata = get_unified_metadata(temp_audio_file)
        assert isinstance(unified_metadata, dict)

    def test_write_metadata_with_all_none_values(self, temp_audio_file: Path):
        # Write metadata with all None values
        metadata = {
            UnifiedMetadataKey.TITLE: None,
            UnifiedMetadataKey.ARTISTS: None,
            UnifiedMetadataKey.ALBUM: None
        }
        update_metadata(temp_audio_file, metadata)
        
        # Should not raise an error
        unified_metadata = get_unified_metadata(temp_audio_file)
        assert isinstance(unified_metadata, dict)
