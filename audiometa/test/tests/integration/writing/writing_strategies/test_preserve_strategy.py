"""Tests for PRESERVE metadata writing strategy.

This module tests the PRESERVE strategy which writes to native format only
and preserves existing metadata in other formats.
"""

import pytest
import shutil
from pathlib import Path

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata,
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestPreserveStrategy:

    def test_preserve_strategy_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        # First, add ID3v2 metadata using external script
        id3v2_metadata = {
            "title": "ID3v2 Title",
            "artist": "ID3v2 Artist",
            "album": "ID3v2 Album"
        }
        
        with TempFileWithMetadata(id3v2_metadata, "wav") as test_file:
            # For ID3v2 on WAV, we need to use mid3v2 directly
            import subprocess
            subprocess.run([
                "mid3v2", 
                "--song=ID3v2 Title",
                "--artist=ID3v2 Artist", 
                "--album=ID3v2 Album",
                str(test_file.path)
            ], check=True)
            
            # Verify ID3v2 metadata was written
            id3v2_result = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Now write RIFF metadata with PRESERVE strategy (default)
            # This part still uses the app's function since we're testing the strategy
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "RIFF Album"
            }
            update_file_metadata(test_file, riff_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
            
            # Verify both formats exist
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            
            # ID3v2 should be preserved (unchanged)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            # RIFF should have new metadata
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            
            # Merged metadata should prefer RIFF (WAV native format has higher precedence)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v1_not_preserved_with_preserve_strategy(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Create test file with ID3v1 metadata using external script
        test_file = temp_audio_file.with_suffix('.mp3')
        shutil.copy2(sample_mp3_file, test_file)
        
        # Add ID3v1 metadata using external script
        import subprocess
        subprocess.run([
            "id3v2", 
            "--song=ID3v1 Title",
            "--artist=ID3v1 Artist", 
            "--album=ID3v1 Album",
            "--id3v1-only",
            str(test_file)
        ], check=True)
        
        # Verify ID3v1 metadata was written
        id3v1_result = get_single_format_app_metadata(test_file, MetadataFormat.ID3V1)
        assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
        
        # Now write ID3v2 metadata with PRESERVE strategy
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v2 Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
        }
        update_file_metadata(test_file, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
        
        # Verify ID3v1 metadata behavior with PRESERVE strategy
        # ID3v1 should be preserved (not overwritten) with PRESERVE strategy
        id3v1_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V1)
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"  # ID3v1 was preserved
        
        # Verify ID3v2 metadata was written
        id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
        
        # Merged metadata should prefer ID3v2 (higher precedence)
        merged = get_merged_unified_metadata(test_file)
        assert merged.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
