import pytest

from audiometa import get_specific_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v1.id3v1_metadata_setter import ID3v1MetadataSetter
from audiometa.test.helpers.id3v1.id3v1_metadata_getter import ID3v1MetadataGetter
from audiometa.test.helpers.id3v2.id3v2_header_verifier import ID3v2HeaderVerifier


@pytest.mark.integration
class TestMp3Reading:
    def test_id3v1_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            ID3v1MetadataSetter.set_title(test_file.path, "Title ID3v1")

            title = get_specific_metadata(file=test_file.path, metadata_format=MetadataFormat.ID3V1, unified_metadata_key=UnifiedMetadataKey.TITLE)
            assert title == "Title ID3v1"
            
    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Title ID3v2.3"}
            ID3v2MetadataSetter.set_metadata(test_file.path, metadata, version='2.3')
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)

            title = get_specific_metadata(file=test_file.path, metadata_format=MetadataFormat.ID3V2, unified_metadata_key=UnifiedMetadataKey.TITLE)
            assert title == "Title ID3v2.3"
            
    def test_id3v2_4_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Title ID3v2.4"}
            ID3v2MetadataSetter.set_metadata(test_file.path, metadata, version='2.4')
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)

            title = get_specific_metadata(file=test_file.path, metadata_format=MetadataFormat.ID3V2, unified_metadata_key=UnifiedMetadataKey.TITLE)
            assert title == "Title ID3v2.4"