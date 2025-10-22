

import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestId3v1Reading:

    def test_audio_file_object_reading(self, metadata_id3v1_small_mp3):
        audio_file = AudioFile(metadata_id3v1_small_mp3)
        
        # Test merged metadata
        metadata = get_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # Test specific metadata
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)

    def test_id3v1_error_handling(self, temp_audio_file: Path):
        # Test ID3v1 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_unified_metadata(str(temp_audio_file), metadata_format=MetadataFormat.ID3V1)
