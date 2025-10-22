import pytest
from audiometa import get_unified_metadata, update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestWavWriting:
    def test_riff_metadata_writing_wav(self, temp_wav_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title RIFF"}
        update_metadata(temp_wav_file, metadata, metadata_format=MetadataFormat.RIFF)
        read_metadata = get_unified_metadata(temp_wav_file, metadata_format=MetadataFormat.RIFF)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title RIFF"

    def test_id3v2_3_metadata_writing_wav(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.3"}
            update_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            read_metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v2.3"
            
    def test_id3v2_4_metadata_writing_wav(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.4"}
            update_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            read_metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v2.4"