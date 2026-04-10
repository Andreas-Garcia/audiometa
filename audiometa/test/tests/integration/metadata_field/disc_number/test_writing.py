import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestDiscNumberWriting:
    @pytest.mark.parametrize(
        ("disc_number", "disc_total", "expected_disc_number", "expected_disc_total"),
        [
            (1, None, 1, None),
            (1, 2, 1, 2),
            (99, 99, 99, 99),
        ],
    )
    def test_id3v2_disc_number_writing(self, disc_number, disc_total, expected_disc_number, expected_disc_total):
        with temp_file_with_metadata({}, "mp3") as test_file:
            metadata = {UnifiedMetadataKey.DISC_NUMBER: disc_number}
            if disc_total is not None:
                metadata[UnifiedMetadataKey.DISC_TOTAL] = disc_total
            update_metadata(test_file, metadata, metadata_format=MetadataFormat.ID3V2)

            result_disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            result_disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert result_disc_number == expected_disc_number
            assert result_disc_total == expected_disc_total

    @pytest.mark.parametrize(
        ("disc_number", "disc_total", "expected_disc_number", "expected_disc_total"),
        [
            (1, None, 1, None),
            (1, 2, 1, 2),
            (99, 99, 99, 99),
        ],
    )
    def test_vorbis_disc_number_writing(self, disc_number, disc_total, expected_disc_number, expected_disc_total):
        with temp_file_with_metadata({}, "flac") as test_file:
            metadata = {UnifiedMetadataKey.DISC_NUMBER: disc_number}
            if disc_total is not None:
                metadata[UnifiedMetadataKey.DISC_TOTAL] = disc_total
            update_metadata(test_file, metadata, metadata_format=MetadataFormat.VORBIS)

            result_disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            result_disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert result_disc_number == expected_disc_number
            assert result_disc_total == expected_disc_total

    def test_id3v2_disc_number_with_total_combines_format(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 1, UnifiedMetadataKey.DISC_TOTAL: 2},
                metadata_format=MetadataFormat.ID3V2,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_id3v2_disc_number_without_total_writes_simple_format(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(test_file, {UnifiedMetadataKey.DISC_NUMBER: 1}, metadata_format=MetadataFormat.ID3V2)
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total is None

    def test_id3v2_update_disc_number_preserves_total_from_hyphen_tpos(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "1-2"})

            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 5},
                metadata_format=MetadataFormat.ID3V2,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 5
            assert disc_total == 2

    def test_id3v2_update_disc_total_preserves_disc_number_from_hyphen_tpos(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "1-2"})

            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_TOTAL: 4},
                metadata_format=MetadataFormat.ID3V2,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 4

    def test_vorbis_disc_number_writes_separate_fields(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 1, UnifiedMetadataKey.DISC_TOTAL: 2},
                metadata_format=MetadataFormat.VORBIS,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    @pytest.mark.parametrize(
        "initial_disc_number",
        ["1/2", "1-2"],
    )
    def test_vorbis_update_disc_number_preserves_total_from_combined_discnumber(self, initial_disc_number):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", initial_disc_number)

            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 5},
                metadata_format=MetadataFormat.VORBIS,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 5
            assert disc_total == 2

    def test_vorbis_update_disc_number_preserves_explicit_total_when_conflicting(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "1/3")
            VorbisMetadataSetter.set_tag(test_file, "DISCTOTAL", "2")

            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 5},
                metadata_format=MetadataFormat.VORBIS,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 5
            assert disc_total == 2

    def test_id3v2_disc_number_max_value_truncated(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 256, UnifiedMetadataKey.DISC_TOTAL: 300},
                metadata_format=MetadataFormat.ID3V2,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 255
            assert disc_total == 255

    def test_vorbis_disc_number_no_limit(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.DISC_NUMBER: 256, UnifiedMetadataKey.DISC_TOTAL: 300},
                metadata_format=MetadataFormat.VORBIS,
            )
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 256
            assert disc_total == 300

    def test_id3v1_not_supported(self):
        from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError

        with temp_file_with_metadata({}, "mp3") as test_file:
            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_NUMBER metadata not supported by ID3v1 format",
            ):
                update_metadata(
                    test_file,
                    {UnifiedMetadataKey.DISC_NUMBER: 1},
                    metadata_format=MetadataFormat.ID3V1,
                )

            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_TOTAL metadata not supported by ID3v1 format",
            ):
                update_metadata(
                    test_file,
                    {UnifiedMetadataKey.DISC_TOTAL: 2},
                    metadata_format=MetadataFormat.ID3V1,
                )

    def test_riff_not_supported(self):
        from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError

        with temp_file_with_metadata({}, "wav") as test_file:
            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_NUMBER metadata not supported by RIFF format",
            ):
                update_metadata(
                    test_file,
                    {UnifiedMetadataKey.DISC_NUMBER: 1},
                    metadata_format=MetadataFormat.RIFF,
                )

            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_TOTAL metadata not supported by RIFF format",
            ):
                update_metadata(
                    test_file,
                    {UnifiedMetadataKey.DISC_TOTAL: 2},
                    metadata_format=MetadataFormat.RIFF,
                )
