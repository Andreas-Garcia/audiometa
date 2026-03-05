import json
import subprocess
import sys

import pytest

from audiometa.test.helpers.temp_file_with_metadata import temp_file_with_metadata
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey


@pytest.mark.e2e
class TestCLIReadComprehensive:
    def test_cli_read_all_fields_comprehensive_mp3(self):
        with temp_file_with_metadata(
            {
                "title": "Comprehensive Test Title",
                "artist": ["Artist One", "Artist Two"],
                "album": "Test Album",
                "album_artist": ["Album Artist"],
                "year": "2024",
                "genre": ["Rock", "Blues"],
                "track": "5/12",
                "disc_number": 1,
                "disc_total": 2,
                "rating": 85,
                "bpm": 120,
                "language": "eng",
                "composer": ["Composer One", "Composer Two"],
                "publisher": "Test Publisher",
                "copyright": "© 2024",
                "lyrics": "Test lyrics",
                "comment": "Test comment",
                "isrc": "USRC17607839",
                "musicbrainz_trackid": "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                "musicbrainz_artistids": [
                    "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                    "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                ],
            },
            "mp3",
        ) as test_file:
            result = subprocess.run(
                [sys.executable, "-m", "audiometa", "read", str(test_file), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0
            data = json.loads(result.stdout)
            unified = data.get("unified_metadata", {})

            assert unified.get(UnifiedMetadataKey.TITLE.value) == "Comprehensive Test Title"
            assert unified.get(UnifiedMetadataKey.ARTISTS.value) == ["Artist One", "Artist Two"]
            assert unified.get(UnifiedMetadataKey.ALBUM.value) == "Test Album"
            assert unified.get(UnifiedMetadataKey.ALBUM_ARTISTS.value) == ["Album Artist"]
            assert unified.get(UnifiedMetadataKey.RELEASE_DATE.value) == "2024"
            assert unified.get(UnifiedMetadataKey.GENRES_NAMES.value) == ["Rock", "Blues"]
            assert unified.get(UnifiedMetadataKey.TRACK_NUMBER.value) == "5/12"
            assert unified.get(UnifiedMetadataKey.DISC_NUMBER.value) == 1
            assert unified.get(UnifiedMetadataKey.DISC_TOTAL.value) == 2
            assert unified.get(UnifiedMetadataKey.RATING.value) == 85
            assert unified.get(UnifiedMetadataKey.BPM.value) == 120
            assert unified.get(UnifiedMetadataKey.LANGUAGE.value) == "eng"
            assert unified.get(UnifiedMetadataKey.COMPOSERS.value) == ["Composer One", "Composer Two"]
            assert unified.get(UnifiedMetadataKey.PUBLISHER.value) == "Test Publisher"
            assert unified.get(UnifiedMetadataKey.COPYRIGHT.value) == "© 2024"
            assert unified.get(UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS.value) == "Test lyrics"
            assert unified.get(UnifiedMetadataKey.COMMENT.value) == "Test comment"
            assert unified.get(UnifiedMetadataKey.ISRC.value) == "USRC17607839"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value) == "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value) == [
                "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            ]
            # REPLAYGAIN and ARCHIVAL_LOCATION are not supported by ID3v2 format (MP3)

    def test_cli_read_all_fields_comprehensive_flac(self):
        with temp_file_with_metadata(
            {
                "title": "FLAC Comprehensive Test",
                "artist": ["FLAC Artist"],
                "album": "FLAC Album",
                "track_number": "3/10",
                "disc_number": 1,
                "disc_total": 2,
                "bpm": 140,
                "language": "eng",
                "composer": ["FLAC Composer"],
                "publisher": "FLAC Publisher",
                "copyright": "© FLAC",
                "lyrics": "FLAC lyrics",
                "comment": "FLAC comment",
                "description": "FLAC description",
                "replaygain": "+2.5 dB",
                "isrc": "FRXXX1800001",
                "musicbrainz_trackid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "musicbrainz_artistids": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
            },
            "flac",
        ) as test_file:
            result = subprocess.run(
                [sys.executable, "-m", "audiometa", "read", str(test_file), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0
            data = json.loads(result.stdout)
            unified = data.get("unified_metadata", {})

            assert unified.get(UnifiedMetadataKey.TITLE.value) == "FLAC Comprehensive Test"
            assert unified.get(UnifiedMetadataKey.ARTISTS.value) == ["FLAC Artist"]
            assert unified.get(UnifiedMetadataKey.ALBUM.value) == "FLAC Album"
            assert unified.get(UnifiedMetadataKey.TRACK_NUMBER.value) == "3/10"
            assert unified.get(UnifiedMetadataKey.DISC_NUMBER.value) == 1
            assert unified.get(UnifiedMetadataKey.DISC_TOTAL.value) == 2
            assert unified.get(UnifiedMetadataKey.BPM.value) == 140
            assert unified.get(UnifiedMetadataKey.LANGUAGE.value) == "eng"
            assert unified.get(UnifiedMetadataKey.COMPOSERS.value) == ["FLAC Composer"]
            assert unified.get(UnifiedMetadataKey.PUBLISHER.value) == "FLAC Publisher"
            assert unified.get(UnifiedMetadataKey.COPYRIGHT.value) == "© FLAC"
            assert unified.get(UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS.value) == "FLAC lyrics"
            assert unified.get(UnifiedMetadataKey.COMMENT.value) == "FLAC comment"
            assert unified.get(UnifiedMetadataKey.DESCRIPTION.value) == "FLAC description"
            assert unified.get(UnifiedMetadataKey.REPLAYGAIN.value) == "+2.5 dB"
            assert unified.get(UnifiedMetadataKey.ISRC.value) == "FRXXX1800001"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value) == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value) == [
                "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            ]
            # ARCHIVAL_LOCATION is not supported by Vorbis format (FLAC)

    def test_cli_read_all_fields_comprehensive_wav(self):
        with temp_file_with_metadata(
            {
                "title": "WAV Comprehensive Test",
                "artist": ["WAV Artist"],
                "album": "WAV Album",
                "year": "2024",
                "genre": ["Rock"],
                "rating": 100,
                "bpm": 120,
                "language": "eng",
                "composer": ["WAV Composer"],
                "copyright": "© WAV",
                "comment": "WAV comment",
                "description": "WAV description",
                "originator": "WAV originator",
                "isrc": "GBUM71505078",
                "musicbrainz_trackid": "12345678-1234-5678-9abc-def123456789",
                "musicbrainz_artistids": ["12345678-1234-5678-9abc-def123456789"],
            },
            "wav",
        ) as test_file:
            result = subprocess.run(
                [sys.executable, "-m", "audiometa", "read", str(test_file), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0
            data = json.loads(result.stdout)
            unified = data.get("unified_metadata", {})

            assert unified.get(UnifiedMetadataKey.TITLE.value) == "WAV Comprehensive Test"
            assert unified.get(UnifiedMetadataKey.ARTISTS.value) == ["WAV Artist"]
            assert unified.get(UnifiedMetadataKey.ALBUM.value) == "WAV Album"
            assert unified.get(UnifiedMetadataKey.RELEASE_DATE.value) == "2024"
            assert unified.get(UnifiedMetadataKey.GENRES_NAMES.value) == ["Rock"]
            assert unified.get(UnifiedMetadataKey.RATING.value) == 100
            assert unified.get(UnifiedMetadataKey.BPM.value) == 120
            assert unified.get(UnifiedMetadataKey.LANGUAGE.value) == "eng"
            assert unified.get(UnifiedMetadataKey.COMPOSERS.value) == ["WAV Composer"]
            assert unified.get(UnifiedMetadataKey.COPYRIGHT.value) == "© WAV"
            assert unified.get(UnifiedMetadataKey.COMMENT.value) == "WAV comment"
            assert unified.get(UnifiedMetadataKey.DESCRIPTION.value) == "WAV description"
            assert unified.get(UnifiedMetadataKey.ORIGINATOR.value) == "WAV originator"
            assert unified.get(UnifiedMetadataKey.ISRC.value) == "GBUM71505078"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value) == "12345678-1234-5678-9abc-def123456789"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value) == [
                "12345678-1234-5678-9abc-def123456789"
            ]

    def test_cli_read_comprehensive_roundtrip(self):
        """Test that we can write all fields via CLI and read them back correctly."""
        with temp_file_with_metadata({}, "mp3") as test_file:
            write_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "audiometa",
                    "write",
                    str(test_file),
                    "--title",
                    "Roundtrip Test",
                    "--artist",
                    "Roundtrip Artist One",
                    "--artist",
                    "Roundtrip Artist Two",
                    "--album",
                    "Roundtrip Album",
                    "--album-artist",
                    "Roundtrip Album Artist",
                    "--year",
                    "2024",
                    "--genre",
                    "Rock",
                    "--genre",
                    "Blues",
                    "--track-number",
                    "5/12",
                    "--disc-number",
                    "1",
                    "--disc-total",
                    "2",
                    "--rating",
                    "85",
                    "--bpm",
                    "120",
                    "--language",
                    "eng",
                    "--composer",
                    "Roundtrip Composer",
                    "--publisher",
                    "Roundtrip Publisher",
                    "--copyright",
                    "© Roundtrip",
                    "--lyrics",
                    "Roundtrip lyrics",
                    "--comment",
                    "Roundtrip comment",
                    "--isrc",
                    "USRC17607839",
                    "--musicbrainz-track-id",
                    "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                    "--musicbrainz-artist-ids",
                    "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            assert write_result.returncode == 0

            read_result = subprocess.run(
                [sys.executable, "-m", "audiometa", "read", str(test_file), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            assert read_result.returncode == 0
            data = json.loads(read_result.stdout)
            unified = data.get("unified_metadata", {})

            assert unified.get(UnifiedMetadataKey.TITLE.value) == "Roundtrip Test"
            assert unified.get(UnifiedMetadataKey.ARTISTS.value) == ["Roundtrip Artist One", "Roundtrip Artist Two"]
            assert unified.get(UnifiedMetadataKey.ALBUM.value) == "Roundtrip Album"
            assert unified.get(UnifiedMetadataKey.ALBUM_ARTISTS.value) == ["Roundtrip Album Artist"]
            assert unified.get(UnifiedMetadataKey.RELEASE_DATE.value) == "2024"
            assert unified.get(UnifiedMetadataKey.GENRES_NAMES.value) == ["Rock", "Blues"]
            assert unified.get(UnifiedMetadataKey.TRACK_NUMBER.value) == "5/12"
            assert unified.get(UnifiedMetadataKey.DISC_NUMBER.value) == 1
            assert unified.get(UnifiedMetadataKey.DISC_TOTAL.value) == 2
            assert unified.get(UnifiedMetadataKey.RATING.value) == 85
            assert unified.get(UnifiedMetadataKey.BPM.value) == 120
            assert unified.get(UnifiedMetadataKey.LANGUAGE.value) == "eng"
            assert unified.get(UnifiedMetadataKey.COMPOSERS.value) == ["Roundtrip Composer"]
            assert unified.get(UnifiedMetadataKey.PUBLISHER.value) == "Roundtrip Publisher"
            assert unified.get(UnifiedMetadataKey.COPYRIGHT.value) == "© Roundtrip"
            assert unified.get(UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS.value) == "Roundtrip lyrics"
            assert unified.get(UnifiedMetadataKey.COMMENT.value) == "Roundtrip comment"
            assert unified.get(UnifiedMetadataKey.ISRC.value) == "USRC17607839"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_TRACKID.value) == "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
            assert unified.get(UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS.value) == [
                "9d6f6f7c-9d52-4c76-8f9e-01d18d8f8ec6"
            ]
