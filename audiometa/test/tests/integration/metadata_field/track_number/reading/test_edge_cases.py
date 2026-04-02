import pytest

from audiometa import get_unified_metadata_field
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestTrackNumberReadingEdgeCases:
    @pytest.mark.parametrize("fmt", ["mp3", "flac"])
    def test_trailing_slash(self, fmt):
        with temp_file_with_metadata({"track_number": "5/"}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == "5/"

    @pytest.mark.parametrize("fmt", ["mp3", "flac"])
    def test_leading_slash_no_track(self, fmt):
        with temp_file_with_metadata({"track_number": "/12"}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number is None

    @pytest.mark.parametrize("fmt", ["mp3", "flac"])
    def test_non_numeric_values(self, fmt):
        with temp_file_with_metadata({"track_number": "abc/def"}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number is None

    @pytest.mark.parametrize(
        ("fmt", "expected"),
        [
            ("mp3", None),
            ("flac", ""),
        ],
    )
    def test_empty_string(self, fmt, expected):
        with temp_file_with_metadata({"track_number": ""}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == expected

    @pytest.mark.parametrize("fmt", ["mp3", "flac"])
    def test_multiple_slashes(self, fmt):
        with temp_file_with_metadata({"track_number": "5/12/15"}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number is None

    @pytest.mark.parametrize("fmt", ["mp3", "flac"])
    def test_different_separator(self, fmt):
        with temp_file_with_metadata({"track_number": "5-12"}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == "5-12"

    @pytest.mark.parametrize("fmt", ["mp3", "flac"])
    def test_leading_zeros_preserved(self, fmt):
        with temp_file_with_metadata({"track_number": "01"}, fmt) as test_file:
            track_number = get_unified_metadata_field(test_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == "01"
