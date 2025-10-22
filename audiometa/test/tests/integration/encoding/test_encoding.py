import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    update_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
from audiometa.test.helpers.id3v1 import ID3v1MetadataSetter


@pytest.mark.integration
class TestEncoding:

    def test_id3v2_3_encoding_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            metadata_dict = {
                UnifiedMetadataKey.TITLE: "Test Title with ASCII",
                UnifiedMetadataKey.ARTISTS: ["Artist Name"],
                UnifiedMetadataKey.ALBUM: "Album Name"
            }
            update_metadata(test_file.path, metadata_dict, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with ASCII"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist Name"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Name"

    def test_id3v2_4_utf8_encoding_support(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Test with Unicode characters that require UTF-8
            unicode_metadata = {
                UnifiedMetadataKey.TITLE: "Test 中文 العربية русский 🎵",
                UnifiedMetadataKey.ARTISTS: ["Artist 日本語 한국어"],
                UnifiedMetadataKey.ALBUM: "Album Ελληνικά ภาษาไทย"
            }
            
            update_metadata(test_file.path, unicode_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            # Verify the Unicode characters are preserved
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test 中文 العربية русский 🎵"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist 日本語 한국어"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Ελληνικά ภาษาไทย"

    def test_id3v1_encoding_support(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            metadata_dict = {
                UnifiedMetadataKey.TITLE: "Test Title with ASCII",
                UnifiedMetadataKey.ARTISTS: ["Artist Name"],
                UnifiedMetadataKey.ALBUM: "Album Name"
            }
            update_metadata(test_file.path, metadata_dict, metadata_format=MetadataFormat.ID3V1)
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with ASCII"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist Name"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Name"

    def test_riff_utf8_encoding_support(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Test with Unicode characters that require UTF-8
            unicode_metadata = {
                UnifiedMetadataKey.TITLE: "Test 中文 العربية русский 🎵",
                UnifiedMetadataKey.ARTISTS: ["Artist 日本語 한국어"],
                UnifiedMetadataKey.ALBUM: "Album Ελληνικά ภาษาไทย"
            }
            
            update_metadata(test_file.path, unicode_metadata, metadata_format=MetadataFormat.RIFF)
            
            # Verify the Unicode characters are preserved
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test 中文 العربية русский 🎵"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist 日本語 한국어"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Ελληνικά ภาษาไทย"

    def test_vorbis_utf8_encoding_support(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Test with Unicode characters that require UTF-8
            unicode_metadata = {
                UnifiedMetadataKey.TITLE: "Test 中文 العربية русский 🎵",
                UnifiedMetadataKey.ARTISTS: ["Artist 日本語 한국어"],
                UnifiedMetadataKey.ALBUM: "Album Ελληνικά ภาษาไทย"
            }
            
            update_metadata(test_file.path, unicode_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Verify the Unicode characters are preserved
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test 中文 العربية русский 🎵"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist 日本語 한국어"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Ελληνικά ภาษาไทย"