"""Tests for unsupported fields handling in metadata writing strategies.

This module tests how different strategies handle unsupported metadata fields
and the fail_on_unsupported_field parameter behavior.
"""

import pytest
import warnings

from audiometa import (
    update_file_metadata,
    get_merged_unified_metadata,
)
from audiometa.exceptions import MetadataNotSupportedError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestUnsupportedFieldsHandling:

    def test_fail_on_unsupported_field_enabled(self):
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

    def test_fail_on_unsupported_field_disabled_graceful_default(self):
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
                # Check for any warning about unsupported fields
                warning_messages = [str(warning.message) for warning in w]
                assert any("unsupported" in msg.lower() or "not supported" in msg.lower() for msg in warning_messages)
            
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

    def test_fail_on_unsupported_field_preserve_strategy(self):
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
            
            # Try to write metadata with unsupported field (BPM is not supported by RIFF format)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New WAV Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS_NAMES: ["New WAV Artist"],  # Should NOT be written
                UnifiedMetadataKey.BPM: 120  # Not supported by RIFF format
            }
            
            # Should fail because BPM is not supported by RIFF format
            with pytest.raises(MetadataNotSupportedError) as exc_info:
                update_file_metadata(test_file.path, test_metadata, 
                                   metadata_strategy=MetadataWritingStrategy.PRESERVE,
                                   fail_on_unsupported_field=True)
            
            assert "Fields not supported by riff format" in str(exc_info.value)
            assert "BPM" in str(exc_info.value)
            
            # Verify that NO writing was done - file should still have original metadata
            final_read = get_merged_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original WAV Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original WAV Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.BPM) is None  # Should not exist

    def test_fail_on_unsupported_field_cleanup_strategy(self):
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
            
            # Try to write metadata with unsupported field (BPM is not supported by RIFF format)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New WAV Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS_NAMES: ["New WAV Artist"],  # Should NOT be written
                UnifiedMetadataKey.BPM: 120  # Not supported by RIFF format
            }
            
            # Should fail because BPM is not supported by RIFF format
            with pytest.raises(MetadataNotSupportedError) as exc_info:
                update_file_metadata(test_file.path, test_metadata, 
                                   metadata_strategy=MetadataWritingStrategy.CLEANUP,
                                   fail_on_unsupported_field=True)
            
            assert "Fields not supported by riff format" in str(exc_info.value)
            assert "BPM" in str(exc_info.value)
            
            # Verify that NO writing was done - file should still have original metadata
            final_read = get_merged_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original WAV Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original WAV Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.BPM) is None  # Should not exist
