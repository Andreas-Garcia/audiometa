
import pytest
import shutil

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestCommentReading:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_comment = "Test Comment ID3v2"
        test_metadata = {UnifiedMetadataKey.COMMENT: test_comment}
        from audiometa import update_file_metadata
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        comment = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT)
        assert comment == test_comment

    def test_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_comment = "Test Comment RIFF"
        test_metadata = {UnifiedMetadataKey.COMMENT: test_comment}
        from audiometa import update_file_metadata
        update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)
        comment = get_specific_metadata(temp_wav_file, UnifiedMetadataKey.COMMENT)
        assert comment == test_comment

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_comment = "Test Comment Vorbis"
        test_metadata = {UnifiedMetadataKey.COMMENT: test_comment}
        from audiometa import update_file_metadata
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        comment = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.COMMENT)
        assert comment == test_comment

    def test_id3v1(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_comment = "Test Comment ID3v1"
        test_metadata = {UnifiedMetadataKey.COMMENT: test_comment}
        from audiometa import update_file_metadata
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V1)
        comment = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMMENT)
        assert comment == test_comment
