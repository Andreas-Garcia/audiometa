import pytest

from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.id3v2 import ID3v2MetadataGetter
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_unified_metadata_field, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestComposerDeleting:
    def test_delete_composer_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.COMPOSERS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: ["Test Composer"]}, metadata_format=MetadataFormat.ID3V1)
    
    def test_delete_composer_id3v2(self):
        with TempFileWithMetadata({"composer": "Test Composer"}, "id3v2.4") as test_file:
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path, version="2.4")
            assert raw_metadata['TCOM'] == ["Test Composer"]
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) is None

    def test_delete_composer_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: ["Test Composer"]}, metadata_format=MetadataFormat.RIFF)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) == ["Test Composer"]
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: None}, metadata_format=MetadataFormat.RIFF)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) is None

    def test_delete_composer_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: ["Test Composer"]}, metadata_format=MetadataFormat.VORBIS)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) == ["Test Composer"]
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) is None

    def test_delete_composer_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {
                UnifiedMetadataKey.COMPOSERS: ["Test Composer"],
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS: ["Test Artist"]
            })
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: None})
        
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) is None
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS) == ["Test Artist"]

    def test_delete_composer_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: None})
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) is None

    def test_delete_composer_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: [""]})
            update_metadata(test_file.path, {UnifiedMetadataKey.COMPOSERS: None})
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.COMPOSERS) is None
