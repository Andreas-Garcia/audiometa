import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_full_metadata
)
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestMultipleEntriesVorbis:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["One", "Two", "Three"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_format_specific_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["One", "Two", "Three"])
            
            vorbis_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            artists = vorbis_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_full_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["One", "Two", "Three"])
            
            full_metadata = get_full_metadata(test_file.path)
            
            unified_artists = full_metadata['unified_metadata'].get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(unified_artists, list)
            assert len(unified_artists) == 3
            assert "One" in unified_artists
            assert "Two" in unified_artists
            assert "Three" in unified_artists
            
            vorbis_artists = full_metadata['format_metadata']['vorbis'].get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(vorbis_artists, list)
            assert len(vorbis_artists) == 3
            assert "One" in vorbis_artists
            assert "Two" in vorbis_artists
            assert "Three" in vorbis_artists

    def test_comment_field_returns_first_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_comments(["First comment", "Second comment", "Third comment"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            comments = unified_metadata.get(UnifiedMetadataKey.COMMENT)
            
            assert isinstance(comments, str)
            assert comments == "First comment"