"""Tests for SYNC metadata writing strategy.

This module tests the SYNC strategy which writes to native format and
synchronizes other metadata formats that are already present.
"""

import pytest
from pathlib import Path

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata,
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestSyncStrategy:

    def test_sync_strategy_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        # Create test file with basic metadata first
        basic_metadata = {
            "title": "Basic Title",
            "artist": "Basic Artist",
            "album": "Basic Album"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            # First, add ID3v2 metadata using TempFileWithMetadata methods
            test_file.set_id3v2_title("Original ID3v2 Title")
            test_file.set_id3v2_artist("Original ID3v2 Artist")
            test_file.set_id3v2_album("Original ID3v2 Album")
            
            # Verify ID3v2 metadata was written
            id3v2_result = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
            # Now write RIFF metadata with SYNC strategy
            # Note: RiffManager strips ID3v2 tags when writing, so SYNC will only work
            # if we write to ID3v2 format instead of RIFF format
            sync_metadata = {
                UnifiedMetadataKey.TITLE: "Synced Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Synced Album"
            }
            update_file_metadata(test_file, sync_metadata, 
                               metadata_strategy=MetadataWritingStrategy.SYNC)
            
            # Verify both formats have the synced metadata
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            
            # ID3v2 should have the synced metadata
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"
            # RIFF should also have the synced metadata (SYNC strategy)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"
            
            # Merged metadata should prefer ID3v2 (higher precedence)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "Synced Title"

    def test_default_strategy_is_sync(self):
        # Copy sample file to temp location with correct extension
        with TempFileWithMetadata({}, "wav") as test_file:
            # First, add ID3v2 metadata using TempFileWithMetadata methods
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            
            # Now write RIFF metadata without specifying strategy (should default to SYNC)
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"]
            }
            update_file_metadata(test_file, riff_metadata)
            
            # Verify both formats exist (SYNC strategy should sync both)
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            
            # Both formats should have the new metadata (SYNC strategy)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            
            # Merged metadata should prefer RIFF (WAV native format)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v1_not_preserved_with_sync_strategy(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Create test file with ID3v1 metadata using TempFileWithMetadata methods
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Add ID3v1 metadata using TempFileWithMetadata methods
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v1_album("ID3v1 Album")
            
            # Verify ID3v1 metadata was written
            id3v1_result = get_single_format_app_metadata(test_file, MetadataFormat.ID3V1)
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Now write ID3v2 metadata with SYNC strategy
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "Synced Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Synced Album"
            }
            update_file_metadata(test_file, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.SYNC)
            
            # Verify ID3v1 metadata behavior with different strategies
            # When ID3v2 is written, it overwrites the ID3v1 tag
            id3v1_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"  # ID3v1 was overwritten
            
            # Verify ID3v2 metadata was written with synced values
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"
            
            # Merged metadata should prefer ID3v2 (higher precedence)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "Synced Title"

    def test_id3v1_modification_success(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Create test file with ID3v1 metadata using TempFileWithMetadata methods
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Add ID3v1 metadata using TempFileWithMetadata methods
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v1_album("ID3v1 Album")
            
            # Verify ID3v1 metadata was written
            id3v1_result = get_single_format_app_metadata(str(test_file), MetadataFormat.ID3V1)
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Modify ID3v1 metadata directly should succeed
            update_file_metadata(str(test_file), {
                UnifiedMetadataKey.TITLE: "New Title"
            }, metadata_format=MetadataFormat.ID3V1)
            
            # Verify the modification was successful
            updated_id3v1_result = get_single_format_app_metadata(str(test_file), MetadataFormat.ID3V1)
            assert updated_id3v1_result.get(UnifiedMetadataKey.TITLE) == "New Title"

    def test_sync_strategy_wav_with_id3v1_field_truncation(self, sample_wav_file: Path, temp_audio_file: Path):
        # Create WAV file with ID3v1 metadata using TempFileWithMetadata methods
        with TempFileWithMetadata({}, "wav") as test_file:
            # Add ID3v1 metadata using TempFileWithMetadata methods
            test_file.set_id3v1_title("Short Title")
            test_file.set_id3v1_artist("Short Artist")
            test_file.set_id3v1_album("Short Album")
            
            # Verify ID3v1 metadata was written
            id3v1_result = get_single_format_app_metadata(test_file, MetadataFormat.ID3V1)
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "Short Title"
            
            # Now test SYNC strategy with long title that exceeds ID3v1 30-char limit
            long_title = "This is a Very Long Title That Exceeds ID3v1 Limits"
            sync_metadata = {
                UnifiedMetadataKey.TITLE: long_title,
                UnifiedMetadataKey.ARTISTS_NAMES: ["Long Artist Name That Exceeds Limits"],
                UnifiedMetadataKey.ALBUM_NAME: "Long Album Name That Exceeds Limits"
            }
            update_file_metadata(test_file, sync_metadata, metadata_strategy=MetadataWritingStrategy.SYNC)
            
            # Verify RIFF metadata has full values (no truncation)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == long_title
            assert riff_after.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Long Artist Name That Exceeds Limits"]
            assert riff_after.get(UnifiedMetadataKey.ALBUM_NAME) == "Long Album Name That Exceeds Limits"
            
            # Verify ID3v1 metadata is truncated (ID3v1 has 30-char field limits)
            id3v1_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V1)
            id3v1_title = id3v1_after.get(UnifiedMetadataKey.TITLE)
            id3v1_artist = id3v1_after.get(UnifiedMetadataKey.ARTISTS_NAMES)[0] if id3v1_after.get(UnifiedMetadataKey.ARTISTS_NAMES) else ""
            id3v1_album = id3v1_after.get(UnifiedMetadataKey.ALBUM_NAME)
            
            # Verify truncation occurred (should be shorter than original)
            assert len(id3v1_title) < len(long_title), f"ID3v1 title should be truncated: {id3v1_title}"
            assert len(id3v1_artist) < len("Long Artist Name That Exceeds Limits"), f"ID3v1 artist should be truncated: {id3v1_artist}"
            assert len(id3v1_album) < len("Long Album Name That Exceeds Limits"), f"ID3v1 album should be truncated: {id3v1_album}"
            
            # Verify truncation is reasonable (not too short, not too long)
            assert len(id3v1_title) <= 30, f"ID3v1 title should be <= 30 chars: {len(id3v1_title)}"
            assert len(id3v1_artist) <= 30, f"ID3v1 artist should be <= 30 chars: {len(id3v1_artist)}"
            assert len(id3v1_album) <= 30, f"ID3v1 album should be <= 30 chars: {len(id3v1_album)}"
            
            # Merged metadata should prefer RIFF (WAV native format has higher precedence)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == long_title  # Full title from RIFF
            assert merged.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Long Artist Name That Exceeds Limits"]
