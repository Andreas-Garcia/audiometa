from audiometa import get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestId3v2_4MultipleEntries:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_4_multiple_artists(["Artist One", "Artist Two", "Artist Three"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_multiple_artists_format_specific_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_4_multiple_artists(["Artist One", "Artist Two"])
            
            id3v2_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_4)
            artists = id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists

    def test_multiple_album_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_multiple_album_artists(["Album Artist One", "Album Artist Two"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
            
            assert isinstance(album_artists, list)
            assert len(album_artists) == 2
            assert "Album Artist One" in album_artists
            assert "Album Artist Two" in album_artists

    def test_multiple_composers(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_multiple_composers(["Composer A", "Composer B", "Composer C"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer A" in composers
            assert "Composer B" in composers
            assert "Composer C" in composers

    def test_multiple_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_multiple_genres(["Rock", "Pop", "Jazz"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Pop" in genres
            assert "Jazz" in genres