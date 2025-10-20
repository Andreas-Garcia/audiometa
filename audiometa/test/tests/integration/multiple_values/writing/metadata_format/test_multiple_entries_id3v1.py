from pathlib import Path

from audiometa import update_file_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestMultipleEntriesId3v1:
    def test_id3v1_artists_concatenation(self):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            
            id3v1_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, str)
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            assert ", " in artists or "," in artists

    def test_id3v1_concatenation_with_very_long_values(self):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            long_artists = ["A" * 14, "B" * 15, "C" * 15]
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: long_artists
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            
            id3v1_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            artists = id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert artists[0] == "A" * 14
            assert artists[1] == "B" * 15