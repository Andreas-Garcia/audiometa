

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestReleaseDateReading:
    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v1") as test_file:
            test_file.set_id3v1_max_metadata()
            release_date = get_specific_metadata(test_file.path, UnifiedMetadataKey.RELEASE_DATE)
            assert release_date is None

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_max_metadata()
            release_date = get_specific_metadata(test_file.path, UnifiedMetadataKey.RELEASE_DATE)
            assert release_date == "9999-12-31"

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_max_metadata()
            release_date = get_specific_metadata(test_file.path, UnifiedMetadataKey.RELEASE_DATE)
            assert release_date == "9999"

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            release_date = get_specific_metadata(test_file.path, UnifiedMetadataKey.RELEASE_DATE)
            assert release_date is None
