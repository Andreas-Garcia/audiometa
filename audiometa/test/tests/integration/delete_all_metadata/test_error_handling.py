import pytest
from pathlib import Path

from audiometa import delete_all_metadata
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestDeleteAllMetadataErrorHandling:

    def test_delete_all_metadata_unsupported_file_type(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_all_metadata(str(temp_audio_file))

    def test_delete_all_metadata_nonexistent_file(self):
        nonexistent_file = "nonexistent_file.mp3"
        
        with pytest.raises(FileNotFoundError):
            delete_all_metadata(nonexistent_file)
