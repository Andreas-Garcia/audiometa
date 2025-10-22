
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

    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.3 Metadata Reading Test")
            ID3v2MetadataSetter.set_artist(test_file.path, "Test Artist", version="2.3")
            ID3v2MetadataSetter.set_album(test_file.path, "Test Album")
            ID3v2MetadataSetter.set_genre(test_file.path, "Electronic")
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(metadata, dict)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Metadata Reading Test"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.GENRES_NAMES) == ["Electronic"]

    def test_id3v2_3_encoding_support(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            ID3v2MetadataSetter.set_title(test_file.path, "Test Title with ASCII")
            ID3v2MetadataSetter.set_artist(test_file.path, "Artist Name", version="2.3")
            ID3v2MetadataSetter.set_album(test_file.path, "Album Name")
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with ASCII"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Artist Name"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Album Name"