
import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestLanguageWriting:
    def test_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_language = "en"
            test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V2)
            language = get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE)
            assert language == test_language

    def test_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_language = "fr"
            test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.RIFF)
            language = get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE)
            assert language == test_language

    def test_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_language = "de"
            test_metadata = {UnifiedMetadataKey.LANGUAGE: test_language}
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.VORBIS)
            language = get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE)
            assert language == test_language
