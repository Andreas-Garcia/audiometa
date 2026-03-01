"""Unit tests for MusicBrainz UUID format validation (shared helper)."""

import pytest

from audiometa.exceptions import InvalidMetadataFieldFormatError
from audiometa.manager._MetadataManager import _MetadataManager
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.unit
class TestMusicBrainzUUIDFormatValidation:
    @pytest.mark.parametrize(
        "uuid_str",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",  # Standard 36-char hyphenated format
            "00000000-0000-0000-0000-000000000000",  # All zeros
            "ffffffff-ffff-ffff-ffff-ffffffffffff",  # All Fs
            "9D6F6F7C-9D52-4C76-8F9E-01D18D8F8EC6",  # Uppercase
        ],
    )
    def test_valid_36_char_hyphenated_format(self, uuid_str):
        _MetadataManager._validate_musicbrainz_uuid_format(uuid_str, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)

    @pytest.mark.parametrize(
        "uuid_str",
        [
            "9d6f6f7c9d524c768f9e01d18d8f8ec6",  # Standard 32-char hex format
            "00000000000000000000000000000000",  # All zeros
            "ffffffffffffffffffffffffffffffff",  # All Fs
            "9D6F6F7C9D524C768F9E01D18D8F8EC6",  # Uppercase
        ],
    )
    def test_valid_32_char_hex_format(self, uuid_str):
        _MetadataManager._validate_musicbrainz_uuid_format(uuid_str, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)

    @pytest.mark.parametrize(
        "uuid_str",
        [
            "9d6f6f7c-9d52-4c76",  # Too short (hyphenated)
            "9d6f6f7c-9d52",  # Too short
            "9d6f6f7c",  # Way too short
            "9d6f6f7c9d524c76",  # Too short (32-char format)
            "abc",  # Way too short
        ],
    )
    def test_invalid_format_too_short(self, uuid_str):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            _MetadataManager._validate_musicbrainz_uuid_format(uuid_str, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value
        assert error.value == uuid_str

    @pytest.mark.parametrize(
        "uuid_str",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6-extra",  # Too long (hyphenated)
            "9d6f6f7c9d524c768f9e01d18d8f8ec6extra",  # Too long (32-char format)
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6-01d18d8f8ec6",  # Way too long
        ],
    )
    def test_invalid_format_too_long(self, uuid_str):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            _MetadataManager._validate_musicbrainz_uuid_format(uuid_str, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value
        assert error.value == uuid_str

    @pytest.mark.parametrize(
        "uuid_str",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec",  # Wrong hyphen positions
            "9d6f6f7c9d52-4c76-8f9e-01d18d8f8ec6",  # Mixed format
            "9d6f-6f7c-9d52-4c76-8f9e-01d18d8f8ec6",  # Too many hyphens
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec66",  # Extra character
        ],
    )
    def test_invalid_hyphenated_format(self, uuid_str):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            _MetadataManager._validate_musicbrainz_uuid_format(uuid_str, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value
        assert error.value == uuid_str

    @pytest.mark.parametrize(
        "uuid_str",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8eg",  # Invalid hex character (g)
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8e!",  # Special character
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8e@",  # Special character
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8e ",  # Space
            "not-a-uuid",  # Not a UUID
        ],
    )
    def test_invalid_format_special_characters(self, uuid_str):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            _MetadataManager._validate_musicbrainz_uuid_format(uuid_str, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value
        assert error.value == uuid_str

    def test_empty_string_allowed(self):
        _MetadataManager._validate_musicbrainz_uuid_format("", UnifiedMetadataKey.MUSICBRAINZ_TRACKID)

    def test_field_key_used_in_error_message(self):
        """Test that the correct field key is used in error messages."""
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            _MetadataManager._validate_musicbrainz_uuid_format("invalid", UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
        assert exc_info.value.field == UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value

        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            _MetadataManager._validate_musicbrainz_uuid_format("invalid", UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
        assert exc_info.value.field == UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value
