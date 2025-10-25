import pytest

from audiometa import get_unified_metadata
from audiometa.exceptions import MetadataFormatNotSupportedByAudioFormatError
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v1.id3v1_metadata_getter import ID3v1MetadataGetter
from audiometa.test.helpers.id3v1.id3v1_metadata_setter import ID3v1MetadataSetter
from audiometa.test.helpers.riff.riff_metadata_setter import RIFFMetadataSetter


@pytest.mark.integration
class TestWavReading:
    def test_all_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            ID3v1MetadataSetter.set_metadata(test_file.path, {'title': 'a' * 30})
            assert ID3v1MetadataGetter.get_title(test_file.path) == 'a' * 30

            metadata = get_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) == 'a' * 30

    def test_id3v2_3_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "ID3v2.3 Long Title That Exceeds ID3v1 Limits"}, version='2.3')

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"
            
    def test_id3v2_4_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file.path, {"title": "ID3v2.4 Long Title That Exceeds ID3v1 Limits"}, version='2.4')

            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            assert metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2.4 Long Title That Exceeds ID3v1 Limits"

    def test_id3v1_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            ID3v1MetadataSetter.set_metadata(test_file.path, {'title': 'a' * 30})
            assert ID3v1MetadataGetter.get_title(test_file.path) == 'a' * 30
            
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert metadata.get(UnifiedMetadataKey.TITLE) == 'a' * 30
            
    def test_riff_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            RIFFMetadataSetter.set_title(test_file.path, 'a' * 30)
                
            metadata = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.RIFF)
            assert metadata.get(UnifiedMetadataKey.TITLE) == 'a' * 30
            
    def test_vorbis_metadata_reading_wav(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                get_unified_metadata(test_file.path, metadata_format=MetadataFormat.VORBIS)