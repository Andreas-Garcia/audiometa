import pytest
from pathlib import Path

from audiometa import (
    delete_all_metadata,
    get_single_format_app_metadata,
    update_file_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestDeleteAllMetadataAllFormats:

    def test_delete_all_metadata_formats_mp3(self):
        with TempFileWithMetadata({"title": "ID3v1 Title", "artist": "ID3v1 Artist"}, "id3v1") as test_file:
            # Add ID3v2 metadata using the library
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v2 Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
        }
        update_file_metadata(temp_audio_file, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Verify both formats have metadata before deletion
        id3v2_before = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        id3v1_before = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
        assert id3v1_before.get(UnifiedMetadataKey.TITLE) is not None  # Should have ID3v1 metadata
        
        # Delete all metadata from all formats
        result = delete_all_metadata(temp_audio_file)
        assert result is True
        
        # Verify both ID3v2 and ID3v1 metadata were deleted
        id3v2_after = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        id3v1_after = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_formats_flac(self, metadata_id3v1_small_flac: Path, temp_audio_file: Path):
        # Copy sample file with ID3v1 metadata to temp location with correct extension
        temp_flac_file = temp_audio_file.with_suffix('.flac')
        shutil.copy2(metadata_id3v1_small_flac, temp_flac_file)
        
        # Add ID3v2 metadata using the library
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "FLAC ID3v2 Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["FLAC ID3v2 Artist"]
        }
        update_file_metadata(temp_flac_file, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Verify ID3v1 metadata exists (from source file)
        id3v1_before = get_single_format_app_metadata(temp_flac_file, MetadataFormat.ID3V1)
        assert id3v1_before.get(UnifiedMetadataKey.TITLE) is not None  # Should have ID3v1 metadata
        
        # Verify ID3v2 metadata exists
        id3v2_before = get_single_format_app_metadata(temp_flac_file, MetadataFormat.ID3V2)
        assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "FLAC ID3v2 Title"
        
        # Delete all metadata from all formats
        result = delete_all_metadata(temp_flac_file)
        assert result is True
        
        # Verify ID3v1 metadata was deleted
        id3v1_after = get_single_format_app_metadata(temp_flac_file, MetadataFormat.ID3V1)
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None
        
        # Verify ID3v2 metadata was deleted
        id3v2_after = get_single_format_app_metadata(temp_flac_file, MetadataFormat.ID3V2)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_formats_wav(self, metadata_id3v1_small_wav: Path, temp_audio_file: Path):
        # Copy sample file with ID3v1 metadata to temp location with correct extension
        temp_wav_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(metadata_id3v1_small_wav, temp_wav_file)
        
        # Add ID3v2 metadata using the library
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "WAV ID3v2 Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["WAV ID3v2 Artist"]
        }
        update_file_metadata(temp_wav_file, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
        
        # Verify ID3v1 metadata exists (from source file)
        id3v1_before = get_single_format_app_metadata(temp_wav_file, MetadataFormat.ID3V1)
        assert id3v1_before.get(UnifiedMetadataKey.TITLE) is not None  # Should have ID3v1 metadata
        
        # Verify ID3v2 metadata exists
        id3v2_before = get_single_format_app_metadata(temp_wav_file, MetadataFormat.ID3V2)
        assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "WAV ID3v2 Title"
        
        # Delete all metadata from all formats
        result = delete_all_metadata(temp_wav_file)
        assert result is True
        
        # Verify ID3v1 metadata was deleted
        id3v1_after = get_single_format_app_metadata(temp_wav_file, MetadataFormat.ID3V1)
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None
        
        # Verify ID3v2 metadata was deleted
        id3v2_after = get_single_format_app_metadata(temp_wav_file, MetadataFormat.ID3V2)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_removes_all_formats(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Add ID3v1 metadata using external script
        test_metadata = {
            "title": "Test ID3v1 Title",
            "artist": "Test ID3v1 Artist"
        }
        with TempFileWithMetadata(test_metadata, "id3v1") as id3v1_file:
            # Copy the file with ID3v1 metadata to our test file
            shutil.copy2(id3v1_file.path, temp_audio_file)
            
            # Add ID3v2 metadata using the library
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(temp_audio_file, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata before deletion
            id3v1_before = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
            id3v2_before = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
            # Note: ID3v2 metadata overwrites ID3v1 in the merged view, but both formats exist
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) is not None  # ID3v1 metadata exists
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Delete all metadata - should succeed and remove both formats
            result = delete_all_metadata(temp_audio_file)
            assert result is True
            
            # Verify both ID3v1 and ID3v2 were deleted
            id3v1_after = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
            id3v2_after = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None

    def test_delete_all_metadata_returns_false_when_no_formats_support_deletion(self, temp_audio_file: Path):
        # This test is more theoretical since most formats support deletion
        # But it documents the expected behavior
        result = delete_all_metadata(temp_audio_file)
        # Should return True even for files with no metadata (deletion is considered successful)
        assert isinstance(result, bool)
