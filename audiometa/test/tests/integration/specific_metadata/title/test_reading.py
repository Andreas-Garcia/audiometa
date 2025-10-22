

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestTitleReading:
    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v1") as test_file:
            test_file.set_id3v1_max_metadata()
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == "a" * 30

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_max_metadata()
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == "a" * 1000

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_max_metadata()
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == "a" * 1000

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_max_metadata()
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title == "a" * 1000
