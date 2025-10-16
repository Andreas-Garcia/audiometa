import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestCommentDeleting:
    def test_delete_comment_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) == "Test comment"
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_id3v1(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) == "Test comment"
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.COMMENT) == "Test comment"
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.COMMENT: "Test comment"}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.COMMENT) == "Test comment"
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.COMMENT: None}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_preserves_other_fields(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {
            UnifiedMetadataKey.COMMENT: "Test comment",
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
        })
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: None})
        
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) is None
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Test Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_comment_already_none(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_empty_string(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: ""})
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.COMMENT: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT) is None
