import pytest
from audiometa import get_unified_metadata, update_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestFlacWriting:
    def test_vorbis_metadata_writing_flac(self, temp_flac_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title Vorbis"}
        update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.VORBIS)
        read_metadata = get_unified_metadata(temp_flac_file, metadata_format=MetadataFormat.VORBIS)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title Vorbis"

    def test_id3v2_3_metadata_writing_flac(self, temp_flac_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.3"}
        update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
        read_metadata = get_unified_metadata(temp_flac_file, metadata_format=MetadataFormat.ID3V2)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v2.3"

    def test_id3v2_4_metadata_writing_flac(self, temp_flac_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v2.4"}
        update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        read_metadata = get_unified_metadata(temp_flac_file, metadata_format=MetadataFormat.ID3V2)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v2.4"

    def test_id3v1_metadata_writing_flac(self, temp_flac_file):
        metadata = {UnifiedMetadataKey.TITLE: "Test Title ID3v1"}
        update_metadata(temp_flac_file, metadata, metadata_format=MetadataFormat.ID3V1)
        read_metadata = get_unified_metadata(temp_flac_file, metadata_format=MetadataFormat.ID3V1)
        assert read_metadata[UnifiedMetadataKey.TITLE] == "Test Title ID3v1"