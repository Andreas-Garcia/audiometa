import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.riff import RIFFMetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.test.helpers.vorbis import VorbisMetadataSetter
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestDescriptionDeleting:
    def test_delete_description_riff(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            RIFFMetadataSetter.set_metadata(test_file, {"description": "Test description"})
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION) == "Test description"

            update_metadata(test_file, {UnifiedMetadataKey.DESCRIPTION: None}, metadata_format=MetadataFormat.RIFF)
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION) is None

    def test_delete_description_vorbis(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_metadata(test_file, {"description": "Test description"})
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION) == "Test description"

            update_metadata(test_file, {UnifiedMetadataKey.DESCRIPTION: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION) is None

    def test_delete_description_preserves_other_fields(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_metadata(test_file, {"description": "Test description", "title": "Test Title"})
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION) == "Test description"
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.TITLE) == "Test Title"

            update_metadata(test_file, {UnifiedMetadataKey.DESCRIPTION: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION) is None
            assert get_unified_metadata_field(test_file, UnifiedMetadataKey.TITLE) == "Test Title"

    def test_delete_description_id3v1_raises(self):
        with (
            temp_file_with_metadata({}, "id3v1") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            update_metadata(test_file, {UnifiedMetadataKey.DESCRIPTION: None}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_description_id3v2_raises(self):
        with (
            temp_file_with_metadata({}, "mp3") as test_file,
            pytest.raises(MetadataFieldNotSupportedByMetadataFormatError),
        ):
            update_metadata(test_file, {UnifiedMetadataKey.DESCRIPTION: None}, metadata_format=MetadataFormat.ID3V2)
