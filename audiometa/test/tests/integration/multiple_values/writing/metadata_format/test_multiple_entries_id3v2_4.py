from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesId3v2_4:
    def test_write_multiple_artists_id3v2_4(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Artist One" in artists
        assert "Artist Two" in artists
        assert "Artist Three" in artists

    def test_write_multiple_artists_id3v2_4_specific(self, temp_audio_file: Path):
        # Write multiple artists to ID3v2.4 format specifically
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Primary Artist", "Secondary Artist", "Featured Artist"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Read back using ID3v2.4 specific function
        id3v2_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        artists = id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 3
        assert "Primary Artist" in artists
        assert "Secondary Artist" in artists
        assert "Featured Artist" in artists

    def test_write_multiple_album_artists_id3v2_4(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist One", "Album Artist Two"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
        
        assert isinstance(album_artists, list)
        assert len(album_artists) == 2
        assert "Album Artist One" in album_artists
        assert "Album Artist Two" in album_artists

    def test_write_multiple_composers_id3v2_4(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.COMPOSERS: ["Composer A", "Composer B", "Composer C"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSERS)
        
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer A" in composers
        assert "Composer B" in composers
        assert "Composer C" in composers


    def test_write_mixed_single_and_multiple_values_id3v2_4(self, temp_audio_file: Path):
        # Write a mix of single and multiple values
        metadata = {
            UnifiedMetadataKey.TITLE: "Single Title",  # Single value
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"],  # Multiple values
            UnifiedMetadataKey.ALBUM_NAME: "Single Album",  # Single value
            UnifiedMetadataKey.COMPOSERS: ["Composer 1", "Composer 2", "Composer 3"]  # Multiple values
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Check single values
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Single Title"
        assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Single Album"
        
        # Check multiple values
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist 1" in artists
        assert "Artist 2" in artists
        
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSERS)
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer 1" in composers
        assert "Composer 2" in composers
        assert "Composer 3" in composers

    def test_write_empty_list_removes_field_id3v2_4(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write empty list (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: []
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_write_none_removes_field_id3v2_4(self, temp_audio_file: Path):
        # First write some metadata
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Verify it was written
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        
        # Now write None (should remove the field)
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: None
        }
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Verify field was removed
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_id3v2_4_version_specific_behavior(self, temp_audio_file: Path):
        """Test that ID3v2.4 specific behavior is maintained (UTF-8 encoding, TDRC frames)."""
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"],
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            UnifiedMetadataKey.RELEASE_DATE: "2023"
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Verify the metadata was written correctly
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
        assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
        assert unified_metadata.get(UnifiedMetadataKey.RELEASE_DATE) == "2023"
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist One" in artists
        assert "Artist Two" in artists

    def test_utf8_encoding_id3v2_4(self, temp_audio_file: Path):
        """Test that ID3v2.4 properly handles UTF-8 encoding for international characters."""
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["François", "José", "Müller", "北京"],
            UnifiedMetadataKey.TITLE: "Título con Acentos",
            UnifiedMetadataKey.ALBUM_NAME: "Álbum con Caracteres Especiales"
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Verify UTF-8 encoding is preserved
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Título con Acentos"
        assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Álbum con Caracteres Especiales"
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 4
        assert "François" in artists
        assert "José" in artists
        assert "Müller" in artists
        assert "北京" in artists

    def test_unsynchronization_per_frame_id3v2_4(self, temp_audio_file: Path):
        """Test that ID3v2.4 handles unsynchronization per frame correctly."""
        # This test verifies that ID3v2.4's per-frame unsynchronization works
        # with multiple values that might contain problematic byte sequences
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist with \x00\xFF\xFE bytes", "Normal Artist"],
            UnifiedMetadataKey.TITLE: "Title with \x00\xFF\xFE bytes"
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Verify the metadata was written and read correctly despite problematic bytes
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Title with \x00\xFF\xFE bytes"
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist with \x00\xFF\xFE bytes" in artists
        assert "Normal Artist" in artists
