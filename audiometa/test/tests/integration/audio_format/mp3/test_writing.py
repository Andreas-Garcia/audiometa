import pytest
from audiometa import get_unified_metadata, update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestMp3Writing:
    def test_id3v1_metadata_writing_mp3(self, temp_audio_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v1"}
        update_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V1)
        read_metadata = get_unified_metadata(temp_audio_file, metadata_format=MetadataFormat.ID3V1)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v1"

    def test_id3v2_metadata_writing_mp3(self, temp_audio_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2"}
        update_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2)
        read_metadata = get_unified_metadata(temp_audio_file, metadata_format=MetadataFormat.ID3V2)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v2"