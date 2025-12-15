"""Tests for writing MusicBrainz Artist ID metadata field across different formats."""

import pytest

from audiometa import get_unified_metadata, get_unified_metadata_field, update_metadata
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.metadata_format import MetadataFormat
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestMusicBrainzArtistIDWritingByMetadataFormat:
    """Test MusicBrainz Artist ID writing explicitly by metadata format (ID3v2, Vorbis, RIFF)."""

    @pytest.mark.parametrize(
        "artist_ids",
        [
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"],
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"],
        ],
    )
    def test_id3v2_hyphenated_format(self, artist_ids):
        """Test 36-character hyphenated UUID format with ID3v2."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids},
                metadata_format=MetadataFormat.ID3V2,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.ID3V2
            )
            assert result == artist_ids

    @pytest.mark.parametrize(
        "artist_ids",
        [
            ["9d6f6f7c9d524c768f9e01d18d8f8ec6"],
            ["9d6f6f7c9d524c768f9e01d18d8f8ec6", "aaaaaaaaaaaabbbbccccddddeeeeeeee"],
        ],
    )
    def test_id3v2_32_char_hex_format(self, artist_ids):
        """Test 32-character hex UUID format with ID3v2 (should be normalized to hyphenated)."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids},
                metadata_format=MetadataFormat.ID3V2,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.ID3V2
            )
            # Should be normalized to hyphenated format
            expected = []
            for artist_id in artist_ids:
                expected.append(
                    f"{artist_id[:8]}-{artist_id[8:12]}-{artist_id[12:16]}-{artist_id[16:20]}-{artist_id[20:32]}"
                )
            assert result == expected

    @pytest.mark.parametrize(
        "artist_ids",
        [
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"],
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6", "a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
        ],
    )
    def test_vorbis_hyphenated_format(self, artist_ids):
        """Test 36-character hyphenated UUID format with Vorbis."""
        with temp_file_with_metadata({}, "flac") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids},
                metadata_format=MetadataFormat.VORBIS,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.VORBIS
            )
            assert result == artist_ids

    @pytest.mark.parametrize(
        "artist_ids",
        [
            ["9d6f6f7c9d524c768f9e01d18d8f8ec6"],
            ["9d6f6f7c9d524c768f9e01d18d8f8ec6", "aaaaaaaaaaaabbbbccccddddeeeeeeee"],
        ],
    )
    def test_vorbis_32_char_hex_format(self, artist_ids):
        """Test 32-character hex UUID format with Vorbis (should be normalized to hyphenated)."""
        with temp_file_with_metadata({}, "flac") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids},
                metadata_format=MetadataFormat.VORBIS,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.VORBIS
            )
            # Should be normalized to hyphenated format
            expected = []
            for artist_id in artist_ids:
                expected.append(
                    f"{artist_id[:8]}-{artist_id[8:12]}-{artist_id[12:16]}-{artist_id[16:20]}-{artist_id[20:32]}"
                )
            assert result == expected

    @pytest.mark.parametrize(
        "artist_ids",
        [
            ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"],
            ["12345678-1234-5678-9abc-def123456789", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"],
        ],
    )
    def test_riff_hyphenated_format(self, artist_ids):
        """Test 36-character hyphenated UUID format with RIFF."""
        with temp_file_with_metadata({}, "wav") as test_file:
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids},
                metadata_format=MetadataFormat.RIFF,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.RIFF
            )
            assert result == artist_ids

    def test_id3v1_musicbrainz_artistid_not_supported_on_write(self, sample_mp3_file):
        """Test that MusicBrainz Artist ID is not supported by ID3v1 format when explicitly targeting ID3v1."""
        test_metadata = {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]}

        with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
            update_metadata(
                sample_mp3_file,
                test_metadata,
                metadata_format=MetadataFormat.ID3V1,
                fail_on_unsupported_field=True,
            )

    def test_delete_by_setting_to_none(self):
        """Test deleting MusicBrainz Artist ID by setting to None."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            artist_ids = ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: None},
                metadata_format=MetadataFormat.ID3V2,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.ID3V2
            )
            assert result is None or result == []

    def test_delete_by_setting_to_empty_list(self):
        """Test deleting MusicBrainz Artist ID by setting to empty list."""
        with temp_file_with_metadata({}, "flac") as test_file:
            artist_ids = ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]
            update_metadata(test_file, {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: artist_ids})
            update_metadata(
                test_file,
                {UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: []},
                metadata_format=MetadataFormat.VORBIS,
            )
            result = get_unified_metadata_field(
                test_file, UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS, metadata_format=MetadataFormat.VORBIS
            )
            assert result is None or result == []


@pytest.mark.integration
class TestMusicBrainzArtistIDWritingRoundtrip:
    """Test MusicBrainz Artist ID writing roundtrip by file format."""

    def test_musicbrainz_artistid_with_other_fields(self):
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Song",
            UnifiedMetadataKey.ARTISTS: ["Test Artist"],
            UnifiedMetadataKey.ALBUM: "Test Album",
            UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"],
        }

        with temp_file_with_metadata({}, "mp3") as test_file:
            update_metadata(test_file, test_metadata)
            metadata = get_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM) == "Test Album"
            assert metadata.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS) == ["9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"]

    def test_multiple_musicbrainz_artistids_with_other_fields(self):
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Song",
            UnifiedMetadataKey.ARTISTS: ["Test Artist"],
            UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: [
                "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            ],
        }

        with temp_file_with_metadata({}, "flac") as test_file:
            update_metadata(test_file, test_metadata)
            metadata = get_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song"
            assert metadata.get(UnifiedMetadataKey.ARTISTS) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS) == [
                "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            ]
