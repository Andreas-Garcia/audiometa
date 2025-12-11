"""Tests for writing MusicBrainz Track ID metadata field across different formats."""

import pytest

from audiometa import get_unified_metadata, get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestMusicBrainzTrackIDWritingByMetadataFormat:
    """Test MusicBrainz Track ID writing explicitly by metadata format (ID3v2, Vorbis, RIFF)."""

    @pytest.mark.parametrize(
        "track_id",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",  # Standard 36-char hyphenated format
            "00000000-0000-0000-0000-000000000000",  # All zeros
            "ffffffff-ffff-ffff-ffff-ffffffffffff",  # All Fs
        ],
    )
    def test_id3v2_hyphenated_format(self, track_id):
        """Test 36-character hyphenated UUID format with ID3v2."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: track_id},
                metadata_format=MetadataFormat.ID3V2,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID, metadata_format=MetadataFormat.ID3V2
            )
            assert result == track_id

    @pytest.mark.parametrize(
        "track_id",
        [
            "9d6f6f7c9d524c768f9e01d18d8f8ec6",  # 32-character hex format
            "00000000000000000000000000000000",  # All zeros
            "ffffffffffffffffffffffffffffffff",  # All Fs
        ],
    )
    def test_id3v2_32_char_hex_format(self, track_id):
        """Test 32-character hex UUID format with ID3v2 (should be normalized to hyphenated)."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: track_id},
                metadata_format=MetadataFormat.ID3V2,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID, metadata_format=MetadataFormat.ID3V2
            )
            # Should be normalized to hyphenated format
            expected = f"{track_id[:8]}-{track_id[8:12]}-{track_id[12:16]}-{track_id[16:20]}-{track_id[20:32]}"
            assert result == expected

    @pytest.mark.parametrize(
        "track_id",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",  # Standard 36-char hyphenated format
            "a1b2c3d4-e5f6-7890-abcd-ef1234567890",  # Another example
        ],
    )
    def test_vorbis_hyphenated_format(self, track_id):
        """Test 36-character hyphenated UUID format with Vorbis."""
        with temp_file_with_metadata({}, "flac") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: track_id},
                metadata_format=MetadataFormat.VORBIS,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID, metadata_format=MetadataFormat.VORBIS
            )
            assert result == track_id

    @pytest.mark.parametrize(
        "track_id",
        [
            "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",  # Standard 36-char hyphenated format
            "12345678-1234-5678-9abc-def123456789",  # Another example
        ],
    )
    def test_riff_hyphenated_format(self, track_id):
        """Test 36-character hyphenated UUID format with RIFF."""
        with temp_file_with_metadata({}, "wav") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: track_id},
                metadata_format=MetadataFormat.RIFF,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID, metadata_format=MetadataFormat.RIFF
            )
            assert result == track_id

    def test_id3v1_musicbrainz_trackid_not_supported_on_write(self, sample_mp3_file):
        """Test that MusicBrainz Track ID is not supported by ID3v1 format when explicitly targeting ID3v1."""
        test_metadata = {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}

        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
            update_metadata(
                sample_mp3_file,
                test_metadata,
                metadata_format=MetadataFormat.ID3V1,
                fail_on_unsupported_field=True,
            )

    def test_delete_by_setting_to_none(self):
        """Test deleting MusicBrainz Track ID by setting to None."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}, "mp3"
        ) as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None},
                metadata_format=MetadataFormat.ID3V2,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID, metadata_format=MetadataFormat.ID3V2
            )
            assert result is None

    def test_delete_by_setting_to_empty_string(self):
        """Test deleting MusicBrainz Track ID by setting to empty string."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}, "flac"
        ) as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_TRACKID: ""},
                metadata_format=MetadataFormat.VORBIS,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID, metadata_format=MetadataFormat.VORBIS
            )
            assert result is None


@pytest.mark.integration
class TestMusicBrainzTrackIDWritingRoundtrip:
    """Test MusicBrainz Track ID writing roundtrip by file format."""

    def test_musicbrainz_trackid_with_other_fields(self):
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Song",
            UnifiedMetadataKey.ARTISTS: ["Test Artist"],
            UnifiedMetadataKey.ALBUM: "Test Album",
            UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
        }

        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(test_file, test_metadata)
            metadata = get_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID) == "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
