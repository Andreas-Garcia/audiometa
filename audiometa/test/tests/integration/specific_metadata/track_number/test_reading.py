

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestTrackNumberReading:
    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v1") as test_file:
            test_file.set_id3v1_max_metadata()
            track_number = get_specific_metadata(test_file.path, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == "1"

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_max_metadata()
            track_number = get_specific_metadata(test_file.path, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == "99/99"

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_max_metadata()
            track_number = get_specific_metadata(test_file.path, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number == "99"

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            track_number = get_specific_metadata(test_file.path, UnifiedMetadataKey.TRACK_NUMBER)
            assert track_number is None
