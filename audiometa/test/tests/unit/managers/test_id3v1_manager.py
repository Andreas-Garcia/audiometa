

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.id3v1.Id3v1Manager import Id3v1Manager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import MetadataNotSupportedError


@pytest.mark.unit
class TestId3v1Manager:

    def test_id3v1_manager_mp3(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v1_manager_flac(self, sample_flac_file: Path):
        audio_file = AudioFile(sample_flac_file)
        manager = Id3v1Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v1_manager_get_specific_metadata(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        title = manager.get_app_specific_metadata(UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_id3v1_manager_no_write_support(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v1 Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Test Album"
        }
        
        # ID3v1 manager should raise error when trying to update metadata
        with pytest.raises(MetadataNotSupportedError):
            manager.update_file_metadata(test_metadata)
