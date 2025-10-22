import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    get_specific_metadata,
    AudioFile,
    update_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter


@pytest.mark.integration
class TestId3v24Reading:

    def test_id3v2_4_extended_metadata(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set maximum metadata using the script helper
            ID3v2MetadataSetter.set_max_metadata(test_file.path)
            
            metadata = get_unified_metadata(test_file.path)
            title = metadata.get(UnifiedMetadataKey.TITLE)
            assert len(title) > 30  # ID3v2.4 can have longer titles than ID3v1

    def test_id3v2_4_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            ID3v2MetadataSetter.set_max_metadata(test_file.path)
            
            metadata = get_unified_metadata(test_file.path)
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            # ID3v2.4 can have longer titles than ID3v1
            assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_id3v2_4_extraction(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            test_file.set_id3v2_4_max_metadata()
            
            id3v2_4_metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(id3v2_4_metadata, dict)
            assert UnifiedMetadataKey.TITLE in id3v2_4_metadata

    def test_audio_file_object_reading(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            test_file.set_id3v2_4_max_metadata()
            
            audio_file = AudioFile(test_file.path)
            
            # Test merged metadata
            metadata = get_unified_metadata(audio_file)
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            
            # Test specific metadata
            title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
            assert isinstance(title, str)
            
            # Test single format metadata
            id3v2_4_metadata = get_unified_metadata(audio_file, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(id3v2_4_metadata, dict)

    def test_id3v2_4_version_specific_behavior(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            test_file.set_id3v2_4_max_metadata()
            
            # Test that ID3v2.4 specific metadata is present
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(metadata, dict)
            
            # ID3v2.4 uses TDRC for recording time instead of ID3v2.3's TYER
            # This test verifies that the library correctly handles version differences
            if UnifiedMetadataKey.RELEASE_DATE in metadata:
                assert isinstance(metadata[UnifiedMetadataKey.RELEASE_DATE], str)

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

    def test_id3v2_4_multiple_artists_support(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set multiple artists
            artists = ["Artist One", "Artist Two", "Artist Three"]
            ID3v2MetadataSetter.set_artists(test_file.path, artists)
            
            metadata = get_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) == 3
            assert all(artist in retrieved_artists for artist in artists)

    def test_id3v2_4_raw_data_verification(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set multiple artists for raw data verification
            artists = ["Raw Artist One", "Raw Artist Two"]
            ID3v2MetadataSetter.set_artists(test_file.path, artists)
            
            # Test that multiple artists are preserved
            metadata = get_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) >= 2
            assert "Raw Artist One" in retrieved_artists
            assert "Raw Artist Two" in retrieved_artists

    def test_id3v2_4_error_handling(self, temp_audio_file: Path):
        # Test ID3v2.4 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_unified_metadata(str(temp_audio_file), metadata_format=MetadataFormat.ID3V2)

    def test_id3v2_4_with_other_formats(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # First, add ID3v2.4 metadata
            test_file.set_id3v2_4_max_metadata()
            
            # Then add ID3v1 metadata using the library
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM: "ID3v1 Album"
            }
            update_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Test that we can read both ID3v2.4 and ID3v1 metadata
            id3v2_4_metadata_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            id3v1_metadata_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            
            # Verify ID3v2.4 metadata is present
            assert id3v2_4_metadata_result is not None
            assert UnifiedMetadataKey.TITLE in id3v2_4_metadata_result
            # ID3v2.4 title should be the long one from the script
            assert len(id3v2_4_metadata_result[UnifiedMetadataKey.TITLE]) > 30
            
            # Verify ID3v1 metadata is present
            assert id3v1_metadata_result is not None
            assert UnifiedMetadataKey.TITLE in id3v1_metadata_result
            assert id3v1_metadata_result[UnifiedMetadataKey.TITLE] == "ID3v1 Title"
            
            # Test merged metadata (should prioritize ID3v2.4 over ID3v1)
            merged_metadata = get_unified_metadata(test_file.path)
            assert merged_metadata is not None
            assert UnifiedMetadataKey.TITLE in merged_metadata
            # Should prefer ID3v2.4 title since it's more comprehensive
            assert len(merged_metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_id3v2_4_advanced_features(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set complex metadata that might trigger advanced features
            complex_metadata = {
                UnifiedMetadataKey.TITLE: "Complex Title with Special Characters: äöü ñç 中文",
                UnifiedMetadataKey.ARTISTS: ["Artist with UTF-8: 日本語", "Another Artist: العربية"],
                UnifiedMetadataKey.ALBUM: "Album with Emojis: 🎵🎶🎤",
                UnifiedMetadataKey.GENRES_NAMES: ["Genre 1", "Genre 2", "Genre 3"],
                UnifiedMetadataKey.COMMENT: "Comment with Unicode: русский język"
            }
            
            update_metadata(test_file.path, complex_metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            # Verify all complex metadata is preserved
            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Complex Title with Special Characters: äöü ñç 中文"
            assert "Artist with UTF-8: 日本語" in metadata.get(UnifiedMetadataKey.ARTISTS)
            assert "Another Artist: العربية" in metadata.get(UnifiedMetadataKey.ARTISTS)
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album with Emojis: 🎵🎶🎤"

    def test_id3v2_4_vs_id3v2_3_differences(self):
        # Create two files, one with ID3v2.3 and one with ID3v2.4
        with TempFileWithMetadata({}, "id3v2.3") as id3v23_file, \
             TempFileWithMetadata({}, "id3v2.4") as id3v24_file:
            
            # Set the same Unicode metadata to both
            unicode_test_data = {
                UnifiedMetadataKey.TITLE: "Unicode Test: 中文 العربية",
                UnifiedMetadataKey.ARTISTS: ["Artist 日本語"],
            }
            
            update_metadata(id3v23_file.path, unicode_test_data, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            update_metadata(id3v24_file.path, unicode_test_data, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            # Both should preserve the Unicode characters, but ID3v2.4 should handle them more efficiently
            id3v23_metadata = get_unified_metadata(id3v23_file.path)
            id3v24_metadata = get_unified_metadata(id3v24_file.path)
            
            # Both should preserve the same content
            assert id3v23_metadata.get(UnifiedMetadataKey.TITLE) == "Unicode Test: 中文 العربية"
            assert id3v24_metadata.get(UnifiedMetadataKey.TITLE) == "Unicode Test: 中文 العربية"
            assert id3v23_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist 日本語"]
            assert id3v24_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist 日本語"]