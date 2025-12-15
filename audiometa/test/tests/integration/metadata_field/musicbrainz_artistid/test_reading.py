"""Tests for reading MusicBrainz Artist ID metadata field across different formats."""

import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestMusicBrainzArtistIDReading:
    def test_id3v1_musicbrainz_artistid_not_supported(self, sample_mp3_file):
        """Test that MusicBrainz Artist ID is not supported by ID3v1 format when explicitly requesting ID3v1."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
            get_unified_metadata_field(
                sample_mp3_file,
                UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS,
                metadata_format=MetadataFormat.ID3V1,
            )

    def test_id3v2_txxx_reading(self):
        """Test reading MusicBrainz Artist ID from TXXX frame."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            artist_ids = ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == artist_ids

    def test_id3v2_txxx_multiple_reading(self):
        """Test reading multiple MusicBrainz Artist IDs from TXXX frame (separator-based values)."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            artist_ids = [
                "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            ]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == artist_ids

    def test_id3v2_txxx_32_char_hex_reading(self):
        """Test reading 32-character hex format from TXXX frame and normalization to hyphenated format."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            artist_id_hex = "9d6f6f7c9d524c768f9e01d18d8f8ec6"
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: [artist_id_hex]})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            # Should be normalized to hyphenated format
            assert result == ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]

    def test_id3v2_txxx_case_insensitive_reading(self):
        """Test reading MusicBrainz Artist ID from TXXX frames with different case descriptions."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            artist_id = "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: [artist_id]})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == [artist_id]

    def test_vorbis_reading(self):
        """Test reading MusicBrainz Artist ID from Vorbis comments."""
        with temp_file_with_metadata({}, "flac") as test_file:
            artist_ids = ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == artist_ids

    def test_vorbis_multiple_reading(self):
        """Test reading multiple MusicBrainz Artist IDs from Vorbis comments."""
        with temp_file_with_metadata({}, "flac") as test_file:
            artist_ids = [
                "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "11111111-2222-3333-4444-555555555555",
            ]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == artist_ids

    def test_riff_reading(self):
        """Test reading MusicBrainz Artist ID from RIFF MBAR FourCC."""
        with temp_file_with_metadata({}, "wav") as test_file:
            artist_ids = ["12345678-1234-5678-9abc-def123456789"]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == artist_ids

    def test_riff_multiple_reading(self):
        """Test reading multiple MusicBrainz Artist IDs from RIFF MBAR FourCC."""
        with temp_file_with_metadata({}, "wav") as test_file:
            artist_ids = [
                "12345678-1234-5678-9abc-def123456789",
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            ]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS)
            assert result == artist_ids
