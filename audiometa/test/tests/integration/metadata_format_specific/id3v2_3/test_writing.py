"""Tests for ID3v2.3 format writing functionality.

This module tests the ID3v2.3-specific writing capabilities, including
version-specific features, encoding support, and compatibility with other formats.
"""

import pytest

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v23Writing:

    def test_metadata_writing_mp3(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title ID3v2.3",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist ID3v2.3"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album ID3v2.3",
            }
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title ID3v2.3"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist ID3v2.3"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album ID3v2.3"

    def test_multiple_metadata_reading(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Song Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
            }
            
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_multiple_metadata_writing(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Written Song Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Written Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Written Album",
            }
            
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Written Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Written Album"

    def test_none_field_removal_id3v2_3(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            initial_metadata = {
                UnifiedMetadataKey.TITLE: "Test ID3v2.3 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test ID3v2.3 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test ID3v2.3 Album"
            }
            update_file_metadata(test_file.path, initial_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test ID3v2.3 Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test ID3v2.3 Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test ID3v2.3 Album"
            
            none_metadata = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test ID3v2.3 Artist"],  # Keep this field
                UnifiedMetadataKey.ALBUM_NAME: None  # Remove this field
            }
            update_file_metadata(test_file.path, none_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            updated_metadata = get_merged_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None
            
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test ID3v2.3 Artist"]
            
            id3v2_3_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            assert id3v2_3_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None

    def test_none_vs_empty_string_behavior_id3v2_3(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""}, metadata_format=MetadataFormat.ID3V2_3)
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field in ID3v2.3
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.ID3V2_3)
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # None removes field
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""}, metadata_format=MetadataFormat.ID3V2_3)
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field in ID3v2.3

    def test_id3v2_3_encoding_behavior(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            special_metadata = {
                UnifiedMetadataKey.TITLE: "Tëst Ñamé with Spëcîal Charâcters",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artîst with Åccénts"],
                UnifiedMetadataKey.ALBUM_NAME: "Albüm Naïme Tést"
            }
            
            update_file_metadata(test_file.path, special_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Tëst Ñamé with Spëcîal Charâcters"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Artîst with Åccénts"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Albüm Naïme Tést"

    def test_id3v2_3_multiple_artists_writing(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            multiple_artists_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"],
                UnifiedMetadataKey.TITLE: "Multi-Artist Song"
            }
            
            update_file_metadata(test_file.path, multiple_artists_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) == 3
            assert "Artist One" in retrieved_artists
            assert "Artist Two" in retrieved_artists
            assert "Artist Three" in retrieved_artists

    def test_id3v2_3_compatibility_with_other_formats(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            id3v2_3_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2.3 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.3 Album"
            }
            update_file_metadata(test_file.path, id3v2_3_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Album"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            id3v2_3_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            id3v1_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            assert id3v2_3_result.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Title"
            assert id3v2_3_result.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Artist"]
            
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_result.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Artist"]
            
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Artist"]