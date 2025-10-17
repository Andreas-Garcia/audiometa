import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestLanguageDeleting:
    def test_delete_language_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_id3v1(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.LANGUAGE: "en",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None})
            
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_language_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: ""})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None
