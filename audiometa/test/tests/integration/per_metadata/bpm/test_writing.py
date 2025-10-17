import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestBpmWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_bpm = 128
            test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            bpm = get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM)
            assert bpm == test_bpm

    def test_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            test_bpm = 120
            test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        
            # RIFF format raises exception for unsupported metadata when format is forced
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by RIFF format"):
                update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)

    def test_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_bpm = 140
            test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)
            bpm = get_specific_metadata(test_file.path, UnifiedMetadataKey.BPM)
            assert bpm == test_bpm

    def test_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_bpm = 128
            test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        
            # ID3v1 format raises exception for unsupported metadata when format is forced
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by this format"):
                update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V1)
