from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_inspector import ID3v2MetadataInspector
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter


class TestMultipleEntriesId3v2_4:
    def test_write_multiple_artists_id3v2_4(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        # Use helper to check the created ID3v2 frame directly
        verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(temp_audio_file, "TPE1")
        assert verification['success']
        # In ID3v2.4, multiple artists should be in a single frame with null separators (per spec)
        raw_output = verification['raw_output']
        assert "Artist One" in raw_output
        assert "Artist Two" in raw_output  
        assert "Artist Three" in raw_output
        # Should be one TPE1 frame with multiple values, displayed as separated values
        assert "TPE1=" in raw_output
        
        # Also verify unified metadata reading
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
        
        # Use helper to check the created ID3v2 frame directly
        verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(temp_audio_file, "TPE2")
        assert verification['success']
        raw_output = verification['raw_output']
        assert "Album Artist One" in raw_output
        assert "Album Artist Two" in raw_output
        # Should have 1 TPE2 frame with multiple values (ID3v2.4 spec)
        assert "TPE2=" in raw_output
        
        # Also verify unified metadata reading
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
        
        # Use helper to check the created ID3v2 frame directly
        verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(temp_audio_file, "TCOM")
        assert verification['success']
        raw_output = verification['raw_output']
        assert "Composer A" in raw_output
        assert "Composer B" in raw_output
        assert "Composer C" in raw_output
        # Should have 1 TCOM frame with multiple values (ID3v2.4 spec)
        assert "TCOM=" in raw_output
        
        # Also verify unified metadata reading
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSERS)
        
        assert isinstance(composers, list)
        assert len(composers) == 3
        assert "Composer A" in composers
        assert "Composer B" in composers
        assert "Composer C" in composers
    
    def test_id3v2_4_artists_single_frame_with_multiple_values(self):
        """Test that ID3v2.4 creates single frame with null-separated values for artists (per spec)."""
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "id3v2.4") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2", "Artist 3"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            # Use helper to check the created ID3v2 frame directly
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TPE1")
            assert verification['success']
            
            # Check that all artists are in the frame data (ID3v2.4 spec: single frame with null-separated values)
            raw_output = verification['raw_output']
            assert "Artist 1" in raw_output
            assert "Artist 2" in raw_output
            assert "Artist 3" in raw_output
            # Should have one TPE1 frame entry
            assert "TPE1=" in raw_output

    def test_id3v2_4_genres_single_frame_with_multiple_values(self):
        """Test that ID3v2.4 creates single frame with null-separated values for genres (per spec)."""
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "id3v2.4") as test_file:
            metadata = {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Pop", "Alternative"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            # Use helper to check the created ID3v2 frame directly
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TCON")
            assert verification['success']
            
            # Check that all genres are in the frame data (ID3v2.4 spec: single frame with null-separated values)
            raw_output = verification['raw_output']
            assert "Rock" in raw_output
            assert "Pop" in raw_output
            assert "Alternative" in raw_output
            # Should have one TCON frame entry
            assert "TCON=" in raw_output