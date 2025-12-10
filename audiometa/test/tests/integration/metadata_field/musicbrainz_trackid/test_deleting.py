"""Tests for deleting MusicBrainz Track ID metadata field."""

import pytest

from audiometa import delete_all_metadata, get_unified_metadata_field
from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.integration
class TestMusicBrainzTrackIDDeleting:
    def test_id3v2_musicbrainz_trackid_deleted_with_all_metadata(self):
        """Test that MusicBrainz Track ID is deleted when deleting all metadata from MP3."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"}, "mp3"
        ) as test_file:
            delete_all_metadata(test_file)
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert track_id is None

    def test_vorbis_musicbrainz_trackid_deleted_with_all_metadata(self):
        """Test that MusicBrainz Track ID is deleted when deleting all metadata from FLAC."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}, "flac"
        ) as test_file:
            delete_all_metadata(test_file)
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert track_id is None

    def test_riff_musicbrainz_trackid_deleted_with_all_metadata(self):
        """Test that MusicBrainz Track ID is deleted when deleting all metadata from WAV."""
        with temp_file_with_metadata(
            {"musicbrainz_trackid": "12345678-1234-5678-9abc-def123456789"}, "wav"
        ) as test_file:
            delete_all_metadata(test_file)
            track_id = get_unified_metadata_field(test_file, UnifiedMetadataKey.MUSICBRAINZ_TRACKID)
            assert track_id is None
