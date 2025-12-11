"""Tests for reading MusicBrainz Track ID metadata field across different formats."""

import pytest

from audiometa import get_unified_metadata_field
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestMusicBrainzTrackIDReading:
    def test_id3v1_musicbrainz_trackid_not_supported(self, sample_mp3_file):
        """Test that MusicBrainz Track ID is not supported by ID3v1 format when explicitly requesting ID3v1."""
        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
            get_unified_metadata_field(
                sample_mp3_file,
                UnifiedMetadataKey.MUSICBRAINZ_TRACKID,
                metadata_format=MetadataFormat.ID3V1,
            )

    def test_id3v2_ufid_reading(self):
        """Test reading MusicBrainz Track ID from UFID frame (preferred format)."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}, "mp3"
        ) as test_file:
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert track_id == "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"

    def test_id3v2_ufid_32_char_hex_reading(self):
        """Test reading 32-character hex format from UFID frame and normalization to hyphenated format."""
        with temp_file_with_metadata({"musicbrainz_trackid": "9d6f6f7c9d524c768f9e01d18d8f8ec6"}, "mp3") as test_file:
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            # Should be normalized to hyphenated format
            assert track_id == "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"

    def test_id3v2_txxx_reading(self):
        """Test reading MusicBrainz Track ID from TXXX frame (fallback format)."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            track_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            ID3v2MetadataSetter.set_musicbrainz_trackid_txxx(test_file, track_id)
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert result == track_id

    def test_id3v2_txxx_32_char_hex_reading(self):
        """Test reading 32-character hex format from TXXX frame and normalization to hyphenated format."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            track_id_hex = "9d6f6f7c9d524c768f9e01d18d8f8ec6"
            ID3v2MetadataSetter.set_musicbrainz_trackid_txxx(test_file, track_id_hex)
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            # Should be normalized to hyphenated format
            assert result == "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"

    def test_id3v2_ufid_priority_over_txxx(self):
        """Test that UFID frame is preferred over TXXX frame when both are present."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            ufid_track_id = "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
            txxx_track_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            ID3v2MetadataSetter.set_musicbrainz_trackid_ufid(test_file, ufid_track_id)
            ID3v2MetadataSetter.set_musicbrainz_trackid_txxx(test_file, txxx_track_id)
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert result == ufid_track_id

    def test_id3v2_ufid_different_owner_not_read(self):
        """Test that UFID frames with a different owner are not read as MusicBrainz Track ID."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            # Set UFID frame with a different owner (not http://musicbrainz.org)
            other_owner = "http://example.com"
            other_data = "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
            ID3v2MetadataSetter.set_ufid_with_owner(test_file, other_owner, other_data)
            # Should not be read as MusicBrainz Track ID
            result = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert result is None

    def test_vorbis_reading(self):
        """Test reading MusicBrainz Track ID from Vorbis comments."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}, "flac"
        ) as test_file:
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert track_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

    def test_riff_reading(self):
        """Test reading MusicBrainz Track ID from RIFF MBID FourCC."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "12345678-1234-5678-9abc-def123456789"}, "wav"
        ) as test_file:
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert track_id == "12345678-1234-5678-9abc-def123456789"
