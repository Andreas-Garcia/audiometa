from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestMultipleEntriesVorbis:
    def test_write_multiple_artists(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple artists using update_file_metadata
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read back using unified function
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_write_multiple_artists_vorbis_specific(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple artists to Vorbis format specifically
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Primary Artist", "Secondary Artist", "Featured Artist"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read back using Vorbis specific function
            vorbis_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            artists = vorbis_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Primary Artist" in artists
            assert "Secondary Artist" in artists
            assert "Featured Artist" in artists

    def test_write_multiple_album_artists(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple album artists
            metadata = {
                UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist One", "Album Artist Two"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read back using unified function
            unified_metadata = get_merged_unified_metadata(test_file.path)
            album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
            
            assert isinstance(album_artists, list)
            assert len(album_artists) == 2
            assert "Album Artist One" in album_artists
            assert "Album Artist Two" in album_artists

    def test_write_multiple_composers(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple composers
            metadata = {
                UnifiedMetadataKey.COMPOSERS_NAMES: ["Composer One", "Composer Two", "Composer Three"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read back using unified function
            unified_metadata = get_merged_unified_metadata(test_file.path)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSERS_NAMES)
            
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer One" in composers
            assert "Composer Two" in composers
            assert "Composer Three" in composers

    def test_write_multiple_genres(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple genres
            metadata = {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Pop", "Alternative"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read back using unified function
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Pop" in genres
            assert "Alternative" in genres

    def test_write_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write a mix of single and multiple values
            metadata = {
                UnifiedMetadataKey.TITLE: "Single Title",  # Single value
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"],  # Multiple values
                UnifiedMetadataKey.ALBUM_NAME: "Single Album",  # Single value
                UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Pop"]  # Multiple values
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read back using unified function
            unified_metadata = get_merged_unified_metadata(test_file.path)
            
            # Check single values
            assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Single Title"
            assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Single Album"
            
            # Check multiple values
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists
            
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            assert isinstance(genres, list)
            assert len(genres) == 2
            assert "Rock" in genres
            assert "Pop" in genres

    def test_write_empty_list_removes_field(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # First write some metadata
            initial_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Initial Artist"],
                UnifiedMetadataKey.GENRES_NAMES: ["Initial Genre"]
            }
            update_file_metadata(test_file.path, initial_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify it was written
            unified_metadata = get_merged_unified_metadata(test_file.path)
            assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Initial Artist"]
            assert unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Initial Genre"]
            
            # Now write empty lists to remove the fields
            empty_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: [],
                UnifiedMetadataKey.GENRES_NAMES: []
            }
            update_file_metadata(test_file.path, empty_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify fields were removed
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None
            assert updated_metadata.get(UnifiedMetadataKey.GENRES_NAMES) is None

    def test_write_none_removes_field(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # First write some metadata
            initial_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Initial Artist"],
                UnifiedMetadataKey.GENRES_NAMES: ["Initial Genre"]
            }
            update_file_metadata(test_file.path, initial_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify it was written
            unified_metadata = get_merged_unified_metadata(test_file.path)
            assert unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Initial Artist"]
            assert unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Initial Genre"]
            
            # Now write None to remove the fields
            none_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: None,
                UnifiedMetadataKey.GENRES_NAMES: None
            }
            update_file_metadata(test_file.path, none_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify fields were removed
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None
            assert updated_metadata.get(UnifiedMetadataKey.GENRES_NAMES) is None