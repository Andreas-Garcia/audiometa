"""Unit tests for MusicBrainz Track ID metadata field type validation."""

import pytest

from audiometa import validate_metadata_for_update
from audiometa.exceptions import InvalidMetadataFieldTypeError
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.unit
class TestMusicBrainzTrackIDTypeValidation:
    def test_valid_musicbrainz_trackid_string(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"})

    def test_valid_musicbrainz_trackid_without_hyphens(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c9d524c768f9e01d18d8f8ec6"})

    def test_invalid_musicbrainz_trackid_type_integer_raises(self):
        with pytest.raises(InvalidMetadataFieldTypeError):
            validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: 12345})

    def test_invalid_musicbrainz_trackid_type_list_raises(self):
        with pytest.raises(InvalidMetadataFieldTypeError):
            validate_metadata_for_update(
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]}
            )

    def test_musicbrainz_trackid_none_is_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None})

    def test_musicbrainz_trackid_empty_string_is_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_TRACKID: ""})
