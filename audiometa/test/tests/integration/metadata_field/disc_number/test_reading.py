import pytest

from audiometa import get_unified_metadata_field
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestDiscNumberReading:
    def test_id3v2_with_total(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "1/2"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_id3v2_without_total(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "1"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total is None

    def test_id3v2_max_value(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "99/99"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 99
            assert disc_total == 99

    def test_id3v2_hyphen_separator_read(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "1-2"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_id3v2_invalid_tpos_multiple_slashes_returns_none(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "1/2/3"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number is None
            assert disc_total is None

    def test_id3v2_read_tpos_above_255_not_clamped(self):
        with temp_file_with_metadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_metadata(test_file, {"disc_number": "256/300"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 256
            assert disc_total == 300

    def test_vorbis_with_total(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_metadata(test_file, {"disc_number": "1", "disc_total": "2"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_without_total(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_metadata(test_file, {"disc_number": "2"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 2
            assert disc_total is None

    def test_vorbis_disc_number_combined_slash_form(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "3/5")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 3
            assert disc_total == 5

    def test_vorbis_discnumber_combined_slash_via_set_metadata(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_metadata(test_file, {"disc_number": "1/2"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_disc_number_hyphen_form(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "1-2")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_disctotal_overrides_embedded_total(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "1/3")
            VorbisMetadataSetter.set_tag(test_file, "DISCTOTAL", "2")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_discnumber_slash_with_matching_disctotal(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_metadata(test_file, {"disc_number": "1/2", "disc_total": "2"})
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_invalid_disctotal_falls_back_to_discnumber_slash(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "1/2")
            VorbisMetadataSetter.set_tag(test_file, "DISCTOTAL", "bogus")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_negative_disctotal_falls_back_to_discnumber_slash(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "1/2")
            VorbisMetadataSetter.set_tag(test_file, "DISCTOTAL", "-1")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number == 1
            assert disc_total == 2

    def test_vorbis_invalid_combined_discnumber(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCNUMBER", "1/2/3")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number is None
            assert disc_total is None

    def test_vorbis_disctotal_only(self):
        with temp_file_with_metadata({}, "flac") as test_file:
            VorbisMetadataSetter.set_tag(test_file, "DISCTOTAL", "2")
            disc_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_NUMBER)
            disc_total = get_unified_metadata_field(test_file, UnifiedMetadataKey.DISC_TOTAL)
            assert disc_number is None
            assert disc_total == 2

    def test_id3v1_not_supported(self):
        from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
        from audiometa.utils.metadata_format import MetadataFormat

        with temp_file_with_metadata({}, "id3v1") as test_file:
            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_NUMBER metadata not supported by ID3v1 format",
            ):
                get_unified_metadata_field(
                    test_file, UnifiedMetadataKey.DISC_NUMBER, metadata_format=MetadataFormat.ID3V1
                )

            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_TOTAL metadata not supported by ID3v1 format",
            ):
                get_unified_metadata_field(
                    test_file, UnifiedMetadataKey.DISC_TOTAL, metadata_format=MetadataFormat.ID3V1
                )

    def test_riff_not_supported(self):
        from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
        from audiometa.utils.metadata_format import MetadataFormat

        with temp_file_with_metadata({}, "wav") as test_file:
            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_NUMBER metadata not supported by RIFF format",
            ):
                get_unified_metadata_field(
                    test_file, UnifiedMetadataKey.DISC_NUMBER, metadata_format=MetadataFormat.RIFF
                )

            with pytest.raises(
                MetadataFieldNotSupportedByMetadataFormatError,
                match="UnifiedMetadataKey.DISC_TOTAL metadata not supported by RIFF format",
            ):
                get_unified_metadata_field(
                    test_file, UnifiedMetadataKey.DISC_TOTAL, metadata_format=MetadataFormat.RIFF
                )
