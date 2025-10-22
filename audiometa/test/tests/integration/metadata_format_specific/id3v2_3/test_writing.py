"""Tests for ID3v2.3 format writing functionality.

This module tests the ID3v2.3-specific writing capabilities, including
version-specific features, encoding support, and compatibility with other formats.
"""

import pytest

from audiometa import (
    get_unified_metadata,
    get_specific_metadata,
    update_metadata
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
                UnifiedMetadataKey.ARTISTS: ["Test Artist ID3v2.3"],
                UnifiedMetadataKey.ALBUM: "Test Album ID3v2.3",
            }
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title ID3v2.3"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist ID3v2.3"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album ID3v2.3"

    def test_multiple_metadata_reading(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Song Title",
                UnifiedMetadataKey.ARTISTS: ["Test Artist"],
                UnifiedMetadataKey.ALBUM: "Test Album",
            }
            
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path)
            
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album"

    def test_multiple_metadata_writing(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Written Song Title",
                UnifiedMetadataKey.ARTISTS: ["Written Artist"],
                UnifiedMetadataKey.ALBUM: "Written Album",
            }
            
            update_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path)
            
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Written Song Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Written Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Written Album"

    def test_none_field_removal_id3v2_3(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            initial_metadata = {
                UnifiedMetadataKey.TITLE: "Test ID3v2.3 Title",
                UnifiedMetadataKey.ARTISTS: ["Test ID3v2.3 Artist"],
                UnifiedMetadataKey.ALBUM: "Test ID3v2.3 Album"
            }
            update_metadata(test_file.path, initial_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test ID3v2.3 Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test ID3v2.3 Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test ID3v2.3 Album"
            
            none_metadata = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.ARTISTS: ["Test ID3v2.3 Artist"],  # Keep this field
                UnifiedMetadataKey.ALBUM: None  # Remove this field
            }
            update_metadata(test_file.path, none_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            updated_metadata = get_unified_metadata(test_file.path)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM) is None
            
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test ID3v2.3 Artist"]
            
            id3v2_3_metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_3_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ALBUM) is None

    def test_none_vs_empty_string_behavior_id3v2_3(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field in ID3v2.3
            
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # None removes field
            
            update_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is None  # Empty string removes field in ID3v2.3

    def test_id3v2_3_encoding_behavior(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            special_metadata = {
                UnifiedMetadataKey.TITLE: "Tëst Ñamé with Spëcîal Charâcters",
                UnifiedMetadataKey.ARTISTS: ["Artîst with Åccénts"],
                UnifiedMetadataKey.ALBUM: "Albüm Naïme Tést"
            }
            
            update_metadata(test_file.path, special_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Tëst Ñamé with Spëcîal Charâcters"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artîst with Åccénts"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Albüm Naïme Tést"

    def test_id3v2_3_multiple_artists_writing(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            multiple_artists_metadata = {
                UnifiedMetadataKey.ARTISTS: ["Artist One", "Artist Two", "Artist Three"],
                UnifiedMetadataKey.TITLE: "Multi-Artist Song"
            }
            
            update_metadata(test_file.path, multiple_artists_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) == 3
            assert "Artist One" in retrieved_artists
            assert "Artist Two" in retrieved_artists
            assert "Artist Three" in retrieved_artists

    def test_id3v2_3_compatibility_with_other_formats(self, temp_audio_file):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            id3v2_3_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v2.3 Artist"],
                UnifiedMetadataKey.ALBUM: "ID3v2.3 Album"
            }
            update_metadata(test_file.path, id3v2_3_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM: "ID3v1 Album"
            }
            update_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            id3v2_3_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            id3v1_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            
            assert id3v2_3_result.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Title"
            assert id3v2_3_result.get(UnifiedMetadataKey.ARTISTS) == ["ID3v2.3 Artist"]
            
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_result.get(UnifiedMetadataKey.ARTISTS) == ["ID3v1 Artist"]
            
            merged_metadata = get_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS) == ["ID3v2.3 Artist"]