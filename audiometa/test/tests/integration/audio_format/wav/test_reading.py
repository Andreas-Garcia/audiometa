import pytest
from audiometa import get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestWavReading:
    def test_riff_metadata_reading_wav(self, metadata_riff_small_wav):
        metadata = get_unified_metadata(metadata_riff_small_wav, metadata_format=MetadataFormat.RIFF)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Assuming test file has 'a' * 30
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30

    def test_id3v2_metadata_reading_wav(self, metadata_id3v2_small_wav):
        metadata = get_unified_metadata(metadata_id3v2_small_wav, metadata_format=MetadataFormat.ID3V2)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Assuming 'a' * 30
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30