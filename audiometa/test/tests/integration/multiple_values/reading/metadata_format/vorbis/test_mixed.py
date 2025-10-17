from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestVorbisMixed:
    def test_modern_format_multiple_entries_no_parsing(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist; with; semicolons", "Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist; with; semicolons" in artists
            assert "Artist Three" in artists

    def test_legacy_data_single_entry_parsed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One;Artist Two;Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({"title": "Single Title"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Artist One", "Artist Two"])
            test_file.set_vorbis_multiple_genres(["Rock", "Alternative"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists
            
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            assert isinstance(genres, list)
            assert len(genres) == 2
            assert "Rock" in genres
            assert "Alternative" in genres
            
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            assert isinstance(title, str)
            assert title == "Single Title"