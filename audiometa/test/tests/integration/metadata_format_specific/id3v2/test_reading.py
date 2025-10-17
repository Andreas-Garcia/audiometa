

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.tests.script_helpers import Id3v2Helper


@pytest.mark.integration
class TestId3v2Reading:

    def test_id3v2_extended_metadata(self, metadata_id3v2_small_mp3, metadata_id3v2_big_mp3):
        # Small ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles
        
        # Big ID3v2 file
        metadata = get_merged_unified_metadata(metadata_id3v2_big_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert len(title) > 30  # ID3v2 can have longer titles

    def test_id3v2_metadata_reading_mp3(self, metadata_id3v2_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30

    def test_id3v2_metadata_reading_flac(self, metadata_id3v2_small_flac):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_flac)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_id3v2_metadata_reading_wav(self, metadata_id3v2_small_wav):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata

    def test_single_format_id3v2_extraction(self, metadata_id3v2_small_mp3):
        id3v2_metadata = get_single_format_app_metadata(metadata_id3v2_small_mp3, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        assert UnifiedMetadataKey.TITLE in id3v2_metadata

    def test_audio_file_object_reading(self, metadata_id3v2_small_mp3):
        audio_file = AudioFile(metadata_id3v2_small_mp3)
        
        # Test merged metadata
        metadata = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        
        # Test specific metadata
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        
        # Test single format metadata
        id3v2_metadata = get_single_format_app_metadata(audio_file, MetadataFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)

    def test_wav_with_id3v2_and_riff_metadata(self, metadata_id3v2_and_riff_small_wav):
        # Test that we can read metadata from a WAV file with both ID3v2 and RIFF metadata
        metadata = get_merged_unified_metadata(metadata_id3v2_and_riff_small_wav)
        assert isinstance(metadata, dict)
        assert UnifiedMetadataKey.TITLE in metadata
        # ID3v2 can have longer titles than ID3v1
        assert len(metadata[UnifiedMetadataKey.TITLE]) > 30
        
        # Test that the file can be processed without errors
        # This verifies that our fix for handling ID3v2 metadata in WAV files works correctly
        audio_file = AudioFile(metadata_id3v2_and_riff_small_wav)
        metadata_from_audio_file = get_merged_unified_metadata(audio_file)
        assert isinstance(metadata_from_audio_file, dict)
        assert UnifiedMetadataKey.TITLE in metadata_from_audio_file

    def test_id3v2_error_handling(self, temp_audio_file: Path):
        # Test ID3v2 with unsupported file type
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(str(temp_audio_file), MetadataFormat.ID3V2)

    def test_wav_with_id3v2_and_id3v1_metadata(self):
        # Create a WAV file with both ID3v2 and ID3v1 metadata
        with TempFileWithMetadata({}, "wav") as test_file:
            # First, add ID3v2 metadata using the script helper
            Id3v2Helper.set_max_metadata(test_file.path)
            
            # Then add ID3v1 metadata using the library
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Album"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Test that we can read both ID3v2 and ID3v1 metadata
            id3v2_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_metadata_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            # Verify ID3v2 metadata is present
            assert id3v2_metadata_result is not None
            assert UnifiedMetadataKey.TITLE in id3v2_metadata_result
            # ID3v2 title should be the long one from the script
            assert len(id3v2_metadata_result[UnifiedMetadataKey.TITLE]) > 30
            
            # Verify ID3v1 metadata is present
            assert id3v1_metadata_result is not None
            assert UnifiedMetadataKey.TITLE in id3v1_metadata_result
            assert id3v1_metadata_result[UnifiedMetadataKey.TITLE] == "ID3v1 Title"
            
            # Test merged metadata (should prioritize ID3v2 over ID3v1)
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata is not None
            assert UnifiedMetadataKey.TITLE in merged_metadata
            # Should prefer ID3v2 title since it's more comprehensive
            assert len(merged_metadata[UnifiedMetadataKey.TITLE]) > 30
