"""Unit tests for MusicBrainz Artist ID metadata field format validation."""

import pytest

from audiometa import validate_metadata_for_update
from audiometa.exceptions import InvalidMetadataFieldFormatError
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.unit
class TestMusicBrainzArtistIDFormatValidation:
    @pytest.mark.parametrize(
        "artist_ids",
        [
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"],
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"],
            ["9d6f6f7c9d524c768f9e01d18d8f8ec6"],
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "9d6f6f7c9d524c768f9e01d18d8f8ec6"],
        ],
    )
    def test_valid_artist_ids(self, artist_ids):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})

    def test_empty_list_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: []})

    def test_list_with_empty_strings_allowed(self):
        validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["", ""]})

    def test_invalid_format_in_list_raises(self):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            validate_metadata_for_update({UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["not-a-uuid"]})
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value
        assert error.value == "not-a-uuid"

    def test_invalid_format_in_multiple_ids_raises(self):
        with pytest.raises(InvalidMetadataFieldFormatError) as exc_info:
            validate_metadata_for_update(
                {
                    UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: [
                        "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                        "invalid",
                    ]
                }
            )
        error = exc_info.value
        assert error.field == UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value
        assert error.value == "invalid"
