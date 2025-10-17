import pytest



from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestCommentDeleting:
    def test_delete_comment_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.COMMENT: "Test comment",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_comment_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: ""})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.COMMENT: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None
