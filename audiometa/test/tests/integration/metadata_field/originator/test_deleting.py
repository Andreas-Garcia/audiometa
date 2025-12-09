import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.riff import RIFFMetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestOriginatorDeleting:
    def test_delete_originator_riff(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            RIFFMetadataSetter.set_metadata(test_file, {"originator": "Test originator"})
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR) == "Test originator"

            update_metadata(test_file, {UnifiedMetadataKey.ORIGINATOR: None}, metadata_format=MetadataFormat.RIFF)
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR) is None

    def test_delete_originator_preserves_other_fields(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            RIFFMetadataSetter.set_metadata(test_file, {"originator": "Test originator", "title": "Test Title"})
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR) == "Test originator"
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.TITLE) == "Test Title"

            update_metadata(test_file, {UnifiedMetadataKey.ORIGINATOR: None}, metadata_format=MetadataFormat.RIFF)
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR) is None
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.TITLE) == "Test Title"

    def test_delete_originator_vorbis_raises(self):
        with (
            temp_file_with_metadata({}, "flac") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            update_metadata(test_file, {UnifiedMetadataKey.ORIGINATOR: None}, metadata_format=MetadataFormat.VORBIS)

    def test_delete_originator_id3v1_raises(self):
        with (
            temp_file_with_metadata({}, "id3v1") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            update_metadata(test_file, {UnifiedMetadataKey.ORIGINATOR: None}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_originator_id3v2_raises(self):
        with (
            temp_file_with_metadata({}, "mp3") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            update_metadata(test_file, {UnifiedMetadataKey.ORIGINATOR: None}, metadata_format=MetadataFormat.ID3V2)
