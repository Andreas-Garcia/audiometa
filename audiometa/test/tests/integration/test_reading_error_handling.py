import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
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

    def test_nonexistent_file_raises_error(self):
        nonexistent_file = "nonexistent_file.mp3"
        
        with pytest.raises(FileNotFoundError):
            get_merged_unified_metadata(nonexistent_file)
        
        with pytest.raises(FileNotFoundError):
            get_single_format_app_metadata(nonexistent_file, MetadataFormat.ID3V2)
        
        with pytest.raises(FileNotFoundError):
            get_specific_metadata(nonexistent_file, UnifiedMetadataKey.TITLE)

    def test_invalid_metadata_key_returns_none(self, sample_mp3_file: Path):
        # This should not raise an error, but return None
        invalid_key = "INVALID_KEY"
        result = get_specific_metadata(sample_mp3_file, invalid_key)
        assert result is None

    def test_invalid_format_raises_error(self, sample_mp3_file: Path):
        # Try to get Vorbis metadata from MP3 file (should raise error)
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(sample_mp3_file, MetadataFormat.VORBIS)
        
        # Try to get RIFF metadata from MP3 file (should raise error)
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(sample_mp3_file, MetadataFormat.RIFF)
