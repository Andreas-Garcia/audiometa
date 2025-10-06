import pytest
from pathlib import Path

from audiometa import (
    update_file_metadata,
    delete_metadata
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestWritingErrorHandling:

    def test_unsupported_file_type_raises_error(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), {UnifiedMetadataKey.TITLE: "Test"})
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_metadata(str(temp_audio_file))

    def test_nonexistent_file_raises_error(self):
        nonexistent_file = "nonexistent_file.mp3"
        
        with pytest.raises(FileNotFoundError):
            update_file_metadata(nonexistent_file, {UnifiedMetadataKey.TITLE: "Test"})
        
        with pytest.raises(FileNotFoundError):
            delete_metadata(nonexistent_file)
