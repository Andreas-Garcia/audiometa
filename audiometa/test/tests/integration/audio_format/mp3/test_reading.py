import pytest
from audiometa import get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMp3Reading:
    def test_id3v1_metadata_reading_mp3(self, metadata_id3v1_big_mp3):
        metadata_big = get_unified_metadata(metadata_id3v1_big_mp3, metadata_format=MetadataFormat.ID3V1)
        assert isinstance(metadata_big, dict)
        assert UnifiedMetadataKey.TITLE in metadata_big
        assert metadata_big[UnifiedMetadataKey.TITLE] == 'b' * 30  # ID3v1 title limit

    def test_id3v2_3_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.3 Long Title That Exceeds ID3v1 Limits")

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, version=(2, 3, 0))
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"
            
    def test_id3v2_4_metadata_reading_mp3(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.4 Long Title That Exceeds ID3v1 Limits")

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, version=(2, 4, 0))
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "ID3v2.4 Long Title That Exceeds ID3v1 Limits"