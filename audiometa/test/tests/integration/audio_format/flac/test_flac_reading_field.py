import pytest

from audiometa import get_unified_metadata_field
from audiometa.exceptions import MetadataFormatNotSupportedByAudioFormatError
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v1.id3v1_metadata_getter import ID3v1MetadataGetter
from audiometa.test.helpers.id3v1.id3v1_metadata_setter import ID3v1MetadataSetter


@pytest.mark.integration
class TestFlacReading:
    def test_vorbis_metadata_reading_flac(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set test metadata
            from audiometa.test.helpers.vorbis import VorbisMetadataSetter
            VorbisMetadataSetter.add_title(test_file.path, 'a' * 30)

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.VORBIS)
            assert title == 'a' * 30

    def test_id3v2_3_metadata_reading_flac(self):
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            # Set test metadata
            from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.3 Long Title That Exceeds ID3v1 Limits")

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            assert title == "ID3v2.3 Long Title That Exceeds ID3v1 Limits"
            
    def test_id3v2_4_metadata_reading_flac(self):
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            # Set test metadata
            from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
            ID3v2MetadataSetter.set_title(test_file.path, "ID3v2.4 Long Title That Exceeds ID3v1 Limits")

            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            assert title == "ID3v2.4 Long Title That Exceeds ID3v1 Limits"

    def test_id3v1_metadata_reading_flac(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            ID3v1MetadataSetter.set_title(test_file.path, 'a' * 30)
            assert ID3v1MetadataGetter.get_title(test_file.path) == 'a' * 30
            
            title = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V1)
            assert title == 'a' * 30
            
    def test_riff_metadata_reading_flac(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            with pytest.raises(MetadataFormatNotSupportedByAudioFormatError):
                get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.RIFF)