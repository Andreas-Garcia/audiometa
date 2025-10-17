import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesId3v2:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["Artist One", "Artist Two", "Artist Three"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_multiple_artists_format_specific_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["Artist One", "Artist Two"])
            
            id3v2_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            artists = id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists

    def test_id3v2_vs_id3v1_precedence(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v2_multiple_artists(["ID3v2 Artist One", "ID3v2 Artist Two"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "ID3v2 Artist One" in artists
            assert "ID3v2 Artist Two" in artists
            assert "ID3v1 Artist" not in artists
