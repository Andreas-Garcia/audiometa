"""Unit tests for MusicBrainz Artist ID metadata field type validation."""

import pytest

from audiometa import validate_metadata_for_update
from audiometa.exceptions import InvalidMetadataFieldTypeError
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.unit
class TestMusicBrainzArtistIDTypeValidation:
    def test_valid_musicbrainz_artistid_list(self):
        validate_metadata_for_update(
            {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]}
        )

    def test_valid_musicbrainz_artistid_empty_list(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: []})

    def test_valid_musicbrainz_artistid_list_with_empty_strings(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["", ""]})

    def test_invalid_musicbrainz_artistid_type_string_raises(self):
        with pytest.raises(InvalidMetadataFieldTypeError):
            validate_metadata_for_update(
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}
            )

    def test_invalid_musicbrainz_artistid_type_integer_raises(self):
        with pytest.raises(InvalidMetadataFieldTypeError):
            validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: 12345})

    def test_musicbrainz_artistid_none_is_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: None})
