
import pytest

from audiometa import get_unified_metadata_field
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestLyricsReading:
    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v1") as test_file:
            lyrics = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LYRICS)
            assert lyrics is None

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_max_metadata()
            lyrics = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LYRICS)
            assert lyrics == "a" * 4000

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_max_metadata()
            lyrics = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LYRICS)
            assert lyrics is None

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            lyrics = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LYRICS)
            assert lyrics is None
