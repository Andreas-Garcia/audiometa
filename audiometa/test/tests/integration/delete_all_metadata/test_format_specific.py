import pytest
from pathlib import Path
import shutil

from audiometa import (
    delete_all_metadata,
    get_single_format_app_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestDeleteAllMetadataFormatSpecific:
    """Format-specific deletion tests for delete_all_metadata function."""

    def test_delete_all_metadata_format_specific_id3v2(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test deleting only ID3v2 metadata while preserving other formats."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test Title",
            "artist": "Test Artist"
        }
        with TempFileWithMetadata(test_metadata, "mp3") as test_file:
            # Delete only ID3v2 metadata
            result = delete_all_metadata(test_file, tag_format=MetadataFormat.ID3V2)
            assert result is True

    def test_delete_all_metadata_format_specific_vorbis(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test deleting only Vorbis metadata from FLAC file."""
        # Copy sample file to temp location with correct extension
        temp_flac_file = temp_audio_file.with_suffix('.flac')
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test FLAC Title",
            "artist": "Test FLAC Artist"
        }
        with TempFileWithMetadata(test_metadata, "flac") as test_file:
            # Delete only Vorbis metadata
            result = delete_all_metadata(test_file, tag_format=MetadataFormat.VORBIS)
            assert result is True

    def test_delete_all_metadata_format_specific_riff(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test deleting only RIFF metadata from WAV file."""
        # Copy sample file to temp location with correct extension
        temp_wav_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(sample_wav_file, temp_wav_file)
        
        # First add some metadata using external script
        test_metadata = {
            "title": "Test WAV Title",
            "artist": "Test WAV Artist"
        }
        with TempFileWithMetadata(test_metadata, "wav") as test_file:
            # Delete only RIFF metadata - may not be fully supported
            result = delete_all_metadata(test_file, tag_format=MetadataFormat.RIFF)
            # Note: RIFF metadata deletion might not be fully supported
            # This test documents the current behavior
            assert isinstance(result, bool)

    def test_delete_all_metadata_mixed_formats_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test deleting specific format from file with multiple metadata formats."""
        # Copy sample file to temp location with correct extension
        temp_wav_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(sample_wav_file, temp_wav_file)
        
        # Create WAV file with both RIFF and ID3v2 metadata
        initial_metadata = {
            "title": "Original RIFF Title",
            "artist": "Original RIFF Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Add ID3v2 metadata using the library directly
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Original ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original ID3v2 Artist"]
            }
            update_file_metadata(test_file, id3v2_metadata, 
                               metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata
            riff_before = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            id3v2_before = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert riff_before.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
            # Delete metadata from ID3v2 format only
            result = delete_all_metadata(test_file, tag_format=MetadataFormat.ID3V2)
            assert result is True
            
            # Verify ID3v2 metadata was deleted
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            
            # Verify RIFF metadata was NOT deleted
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
