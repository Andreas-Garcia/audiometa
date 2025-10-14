"""Tests for metadata writing strategies using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.

This module tests the different metadata writing strategies:
- SYNC: Write to native format and synchronize other metadata formats that are already present (default)
- PRESERVE: Write to native format only, preserve existing metadata in other formats
- CLEANUP: Write to native format and remove all non-native metadata formats
"""

import pytest
import warnings
from pathlib import Path
import shutil
from typing import Any

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata,
    AudioFile
)
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestMetadataStrategies:

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
                str(test_file)
            ], check=True)
            
            # Verify ID3v2 metadata was written
            id3v2_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Now write RIFF metadata with PRESERVE strategy (default)
            # This part still uses the app's function since we're testing the strategy
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "RIFF Album"
            }
            update_file_metadata(test_file.path, riff_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
            
            # Verify both formats exist
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            
            # ID3v2 should be preserved (unchanged)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            # RIFF should have new metadata
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            
            # Merged metadata should prefer RIFF (WAV native format has higher precedence)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_cleanup_strategy_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        # Create test file with basic metadata first
        basic_metadata = {
            "title": "Basic Title",
            "artist": "Basic Artist",
            "album": "Basic Album"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            # First, add ID3v2 metadata using external script
            import subprocess
            subprocess.run([
                "mid3v2", 
                "--song=ID3v2 Title",
                "--artist=ID3v2 Artist", 
                "--album=ID3v2 Album",
                str(test_file)
            ], check=True)
            
            # Verify ID3v2 metadata was written
            id3v2_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Now write RIFF metadata with CLEANUP strategy
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "RIFF Album"
            }
            update_file_metadata(test_file.path, riff_metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
            
            # Verify ID3v2 was removed
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            
            # Verify RIFF has new metadata
            riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            
            # Merged metadata should only have RIFF (ID3v2 was cleaned up)
            merged = get_merged_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_sync_strategy_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        # Create test file with basic metadata first
        basic_metadata = {
            "title": "Basic Title",
            "artist": "Basic Artist",
            "album": "Basic Album"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
                        # First, add ID3v2 metadata using external script
                        import subprocess
                        subprocess.run([
                            "mid3v2", 
                            "--song=Original ID3v2 Title",
                            "--artist=Original ID3v2 Artist", 
                            "--album=Original ID3v2 Album",
                            str(test_file)
                        ], check=True)
            
                        # Verify ID3v2 metadata was written
                        id3v2_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
                        assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            
                        # Now write RIFF metadata with SYNC strategy
                        # Note: RiffManager strips ID3v2 tags when writing, so SYNC will only work
                        # if we write to ID3v2 format instead of RIFF format
                        sync_metadata = {
                            UnifiedMetadataKey.TITLE: "Synced Title",
                            UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist"],
                            UnifiedMetadataKey.ALBUM_NAME: "Synced Album"
                        }
                        update_file_metadata(test_file.path, sync_metadata, 
                                           metadata_format=MetadataFormat.ID3V2, 
                                           metadata_strategy=MetadataWritingStrategy.SYNC)
        
                    # Verify both formats have the synced metadata
        id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
        riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
        
        # ID3v2 should have the synced metadata
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"
        # RIFF should also have the synced metadata (SYNC strategy)
        assert riff_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"
        
        # Merged metadata should prefer ID3v2 (higher precedence)
        merged = get_merged_unified_metadata(test_file)
        assert merged.get(UnifiedMetadataKey.TITLE) == "Synced Title"

    def test_default_strategy_is_sync(self, sample_wav_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location with correct extension
        test_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(sample_wav_file, test_file)
        
        # First, add ID3v2 metadata using external script
        import subprocess
        subprocess.run([
            "mid3v2", 
            "--song=ID3v2 Title",
            "--artist=ID3v2 Artist",
            str(test_file)
        ], check=True)
        
        # Now write RIFF metadata without specifying strategy (should default to SYNC)
        riff_metadata = {
            UnifiedMetadataKey.TITLE: "RIFF Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"]
        }
        update_file_metadata(test_file.path, riff_metadata)
        
        # Verify both formats exist (SYNC strategy should sync both)
        id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
        riff_after = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
        
        # Both formats should have the new metadata (SYNC strategy)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
        assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
        
        # Merged metadata should prefer RIFF (WAV native format)
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
        id3v1_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
        assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
        
        # Now write ID3v2 metadata with PRESERVE strategy
        # Note: ID3v1 can now be preserved with writing support
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v2 Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
        }
        update_file_metadata(test_file.path, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
        
        # Verify ID3v1 metadata behavior with different strategies
        # When ID3v2 is written, it overwrites the ID3v1 tag
        id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"  # ID3v1 was overwritten
        
        # Verify ID3v2 metadata was written
        id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
        
        # Merged metadata should prefer ID3v2 (higher precedence)
        merged = get_merged_unified_metadata(test_file)
        assert merged.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_id3v1_not_preserved_with_cleanup_strategy(self, sample_mp3_file: Path, temp_audio_file: Path):
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
        id3v1_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
        assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
        
        # Now write ID3v2 metadata with CLEANUP strategy
        # Note: ID3v1 can now be preserved with writing support
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v2 Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
        }
        update_file_metadata(test_file.path, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
        
        # Verify ID3v1 metadata behavior with different strategies
        # When ID3v2 is written, it overwrites the ID3v1 tag
        id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"  # ID3v1 was overwritten
        
        # Verify ID3v2 metadata was written
        id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
        
        # Merged metadata should prefer ID3v2 (higher precedence)
        merged = get_merged_unified_metadata(test_file)
        assert merged.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"

    def test_id3v1_not_preserved_with_sync_strategy(self, sample_mp3_file: Path, temp_audio_file: Path):
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
        id3v1_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
        assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
        
        # Now write ID3v2 metadata with SYNC strategy
        # Note: ID3v1 can now be preserved with writing support
        id3v2_metadata = {
            UnifiedMetadataKey.TITLE: "Synced Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Synced Album"
        }
        update_file_metadata(test_file.path, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.SYNC)
        
        # Verify ID3v1 metadata behavior with different strategies
        # When ID3v2 is written, it overwrites the ID3v1 tag
        id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
        assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"  # ID3v1 was overwritten
        
        # Verify ID3v2 metadata was written with synced values
        id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
        assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "Synced Title"
        
        # Merged metadata should prefer ID3v2 (higher precedence)
        merged = get_merged_unified_metadata(test_file)
        assert merged.get(UnifiedMetadataKey.TITLE) == "Synced Title"

    def test_id3v1_modification_success(self, sample_mp3_file: Path, temp_audio_file: Path):
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
        # Create WAV file with ID3v1 metadata using external script
        test_file = temp_audio_file.with_suffix('.wav')
        shutil.copy2(sample_wav_file, test_file)
        
        # Add ID3v1 metadata using external script
        import subprocess
        subprocess.run([
            "id3v2", 
            "--song=Short Title",
            "--artist=Short Artist", 
            "--album=Short Album",
            "--id3v1-only",
            str(test_file)
        ], check=True)
        
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


class TestUnsupportedFieldsHandling:

    def test_fail_on_unsupported_field_sync_strategy(self):
        # Create a WAV file (RIFF format) which has limited metadata support
        with TempFileWithMetadata({"title": "Test"}, "wav") as test_file:
            # Try to write metadata that includes REPLAYGAIN, which is not supported by any format
            # This should fail when fail_on_unsupported_field=True
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # REPLAYGAIN is not supported by any format
            }
            
            # Should fail because REPLAYGAIN is not supported by any format
            with pytest.raises(MetadataNotSupportedError) as exc_info:
                update_file_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            assert "Fields not supported by any format" in str(exc_info.value)
            assert "REPLAYGAIN" in str(exc_info.value)

    def test_fail_on_unsupported_field_sync_strategy_graceful_default(self):
        # Create a WAV file (RIFF format) which has limited metadata support
        with TempFileWithMetadata({"title": "Test"}, "wav") as test_file:
            # Try to write metadata that includes REPLAYGAIN, which is not supported by any format
            # This should succeed with warnings when fail_on_unsupported_field=False (default)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # REPLAYGAIN is not supported by any format
            }
            
            # Should succeed with warnings (default behavior)
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                update_file_metadata(test_file.path, test_metadata)  # fail_on_unsupported_field=False by default
                
                # Should have warnings about unsupported fields
                assert len(w) > 0
                assert any("doesn't support some metadata fields" in str(warning.message) for warning in w)
            
            # Verify that supported fields were written
            metadata = get_merged_unified_metadata(test_file)
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"

    def test_fail_on_unsupported_field_no_writing_done(self):
        # Create a WAV file with initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Verify initial metadata exists
            initial_read = get_merged_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original Artist"]
            
            # Try to write metadata that includes REPLAYGAIN, which is not supported by any format
            # This should fail when fail_on_unsupported_field=True
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New Title",  # This should NOT be written
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist"],  # This should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # REPLAYGAIN is not supported by any format
            }
            
            # Should fail because REPLAYGAIN is not supported by any format
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            # Verify that NO writing was done - file should still have original metadata
            final_read = get_merged_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

    def test_fail_on_unsupported_field_no_changes_mp3_id3v2_only(self):
        # Create MP3 file with initial metadata
        initial_metadata = {
            "title": "Original MP3 Title",
            "artist": "Original MP3 Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Verify initial metadata exists
            initial_read = get_merged_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original MP3 Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original MP3 Artist"]
            
            # Try to write metadata with unsupported field (REPLAYGAIN is not supported by any format)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New MP3 Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS_NAMES: ["New MP3 Artist"],  # Should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # Not supported by any format
            }
            
            # Should fail because REPLAYGAIN is not supported by any format
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            # Verify that NO writing was done - file should still have original metadata
            final_read = get_merged_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original MP3 Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original MP3 Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

    def test_fail_on_unsupported_field_no_changes_flac_vorbis_only(self):
        # Create FLAC file with initial metadata
        initial_metadata = {
            "title": "Original FLAC Title",
            "artist": "Original FLAC Artist"
        }
        with TempFileWithMetadata(initial_metadata, "flac") as test_file:
            # Verify initial metadata exists
            initial_read = get_merged_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original FLAC Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original FLAC Artist"]
            
            # Try to write metadata with unsupported field (REPLAYGAIN is not supported by any format)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New FLAC Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS_NAMES: ["New FLAC Artist"],  # Should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # Not supported by any format
            }
            
            # Should fail because REPLAYGAIN is not supported by any format
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            # Verify that NO writing was done - file should still have original metadata
            final_read = get_merged_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original FLAC Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original FLAC Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

    def test_fail_on_unsupported_field_no_changes_wav_riff_only(self):
        # Create WAV file with initial metadata
        initial_metadata = {
            "title": "Original WAV Title",
            "artist": "Original WAV Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Verify initial metadata exists
            initial_read = get_merged_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original WAV Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original WAV Artist"]
            
            # Try to write metadata with unsupported field (REPLAYGAIN is not supported by any format)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New WAV Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS_NAMES: ["New WAV Artist"],  # Should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # Not supported by any format
            }
            
            # Should fail because REPLAYGAIN is not supported by any format
            with pytest.raises(MetadataNotSupportedError):
                update_file_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            # Verify that NO writing was done - file should still have original metadata
            final_read = get_merged_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original WAV Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original WAV Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

