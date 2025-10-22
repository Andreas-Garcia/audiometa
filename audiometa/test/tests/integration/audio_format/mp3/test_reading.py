import pytest
from audiometa import get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestMp3Reading:
    def test_id3v1_limitations(self, metadata_id3v1_small_mp3, metadata_id3v1_big_mp3):
        # Small ID3v1 file
        metadata = get_unified_metadata(metadata_id3v1_small_mp3, metadata_format=MetadataFormat.ID3V1)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit
        
        # Big ID3v1 file (should still be limited)
        metadata = get_unified_metadata(metadata_id3v1_big_mp3, metadata_format=MetadataFormat.ID3V1)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit

    def test_id3v1_metadata_reading_mp3(self, metadata_id3v1_small_mp3):
        metadata = get_unified_metadata(metadata_id3v1_small_mp3, metadata_format=MetadataFormat.ID3V1)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30  # ID3v1 title limit

    def test_id3v2_metadata_reading_mp3(self, metadata_id3v2_small_mp3):
        metadata = get_unified_metadata(metadata_id3v2_small_mp3, metadata_format=MetadataFormat.ID3V2)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # Assuming ID3v2 can have longer titles, but test file has 'a' * 30
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30