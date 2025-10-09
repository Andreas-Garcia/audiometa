

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.rating_supporting.RiffManager import RiffManager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError, MetadataNotSupportedError


@pytest.mark.unit
class TestRiffManager:

    def test_riff_manager_wav(self, sample_wav_file: Path):
        audio_file = AudioFile(sample_wav_file)
        manager = RiffManager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_riff_manager_unsupported_format(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            RiffManager(audio_file)

    def test_riff_manager_update_metadata(self, sample_wav_file: Path, temp_wav_file: Path):
        import shutil
        shutil.copy2(sample_wav_file, temp_wav_file)
        
        audio_file = AudioFile(temp_wav_file)
        manager = RiffManager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "RIFF Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "RIFF Test Album"
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "RIFF Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["RIFF Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "RIFF Test Album"

    def test_riff_manager_rating_not_supported(self, sample_wav_file: Path, temp_wav_file: Path):
        import shutil
        shutil.copy2(sample_wav_file, temp_wav_file)
        
        audio_file = AudioFile(temp_wav_file)
        manager = RiffManager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "RIFF Test Title",
            UnifiedMetadataKey.RATING: 85  # RIFF doesn't support rating
        }
        
        # This should raise an exception for unsupported rating
        with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.RATING metadata not supported by RIFF format"):
            manager.update_file_metadata(test_metadata)
