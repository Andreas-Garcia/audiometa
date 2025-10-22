import pytest
from audiometa import get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestWavReading:
    def test_riff_metadata_reading_wav(self, metadata_riff_small_wav):
        metadata = get_unified_metadata(metadata_riff_small_wav, metadata_format=MetadataFormat.RIFF)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Assuming test file has 'a' * 30
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30

    def test_id3v2_3_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.3 Long Title That Exceeds RIFF Limits")

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, version=[2, 3, 0])
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "ID3v2.3 Long Title That Exceeds RIFF Limits"
            
    def test_id3v2_4_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.4 Long Title That Exceeds RIFF Limits")

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, version=[2, 4, 0])
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "ID3v2.4 Long Title That Exceeds RIFF Limits"