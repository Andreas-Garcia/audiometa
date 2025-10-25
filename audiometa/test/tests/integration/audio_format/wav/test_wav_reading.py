import pytest
from audiometa import get_unified_metadata
from audiometa.exceptions import MetadataFormatNotSupportedByAudioFormatError
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_header_verifier import ID3v2HeaderVerifier


@pytest.mark.integration
class TestWavReading:
    def test_riff_metadata_reading_wav(self, metadata_riff_small_wav):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Set test metadata
            from audiometa.test.helpers.riff import RIFFMetadataSetter
            RIFFMetadataSetter.set_title(test_file.path, "RIFF Small Title")

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "RIFF Small Title"

    def test_id3v2_3_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.3 Long Title That Exceeds RIFF Limits", version='2.3')
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "ID3v2.3 Long Title That Exceeds RIFF Limits"
            
    def test_id3v2_4_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.4 Long Title That Exceeds RIFF Limits")
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            assert isinstance(metadata, dict)
            assert UnifiedMetadataKey.TITLE in metadata
            assert metadata[UnifiedMetadataKey.TITLE] == "ID3v2.4 Long Title That Exceeds RIFF Limits"
            
    def test_vorbis_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                get_unified_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.VORBIS)