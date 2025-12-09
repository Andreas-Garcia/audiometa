import pytest

from audiometa import get_unified_metadata_field
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.riff import RIFFMetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestOriginatorReading:
    def test_riff(self):
        with temp_file_with_metadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_metadata(test_file, {"originator": "Test Originator RIFF"})
            originator = get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)
            assert originator == "Test Originator RIFF"

    def test_vorbis(self):
        with (
            temp_file_with_metadata({"title": "Test Song"}, "flac") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)

    def test_id3v1(self):
        with (
            temp_file_with_metadata({"title": "Test Song"}, "id3v1") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)

    def test_id3v2(self):
        with (
            temp_file_with_metadata({"title": "Test Song"}, "mp3") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)
