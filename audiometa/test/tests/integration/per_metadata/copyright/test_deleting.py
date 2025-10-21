import pytest



from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_specific_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestCopyrightDeleting:
    def test_delete_copyright_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: "Test Copyright"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) == "Test Copyright"
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None

    def test_delete_copyright_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: "Test Copyright"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) == "Test Copyright"
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None

    def test_delete_copyright_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: "Test Copyright"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) == "Test Copyright"
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None

    def test_delete_copyright_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: "Test Copyright"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) == "Test Copyright"
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None

    def test_delete_copyright_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {
                UnifiedMetadataKey.COPYRIGHT: "Test Copyright",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_copyright_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None

    def test_delete_copyright_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: ""})
            update_metadata(test_file.path, {UnifiedMetadataKey.COPYRIGHT: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COPYRIGHT) is None
