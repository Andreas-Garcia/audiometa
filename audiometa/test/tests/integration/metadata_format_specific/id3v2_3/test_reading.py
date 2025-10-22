
import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter


@pytest.mark.integration
class TestId3v23Reading:

    def test_id3v2_3_extended_metadata(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("ID3v2.3 Extended Test Title - This is a longer title than ID3v1 can handle")
            test_file.set_id3v2_artist("ID3v2.3 Test Artist")
            test_file.set_id3v2_album("ID3v2.3 Test Album")
            test_file.set_id3v2_genre("Electronic")
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Extended Test Title - This is a longer title than ID3v1 can handle"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["ID3v2.3 Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "ID3v2.3 Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Electronic"]

    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("ID3v2.3 Metadata Reading Test")
            test_file.set_id3v2_artist("Test Artist")
            test_file.set_id3v2_album("Test Album")
            test_file.set_id3v2_genre("Electronic")
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(metadata, dict)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Metadata Reading Test"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Electronic"]

    def test_single_format_id3v2_3_extraction(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("Single Format Test Title")
            test_file.set_id3v2_artist("Single Format Artist")
            test_file.set_id3v2_album("Single Format Album")
            
            id3v2_3_metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(id3v2_3_metadata, dict)
            assert id3v2_3_metadata.get(UnifiedMetadataKey.TITLE) == "Single Format Test Title"
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ARTISTS) == ["Single Format Artist"]
            assert id3v2_3_metadata.get(UnifiedMetadataKey.ALBUM) == "Single Format Album"

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
            id3v2_3_metadata_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            id3v1_metadata_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            
            # Verify ID3v2.3 metadata is present
            assert id3v2_3_metadata_result is not None
            assert id3v2_3_metadata_result.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"
            assert id3v2_3_metadata_result.get(UnifiedMetadataKey.ARTISTS) == ["ID3v2.3 Artist"]
            assert id3v2_3_metadata_result.get(UnifiedMetadataKey.ALBUM) == "ID3v2.3 Album"
            
            # Verify ID3v1 metadata is present
            assert id3v1_metadata_result is not None
            assert id3v1_metadata_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v1_metadata_result.get(UnifiedMetadataKey.ARTISTS) == ["ID3v1 Artist"]
            assert id3v1_metadata_result.get(UnifiedMetadataKey.ALBUM) == "ID3v1 Album"
            
            # Test merged metadata (should prioritize ID3v2.3 over ID3v1)
            merged_metadata = get_unified_metadata(test_file.path)
            assert merged_metadata is not None
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"

    def test_id3v2_3_encoding_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            test_file.set_id3v2_title("Test Title with ASCII")
            test_file.set_id3v2_artist("Artist Name")
            test_file.set_id3v2_album("Album Name")
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with ASCII"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist Name"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Name"