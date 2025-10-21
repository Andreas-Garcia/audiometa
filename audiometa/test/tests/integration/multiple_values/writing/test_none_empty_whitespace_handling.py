
from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestNoneEmptyWhitespaceHandling:
    def test_none_removes_fields(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: None
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None
        
    def test_write_empty_list_removes_field(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is not None
        
        # Now write empty list (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: []
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None

    def test_write_list_with_none_removes_field(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [None, None]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None

    def test_write_empty_strings_in_list(self, temp_audio_file: Path):
        # Write list with empty strings
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["", "Valid Artist", ""]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty strings
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Valid Artist" in artists

    def test_write_whitespace_only_strings(self, temp_audio_file: Path):
        # Write list with whitespace-only strings
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["   ", "Valid Artist", "\t\n"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out whitespace-only strings
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Valid Artist" in artists

    def test_write_mixed_empty_and_valid_entries(self, temp_audio_file: Path):
        # Write list with mix of empty, whitespace, and valid entries
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["", "   ", "Valid Artist 1", "\t", "Valid Artist 2", "\n"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty and whitespace-only strings
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Valid Artist 1" in artists
        assert "Valid Artist 2" in artists

    def test_write_all_empty_strings_removes_field(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["", "   ", "\t\n"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert artists == None

    def test_write_single_empty_string_removes_field(self, temp_audio_file: Path):
        # Write single empty string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [""]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should remove the field entirely (None for single empty string)
        assert artists is None

    def test_write_single_whitespace_string_removes_field(self, temp_audio_file: Path):
        # Write single whitespace string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["   "]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None

    def test_write_trimmed_whitespace_preserved(self, temp_audio_file: Path):
        # Write strings with leading/trailing whitespace that should be preserved
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["  Artist with spaces  ", "Another Artist"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        artists = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Whitespace is trimmed by the implementation
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist with spaces" in artists
        assert "Another Artist" in artists

    def test_write_empty_metadata_dict(self, temp_audio_file: Path):
        # Write empty metadata dictionary
        metadata = {}
        update_file_metadata(temp_audio_file, metadata)
        
        # Should not raise an error
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert isinstance(unified_metadata, dict)

    def test_write_metadata_with_all_none_values(self, temp_audio_file: Path):
        # Write metadata with all None values
        metadata = {
            UnifiedMetadataKey.TITLE: None,
            UnifiedMetadataKey.ARTISTS_NAMES: None,
            UnifiedMetadataKey.ALBUM_NAME: None
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Should not raise an error
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert isinstance(unified_metadata, dict)
