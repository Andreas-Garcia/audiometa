import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestEmptyWhitespaceHandling:
    def test_write_empty_list_removes_field(self, sample_flac_file: Path, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write empty list (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: []
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_write_none_removes_field(self, sample_flac_file: Path, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: None
        }
        update_file_metadata(temp_audio_file, metadata)
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_write_empty_strings_in_list(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write list with empty strings
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["", "Valid Artist", ""]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty strings
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Valid Artist" in artists

    def test_write_whitespace_only_strings(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write list with whitespace-only strings
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["   ", "Valid Artist", "\t\n"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out whitespace-only strings
        assert isinstance(artists, list)
        assert len(artists) == 1
        assert "Valid Artist" in artists

    def test_write_mixed_empty_and_valid_entries(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write list with mix of empty, whitespace, and valid entries
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["", "   ", "Valid Artist 1", "\t", "Valid Artist 2", "\n"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should filter out empty and whitespace-only strings
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Valid Artist 1" in artists
        assert "Valid Artist 2" in artists

    def test_write_all_empty_strings_removes_field(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write list with all empty strings
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["", "   ", "\t\n"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should remove the field entirely
        assert artists is None

    def test_write_single_empty_string_removes_field(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write single empty string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [""]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should remove the field entirely
        assert artists is None

    def test_write_single_whitespace_string_removes_field(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write single whitespace string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["   "]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should remove the field entirely
        assert artists is None

    def test_write_trimmed_whitespace_preserved(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write strings with leading/trailing whitespace that should be preserved
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["  Artist with spaces  ", "Another Artist"]
        }
        update_file_metadata(temp_audio_file, metadata)
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        # Should preserve the whitespace
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "  Artist with spaces  " in artists
        assert "Another Artist" in artists

    def test_write_empty_metadata_dict(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write empty metadata dictionary
        metadata = {}
        update_file_metadata(temp_audio_file, metadata)
        
        # Should not raise an error
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert isinstance(unified_metadata, dict)

    def test_write_metadata_with_all_none_values(self, sample_flac_file: Path, temp_audio_file: Path):
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
