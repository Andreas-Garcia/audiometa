import pytest

from audiometa import update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.riff.riff_metadata_getter import RIFFMetadataGetter
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.id3v2.id3v2_header_verifier import ID3v2HeaderVerifier


@pytest.mark.integration
class TestWavWriting:
    def test_riff_metadata_writing_wav(self, temp_wav_file):
        with TempFileWithMetadata({}, "wav") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title RIFF"}
            update_metadata(test_file.path, metadata, metadata_format=MetadataFormat.RIFF)
            
            title = RIFFMetadataGetter.get_title(test_file.path)
            assert title == "Test Title RIFF"

    def test_id3v2_3_metadata_writing_wav(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.3"}
            update_metadata(test_file.path, unified_metadata=metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)
            
            title = ID3v2MetadataGetter.get_title(test_file.path)
            assert title == "Test Title ID3v2.3"
            
    def test_id3v2_4_metadata_writing_wav(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.4"}
            update_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            title = ID3v2MetadataGetter.get_title(test_file.path)
            assert title == "Test Title ID3v2.4"