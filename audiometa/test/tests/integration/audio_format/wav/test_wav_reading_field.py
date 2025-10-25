import pytest
from audiometa import get_unified_metadata_field
from audiometa.exceptions import MetadataFormatNotSupportedByAudioFormatError
from audiometa.test.helpers.id3v1.id3v1_metadata_setter import ID3v1MetadataSetter
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.test.helpers.riff.riff_metadata_setter import RIFFMetadataSetter
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_header_verifier import ID3v2HeaderVerifier


@pytest.mark.integration
class TestWavReading:
    def test_all_metadata_format_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            ID3v1MetadataSetter.set_metadata(test_file.path, {"title": "Title ID3v1"})

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == "Title ID3v1"

    def test_riff_metadata_reading_wav(self, metadata_riff_small_wav):
        with TempFileWithMetadata({}, "wav") as test_file:
            RIFFMetadataSetter.set_metadata(test_file.path, {"title": "RIFF Small Title"})

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.RIFF)
            assert title == "RIFF Small Title"

    def test_id3v2_3_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "ID3v2.3 Long Title That Exceeds RIFF Limits"}, version='2.3')
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            assert title == "ID3v2.3 Long Title That Exceeds RIFF Limits"
            
    def test_id3v2_4_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "ID3v2.4 Long Title That Exceeds RIFF Limits"})
            
            assert ID3v2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            assert title == "ID3v2.4 Long Title That Exceeds RIFF Limits"
            
    def test_vorbis_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.VORBIS)