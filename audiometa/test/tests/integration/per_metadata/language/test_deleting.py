import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestLanguageDeleting:
    def test_delete_language_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) == "en"
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_id3v1(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) == "en"
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.LANGUAGE) == "en"
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.LANGUAGE: "en"}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.LANGUAGE) == "en"
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_preserves_other_fields(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {
            UnifiedMetadataKey.LANGUAGE: "en",
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
        })
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: None})
        
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) is None
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Test Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_language_already_none(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_empty_string(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: ""})
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.LANGUAGE: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE) is None
