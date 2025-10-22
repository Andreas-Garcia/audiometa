import pytest
from audiometa import get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestFlacReading:
    def test_vorbis_metadata_reading_flac(self, metadata_vorbis_small_flac):
        metadata = get_unified_metadata(metadata_vorbis_small_flac, metadata_format=MetadataFormat.VORBIS)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Assuming 'a' * 30
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30

    def test_id3v2_metadata_reading_flac(self, metadata_id3v2_small_flac):
        metadata = get_unified_metadata(metadata_id3v2_small_flac, metadata_format=MetadataFormat.ID3V2)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Assuming 'a' * 30
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30

    def test_id3v1_metadata_reading_flac(self, metadata_id3v1_small_flac):
        metadata = get_unified_metadata(metadata_id3v1_small_flac, metadata_format=MetadataFormat.ID3V1)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30