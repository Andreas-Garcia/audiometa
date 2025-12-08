import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestDescriptionWriting:
    def test_riff(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            test_description = "Test Description RIFF"
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: test_description}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.RIFF)
            description = get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION)
            assert description == test_description

    def test_vorbis(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            test_description = "Test Description Vorbis"
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: test_description}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
            description = get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION)
            assert description == test_description

    def test_riff_empty(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: ""}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.RIFF)
            description = get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION)
            assert description is None

    def test_vorbis_empty(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: ""}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
            description = get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION)
            assert description is None

    def test_riff_long_description_truncated(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            long_description = "A" * 300  # Over 256 bytes
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: long_description}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.RIFF)
            description = get_unified_metadata_field(test_file, UnifiedMetadataKey.DESCRIPTION)
            assert len(description.encode("utf-8")) <= 256

    def test_id3v1_raises(self):
        with temp_file_with_metadata({}, "id3v1") as test_file:
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: "Test Description"}
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.ID3V1)

    def test_id3v2_raises(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.DESCRIPTION: "Test Description"}
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.ID3V2)

    def test_invalid_type_raises(self):
        from audiometa.exceptions import InvalidMetadataFieldTypeError

        with temp_file_with_metadata({}, "wav") as test_file:
            bad_metadata = {UnifiedMetadataKey.DESCRIPTION: 12345}
            with pytest.raises(InvalidMetadataFieldTypeError):
                update_metadata(test_file, bad_metadata)
