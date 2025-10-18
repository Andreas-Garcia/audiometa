import pytest

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestId3v23Separators:
    def test_semicolon_separated_artists_single_frame(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # For ID3v2.3, when we have a single frame with separator-based values
            test_file.set_id3v2_separator_artists("Artist One;Artist Two;Artist Three", version="2.3")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_double_slash_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_separator_artists("Artist One//Artist Two//Artist Three", version="2.3")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_comma_separated_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_separator_genres("Rock,Alternative,Indie", version="2.3")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Alternative" in genres
            assert "Indie" in genres

    def test_mixed_separators_priority(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Test separator priority: // should be used first
            test_file.set_id3v2_separator_artists("Artist//One;Two,Three", version="2.3")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist" in artists
            assert "One;Two,Three" in artists  # Semicolon and comma preserved as part of artist name

    def test_single_artist_no_parsing_needed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_separator_artists("Single Artist Name", version="2.3")
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 1
            assert "Single Artist Name" in artists