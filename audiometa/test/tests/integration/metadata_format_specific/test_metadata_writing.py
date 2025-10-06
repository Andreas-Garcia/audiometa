"""Tests for general metadata writing functionality."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    update_file_metadata,
    delete_metadata,
    get_merged_unified_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError, MetadataNotSupportedError


@pytest.mark.integration
class TestMetadataWriting:

    def test_update_file_metadata_basic_functionality(self, sample_mp3_file: Path, sample_flac_file: Path, sample_wav_file: Path, temp_audio_file: Path):
        test_cases = [
            (sample_mp3_file, {
                UnifiedMetadataKey.TITLE: "Test MP3 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test MP3 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test MP3 Album",
                UnifiedMetadataKey.RATING: 85
            }),
            (sample_flac_file, {
                UnifiedMetadataKey.TITLE: "Test FLAC Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test FLAC Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test FLAC Album"
            }),
            (sample_wav_file, {
                UnifiedMetadataKey.TITLE: "Test WAV Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test WAV Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test WAV Album"
            })
        ]
        
        for sample_file, test_metadata in test_cases:
            # Copy sample file to temp location
            shutil.copy2(sample_file, temp_audio_file)
            
            # Update metadata
            update_file_metadata(temp_audio_file, test_metadata)
            
            # Verify metadata was written
            updated_metadata = get_merged_unified_metadata(temp_audio_file)
            for key, expected_value in test_metadata.items():
                assert updated_metadata.get(key) == expected_value

    def test_update_file_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title with AudioFile",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist with AudioFile"]
        }
        
        # Update metadata
        update_file_metadata(audio_file, test_metadata)
        
        # Verify metadata was written
        updated_metadata = get_merged_unified_metadata(audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title with AudioFile"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist with AudioFile"]

    def test_update_file_metadata_unsupported_field(self, sample_wav_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support BPM in RIFF format
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.BPM: 120  # This should be ignored for WAV files
        }
        
        # This should not raise an error, but BPM should be ignored
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify only supported metadata was written
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
        # BPM should not be present for WAV files
        assert UnifiedMetadataKey.BPM not in updated_metadata

    def test_delete_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # First add some metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Test Title to Delete",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist to Delete"]
        }
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was added
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Test Title to Delete"
        
        # Delete metadata
        result = delete_metadata(temp_audio_file)
        assert result is True
        
        # Verify metadata was deleted (should be empty or minimal)
        deleted_metadata = get_merged_unified_metadata(temp_audio_file)
        # After deletion, metadata should be empty or contain only technical info
        assert UnifiedMetadataKey.TITLE not in deleted_metadata or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Test Title to Delete"

    def test_delete_metadata_with_specific_format(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Delete only ID3v2 metadata
        result = delete_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert result is True

    def test_delete_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        result = delete_metadata(audio_file)
        assert result is True

    def test_update_metadata_unsupported_file_type(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        test_metadata = {UnifiedMetadataKey.TITLE: "Test Title"}
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), test_metadata)

    def test_delete_metadata_unsupported_file_type(self, temp_audio_file: Path):
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            delete_metadata(str(temp_audio_file))

    def test_write_metadata_to_files_with_existing_metadata(self, metadata_id3v2_small_mp3, metadata_vorbis_small_flac, metadata_riff_small_wav, temp_audio_file):
        test_cases = [
            (metadata_id3v2_small_mp3, {
                UnifiedMetadataKey.TITLE: "Updated Title MP3",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Updated Artist MP3"],
                UnifiedMetadataKey.ALBUM_NAME: "Updated Album MP3",
                UnifiedMetadataKey.RATING: 6
            }),
            (metadata_vorbis_small_flac, {
                UnifiedMetadataKey.TITLE: "Updated Title FLAC",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Updated Artist FLAC"],
                UnifiedMetadataKey.ALBUM_NAME: "Updated Album FLAC",
                UnifiedMetadataKey.RATING: 5
            }),
            (metadata_riff_small_wav, {
                UnifiedMetadataKey.TITLE: "Updated Title WAV",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Updated Artist WAV"],
                UnifiedMetadataKey.ALBUM_NAME: "Updated Album WAV"
            })
        ]
        
        for sample_file, test_metadata in test_cases:
            # Copy sample file to temp location
            shutil.copy2(sample_file, temp_audio_file)
            
            # Update metadata
            update_file_metadata(temp_audio_file, test_metadata)
            
            # Verify metadata was written
            updated_metadata = get_merged_unified_metadata(temp_audio_file)
            for key, expected_value in test_metadata.items():
                assert updated_metadata.get(key) == expected_value

    def test_write_metadata_unsupported_fields(self, metadata_none_wav, temp_audio_file):
        shutil.copy2(metadata_none_wav, temp_audio_file)
        
        # WAV doesn't support rating or BPM
        test_metadata = {
            UnifiedMetadataKey.TITLE: "WAV Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["WAV Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "WAV Test Album",
            UnifiedMetadataKey.RATING: 8,  # This should be ignored for WAV
            UnifiedMetadataKey.BPM: 120    # This should be ignored for WAV
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "WAV Test Album"
        # Rating and BPM should not be present for WAV
        assert UnifiedMetadataKey.RATING not in updated_metadata or updated_metadata.get(UnifiedMetadataKey.RATING) != 8
        assert UnifiedMetadataKey.BPM not in updated_metadata or updated_metadata.get(UnifiedMetadataKey.BPM) != 120

    def test_write_metadata_partial_update(self, metadata_id3v2_small_mp3, temp_audio_file):
        shutil.copy2(metadata_id3v2_small_mp3, temp_audio_file)
        
        # Get original metadata
        original_metadata = get_merged_unified_metadata(temp_audio_file)
        original_title = original_metadata.get(UnifiedMetadataKey.TITLE)
        original_album = original_metadata.get(UnifiedMetadataKey.ALBUM_NAME)
        
        # Update only title
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Partial Update Title"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        updated_metadata = get_merged_unified_metadata(temp_audio_file)
        
        # Title should be updated
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Partial Update Title"
        # Other fields should remain unchanged
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == original_album
