"""Unit tests for MusicBrainz Track ID metadata field format validation.

Note: Comprehensive UUID format validation is tested in musicbrainz_uuid/test_uuid_format_validation.py.
These tests focus on Track ID-specific integration with the public API.
"""

import pytest

from audiometa import validate_metadata_for_update
from audiometa.exceptions import InvalidMetadataFieldFormatError, InvalidMetadataFieldTypeError
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.unit
class TestMusicBrainzTrackIDFormatValidation:
    def test_valid_track_id_36_char_format(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"})

    def test_valid_track_id_32_char_format(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c9d524c768f9e01d18d8f8ec6"})

    def test_invalid_track_id_format_raises(self):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "not-a-uuid"})
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value
        assert error.value == "not-a-uuid"

    def test_none_value_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None})

    def test_empty_string_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: ""})

    def test_format_validation_after_type_validation(self):
        invalid_type = {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: 12345}
        with pytest.raises(InvalidMetadataFieldTypeError) as exc_info:
            validate_metadata_for_update(invalid_type)
        assert not isinstance(exc_info.value, InvalidMetadataFieldFormatError)
