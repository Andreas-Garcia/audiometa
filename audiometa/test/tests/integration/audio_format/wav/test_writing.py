import pytest
from audiometa import get_unified_metadata, update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestWavWriting:
    def test_riff_metadata_writing_wav(self, temp_wav_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title RIFF"}
        update_metadata(temp_wav_file, metadata, metadata_format=MetadataFormat.RIFF)
        read_metadata = get_unified_metadata(temp_wav_file, metadata_format=MetadataFormat.RIFF)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title RIFF"

    def test_id3v2_metadata_writing_wav(self, temp_wav_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2"}
        update_metadata(temp_wav_file, metadata, metadata_format=MetadataFormat.ID3V2)
        read_metadata = get_unified_metadata(temp_wav_file, metadata_format=MetadataFormat.ID3V2)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v2"