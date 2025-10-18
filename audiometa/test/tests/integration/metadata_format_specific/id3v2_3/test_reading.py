
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v23Reading:

    def test_id3v2_3_extended_metadata(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Extended Test Title - This is a longer title than ID3v1 can handle",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2.3 Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.3 Test Album",
                UnifiedMetadataKey.YEAR: "2023"
            }
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Extended Test Title - This is a longer title than ID3v1 can handle"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2.3 Test Album"
            assert metadata.get(UnifiedMetadataKey.YEAR) == "2023"

    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Metadata Reading Test",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.GENRES_NAMES: "Electronic"
            }
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert isinstance(metadata, dict)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Metadata Reading Test"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == "Electronic"

    def test_single_format_id3v2_3_extraction(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Single Format Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Single Format Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Single Format Album"
            }
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            id3v2_3_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            assert isinstance(id3v2_3_metadata, dict)
            assert id3v2_3_metadata.get(UnifiedMetadataKey.TITLE) == "Single Format Test Title"
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Single Format Artist"]
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Single Format Album"

    def test_id3v2_3_version_specific_behavior(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Version Specific Test",
                UnifiedMetadataKey.YEAR: "2023"
            }
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            # Test that ID3v2.3 specific metadata is present
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            assert isinstance(metadata, dict)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Version Specific Test"
            assert metadata.get(UnifiedMetadataKey.YEAR) == "2023"
            
            # ID3v2.3 uses TYER for year instead of ID3v2.4's TDRC
            # This test verifies that the library correctly handles version differences
            if UnifiedMetadataKey.YEAR in metadata:
                assert isinstance(metadata[UnifiedMetadataKey.YEAR], str)

    def test_id3v2_3_multiple_artists_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            artists = ["Artist One", "Artist Two", "Artist Three"]
            test_file.set_id3v2_3_multiple_artists(artists)
            
            metadata = get_merged_unified_metadata(test_file.path)
            retrieved_artists = metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(retrieved_artists, list)
            assert len(retrieved_artists) == 3
            assert all(artist in retrieved_artists for artist in artists)

    def test_id3v2_3_error_handling(self, temp_audio_file: Path):
        # Test ID3v2.3 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2_3)

    def test_id3v2_3_with_other_formats(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # First set ID3v2.3 metadata
            id3v2_3_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2.3 Long Title That Exceeds ID3v1 Limits",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2.3 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2.3 Album"
            }
            update_file_metadata(test_file.path, id3v2_3_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            # Then add ID3v1 metadata
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Album"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Test that we can read both ID3v2.3 and ID3v1 metadata
            id3v2_3_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2_3)
            id3v1_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            # Verify ID3v2.3 metadata is present
            assert id3v2_3_metadata_result is not None
            assert id3v2_3_metadata_result.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"
            assert id3v2_3_metadata_result.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Artist"]
            assert id3v2_3_metadata_result.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2.3 Album"
            
            # Verify ID3v1 metadata is present
            assert id3v1_metadata_result is not None
            assert id3v1_metadata_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_metadata_result.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Artist"]
            assert id3v1_metadata_result.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v1 Album"
            
            # Test merged metadata (should prioritize ID3v2.3 over ID3v1)
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata is not None
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"

    def test_id3v2_3_encoding_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Título with Accénts",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artîst Namé"],
                UnifiedMetadataKey.ALBUM_NAME: "Albüm Naïme"
            }
            
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2_3)
            
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Título with Accénts"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Artîst Namé"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Albüm Naïme"