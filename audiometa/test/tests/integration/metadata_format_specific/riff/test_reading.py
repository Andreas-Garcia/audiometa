

import pytest
from pathlib import Path

from audiometa import (
    get_unified_metadata,
    get_single_format_app_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestRiffReading:

    def test_riff_metadata_capabilities(self, metadata_riff_small_wav, metadata_riff_big_wav):
        # Small RIFF file
        metadata = get_unified_metadata(metadata_riff_small_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles
        
        # Big RIFF file
        metadata = get_unified_metadata(metadata_riff_big_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # RIFF can have longer titles

    def test_riff_metadata_reading(self, metadata_riff_small_wav):
        metadata = get_unified_metadata(metadata_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # RIFF can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_single_format_riff_extraction(self, metadata_riff_small_wav):
        riff_metadata = get_single_format_app_metadata(metadata_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        assert UnifiedMetadataKey.TITLE in riff_metadata

    def test_metadata_none_files(self, metadata_none_wav):
        # WAV with no metadata
        metadata = get_unified_metadata(metadata_none_wav)
        assert isinstance(metadata, dict)

    def test_audio_file_object_reading(self, metadata_riff_small_wav):
        audio_file = AudioFile(metadata_riff_small_wav)
        
        # Test merged metadata
        metadata = get_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_wav_with_id3v2_and_riff_metadata(self, metadata_id3v2_and_riff_small_wav):
        # Test that we can read metadata from a WAV file with ID3v2 metadata and RIFF structure
        metadata = get_unified_metadata(metadata_id3v2_and_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30
        
        # Test that the RIFF manager can process the file without errors
        # Even if there's no RIFF metadata, the manager should handle the structure gracefully
        riff_metadata = get_single_format_app_metadata(metadata_id3v2_and_riff_small_wav, MetadataFormat.RIFF)
        assert isinstance(riff_metadata, dict)
        # The file may not have RIFF metadata, so we just verify it returns a dict without errors
        
        # Test that the file can be processed using AudioFile object
        audio_file = AudioFile(metadata_id3v2_and_riff_small_wav)
        metadata_from_audio_file = get_unified_metadata(audio_file)
        assert isinstance(metadata_from_audio_file, dict)
        assert UnifiedMetadataKey.TITLE in metadata_from_audio_file

    def test_riff_error_handling(self, temp_audio_file: Path):
        # Test RIFF with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.RIFF)
