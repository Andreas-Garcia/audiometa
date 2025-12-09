import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestOriginatorWriting:
    def test_riff(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            test_originator = "Test Originator RIFF"
            test_metadata = {UnifiedMetadataKey.ORIGINATOR: test_originator}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.RIFF)
            originator = get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)
            assert originator == test_originator

    def test_riff_empty(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.ORIGINATOR: ""}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.RIFF)
            originator = get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)
            assert originator is None

    def test_riff_long_originator_truncated(self):
        with temp_file_with_metadata({}, "wav") as test_file:
            long_originator = "A" * 50  # Over 32 bytes
            test_metadata = {UnifiedMetadataKey.ORIGINATOR: long_originator}
            update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.RIFF)
            originator = get_unified_metadata_field(test_file, UnifiedMetadataKey.ORIGINATOR)
            assert originator is not None
            assert len(originator.encode("utf-8")) <= 32

    def test_vorbis_raises(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            test_metadata = {UnifiedMetadataKey.ORIGINATOR: "Test Originator"}
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.VORBIS)

    def test_id3v1_raises(self):
        with temp_file_with_metadata({}, "id3v1") as test_file:
            test_metadata = {UnifiedMetadataKey.ORIGINATOR: "Test Originator"}
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.ID3V1)

    def test_id3v2_raises(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            test_metadata = {UnifiedMetadataKey.ORIGINATOR: "Test Originator"}
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file, test_metadata, metadata_format=MetadataFormat.ID3V2)

    def test_invalid_type_raises(self):
        from audiometa.exceptions import InvalidMetadataFieldTypeError

        with temp_file_with_metadata({}, "wav") as test_file:
            bad_metadata = {UnifiedMetadataKey.ORIGINATOR: 12345}
            with pytest.raises(InvalidMetadataFieldTypeError):
                update_metadata(test_file, bad_metadata)
