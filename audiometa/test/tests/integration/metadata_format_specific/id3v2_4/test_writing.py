"""Tests for ID3v2.4 format writing functionality.

This module tests the ID3v2.4-specific writing capabilities, including
UTF-8 encoding support, version-specific features, and compatibility with other formats.
"""

import pytest

from audiometa import (
    get_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v24Writing:

    def test_metadata_writing_mp3(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title ID3v2.4",
                UnifiedMetadataKey.ARTISTS: ["Test Artist ID3v2.4"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album ID3v2.4",
            }
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title ID3v2.4"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist ID3v2.4"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album ID3v2.4"

    def test_multiple_metadata_reading(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Song Title",
                UnifiedMetadataKey.ARTISTS: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            }
            
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            metadata = get_unified_metadata(test_file.path)
            
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_multiple_metadata_writing(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Written Song Title",
                UnifiedMetadataKey.ARTISTS: ["Written Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Written Album",
            }
            
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            metadata = get_unified_metadata(test_file.path)
            
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Written Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"

    def test_none_field_removal_id3v2_4(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            initial_metadata = {
                UnifiedMetadataKey.TITLE: "Test ID3v2.4 Title",
                UnifiedMetadataKey.ARTISTS: ["Test ID3v2.4 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test ID3v2.4 Album"
            }
            update_metadata(test_file.path, initial_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test ID3v2.4 Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test ID3v2.4 Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test ID3v2.4 Album"
            
            none_metadata = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.ARTISTS: ["Test ID3v2.4 Artist"],  # Keep this field
                UnifiedMetadataKey.ALBUM_NAME: None  # Remove this field
            }
            update_metadata(test_file.path, none_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            updated_metadata = get_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None
            
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test ID3v2.4 Artist"]
            
            id3v2_4_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_4_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_4_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None

    def test_none_vs_empty_string_behavior_id3v2_4(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field in ID3v2.4
            
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # None removes field
            
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field in ID3v2.4

    def test_id3v2_4_utf8_encoding_writing(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            unicode_metadata = {
                UnifiedMetadataKey.TITLE: "Test 中文 العربية русский 🎵",
                UnifiedMetadataKey.ARTISTS: ["Artist 日本語 한국어"],
                UnifiedMetadataKey.ALBUM_NAME: "Album Ελληνικά ภาษาไทย"
            }
            
            update_metadata(test_file.path, unicode_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test 中文 العربية русский 🎵"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist 日本語 한국어"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Album Ελληνικά ภาษาไทย"

    def test_id3v2_4_multiple_artists_writing(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            multiple_artists_metadata = {
                UnifiedMetadataKey.ARTISTS: ["Artist One", "Artist Two", "Artist Three"],
                UnifiedMetadataKey.TITLE: "Multi-Artist Song"
            }
            
            update_metadata(test_file.path, multiple_artists_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            metadata = get_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) == 3
            assert "Artist One" in retrieved_artists
            assert "Artist Two" in retrieved_artists
            assert "Artist Three" in retrieved_artists

    def test_id3v2_4_compatibility_with_other_formats(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            id3v2_4_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.4 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v2.4 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.4 Album"
            }
            update_metadata(test_file.path, id3v2_4_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Album"
            }
            update_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            id3v2_4_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            assert id3v2_4_result.get(UnifiedMetadataKey.TITLE) == "ID3v2.4 Title"
            assert id3v2_4_result.get(UnifiedMetadataKey.ARTISTS) == ["ID3v2.4 Artist"]
            
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_result.get(UnifiedMetadataKey.ARTISTS) == ["ID3v1 Artist"]
            
            merged_metadata = get_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.4 Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS) == ["ID3v2.4 Artist"]