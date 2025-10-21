

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.id3v1.Id3v1Manager import Id3v1Manager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


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

    def test_id3v1_manager_wav(self, sample_wav_file: Path):
        audio_file = AudioFile(sample_wav_file)
        manager = Id3v1Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v1_manager_get_specific_metadata(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        title = manager.get_app_specific_metadata(UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_id3v1_manager_write_support(self):
        # Copy sample file to temp location for testing
        with TempFileWithMetadata({}, "mp3") as test_file:
            audio_file = AudioFile(test_file.path)
            manager = Id3v1Manager(audio_file)
            
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Test Album"
            }
            
            # ID3v1 manager should successfully update metadata
            manager.update_metadata(test_metadata)
            
            # Verify the metadata was written correctly
            updated_metadata = manager.get_app_metadata()
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v1 Test Title"
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Test Artist"]
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v1 Test Album"

    def test_id3v1_manager_write_unsupported_fields_raises_error(self):
        # Copy sample file to temp location for testing
        with TempFileWithMetadata({}, "mp3") as test_file:
            audio_file = AudioFile(test_file.path)
            manager = Id3v1Manager(audio_file)
            
            # Test unsupported fields that should raise MetadataNotSupportedError
            unsupported_metadata = {
                UnifiedMetadataKey.BPM: 120,  # BPM not supported by ID3v1
                UnifiedMetadataKey.RATING: 85,  # Rating not supported by ID3v1
                UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: ["Album Artist"],  # Album artist not supported by ID3v1
            }
            
            # ID3v1 manager should raise error when trying to write unsupported fields
            with pytest.raises(MetadataNotSupportedError):
                manager.update_metadata(unsupported_metadata)
