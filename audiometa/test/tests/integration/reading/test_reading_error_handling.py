import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestReadingErrorHandling:

    def test_unsupported_file_type_raises_error(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_merged_unified_metadata(str(temp_audio_file))
