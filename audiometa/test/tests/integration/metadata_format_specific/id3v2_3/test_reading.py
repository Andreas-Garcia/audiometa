
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v23Reading:

    def test_id3v2_3_extended_metadata(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("ID3v2.3 Extended Test Title - This is a longer title than ID3v1 can handle")
            test_file.set_id3v2_artist("ID3v2.3 Test Artist")
            test_file.set_id3v2_album("ID3v2.3 Test Album")
            test_file.set_id3v2_genre("Electronic")
            
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Extended Test Title - This is a longer title than ID3v1 can handle"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2.3 Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2.3 Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Electronic"]

    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("ID3v2.3 Metadata Reading Test")
            test_file.set_id3v2_artist("Test Artist")
            test_file.set_id3v2_album("Test Album")
            test_file.set_id3v2_genre("Electronic")
            
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert isinstance(metadata, dict)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Metadata Reading Test"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Electronic"]

    def test_single_format_id3v2_3_extraction(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("Single Format Test Title")
            test_file.set_id3v2_artist("Single Format Artist")
            test_file.set_id3v2_album("Single Format Album")
            
            id3v2_3_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert isinstance(id3v2_3_metadata, dict)
            assert id3v2_3_metadata.get(UnifiedMetadataKey.TITLE) == "Single Format Test Title"
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Single Format Artist"]
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Single Format Album"

    def test_id3v2_3_version_specific_behavior(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("Version Specific Test")
            test_file.set_id3v2_artist("Test Artist")
            test_file.set_id3v2_album("Test Album")
            test_file.set_id3v2_genre("Rock")
            
            # Test that ID3v2.3 specific metadata is present
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert isinstance(metadata, dict)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Version Specific Test"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Rock"]
            
            # ID3v2.3 uses TYER for year instead of ID3v2.4's TDRC
            # This test verifies that the library correctly handles basic ID3v2.3 metadata
            assert all(isinstance(value, (str, list)) for value in metadata.values() if value is not None)

    def test_id3v2_3_multiple_artists_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            artists = ["Artist One", "Artist Two", "Artist Three"]
            test_file.set_id3v2_3_multiple_artists(artists)
            
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
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
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)

    def test_id3v2_3_with_other_formats(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # First set ID3v2.3 metadata using external tools
            test_file.set_id3v2_title("ID3v2.3 Long Title That Exceeds ID3v1 Limits")
            test_file.set_id3v2_artist("ID3v2.3 Artist")
            test_file.set_id3v2_album("ID3v2.3 Album")
            
            # Then add ID3v1 metadata using external tools
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v1_album("ID3v1 Album")
            
            # Test that we can read both ID3v2.3 and ID3v1 metadata
            id3v2_3_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
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
            test_file.set_id3v2_title("Test Title with ASCII")
            test_file.set_id3v2_artist("Artist Name")
            test_file.set_id3v2_album("Album Name")
            
            metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with ASCII"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist Name"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Album Name"