import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestPublisherWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_publisher = "Test Publisher ID3v2"
            test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            publisher = get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER)
            assert publisher == test_publisher

    def test_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            test_publisher = "Test Publisher RIFF"
            test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        
            # RIFF format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.PUBLISHER metadata not supported by RIFF format"):
                update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)

    def test_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "flac") as test_file:
            test_publisher = "Test Publisher Vorbis"
            test_metadata = {UnifiedMetadataKey.PUBLISHER: test_publisher}
        
            # Vorbis format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.PUBLISHER metadata not supported by this format"):
                update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)
