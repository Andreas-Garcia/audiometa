import pytest

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestRiffSeparators:
    def test_semicolon_separated_artists_single_chunk(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            # For RIFF, when we have a single chunk with separator-based values
            test_file.set_riff_separator_artists("Artist One;Artist Two;Artist Three")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_double_slash_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_separator_artists("Artist One//Artist Two//Artist Three")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_comma_separated_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_separator_genres("Rock,Alternative,Indie")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Alternative" in genres
            assert "Indie" in genres

    def test_mixed_separators_priority(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            # Test separator priority: // should be used first
            test_file.set_riff_separator_artists("Artist//One;Two,Three")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist" in artists
            assert "One;Two,Three" in artists  # Semicolon and comma preserved as part of artist name

    def test_single_artist_no_parsing_needed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_separator_artists("Single Artist Name")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 1
            assert "Single Artist Name" in artists

    def test_backslash_separated_composers(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_separator_composers("Composer A\\Composer B\\Composer C")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer A" in composers
            assert "Composer B" in composers
            assert "Composer C" in composers

    def test_album_artists_separator_parsing(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_separator_album_artists("Album Artist 1;Album Artist 2")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            album_artists = unified_metadata.get(UnifiedMetadataKey.ALBUM_ARTISTS_NAMES)
            
            assert isinstance(album_artists, list)
            assert len(album_artists) == 2
            assert "Album Artist 1" in album_artists
            assert "Album Artist 2" in album_artists