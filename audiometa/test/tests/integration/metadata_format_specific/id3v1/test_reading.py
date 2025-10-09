

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestId3v1Reading:

    def test_id3v1_limitations(self, metadata_id3v1_small_mp3, metadata_id3v1_big_mp3):
        # Small ID3v1 file
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit
        
        # Big ID3v1 file (should still be limited)
        metadata = get_merged_unified_metadata(metadata_id3v1_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) == 30  # ID3v1 title limit

    def test_id3v1_metadata_reading_mp3(self, metadata_id3v1_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        assert metadata[UnifiedMetadataKey.TITLE] == 'a' * 30  # ID3v1 title limit

    def test_id3v1_metadata_reading_flac(self, metadata_id3v1_small_flac):
        metadata = get_merged_unified_metadata(metadata_id3v1_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_id3v1_metadata_reading_wav(self, metadata_id3v1_small_wav):
        metadata = get_merged_unified_metadata(metadata_id3v1_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_metadata_none_files(self, metadata_none_mp3):
        # MP3 with no metadata
        metadata = get_merged_unified_metadata(metadata_none_mp3)
        assert isinstance(metadata, dict)
        # Should have minimal or no metadata
        assert not metadata.get(UnifiedMetadataKey.TITLE) or metadata.get(UnifiedMetadataKey.TITLE) == ""

    def test_audio_file_object_reading(self, metadata_id3v1_small_mp3):
        audio_file = AudioFile(metadata_id3v1_small_mp3)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
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
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V1)
