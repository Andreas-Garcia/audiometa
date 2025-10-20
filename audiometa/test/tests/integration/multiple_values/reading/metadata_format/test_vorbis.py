import pytest

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_full_metadata,
    get_specific_metadata
)
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.vorbis import VorbisMetadataSetter
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from test.tests.integration.per_metadata import artists


class TestVorbis:
    def test_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3", "Artist 4"])
            verification = test_file.verify_vorbis_multiple_entries_in_raw_data("ARTIST", expected_count=3)
            
            assert "ARTIST=Artist 1;Artist" in verification['raw_output'] 
            assert "ARTIST=Artist 3" in verification['raw_output']
            assert "ARTIST=Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists


class TestVorbisMultipleEntries:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_artists(test_file.path, ["One", "Two", "Three"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_format_specific_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            VorbisMetadataSetter.set_multiple_artists(test_file.path, ["One", "Two", "Three"])
            
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


    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_artists(["Artist One;Artist Two;Artist Three"])
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            

    def test_comment_field_returns_first_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_multiple_comments(["First comment", "Second comment", "Third comment"])

            comment = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT, metadata_format=MetadataFormat.VORBIS)
            assert isinstance(comment, str)
            assert comment == "First comment"