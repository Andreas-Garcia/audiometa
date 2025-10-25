import pytest

from audiometa import (
    update_metadata,
    get_unified_metadata,
)
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestNoWritingOnFailure:

    def test_fail_on_unsupported_field_no_writing_done(self):
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            initial_read = get_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS) == ["Original Artist"]
            
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New Title",  # This should NOT be written
                UnifiedMetadataKey.ARTISTS: ["New Artist"],  # This should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # REPLAYGAIN is not supported by any format
            }
            
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            final_read = get_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS) == ["Original Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

    def test_fail_on_unsupported_field_no_changes_mp3_id3v2_only(self):
        initial_metadata = {
            "title": "Original MP3 Title",
            "artist": "Original MP3 Artist"
        }
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            initial_read = get_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original MP3 Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS) == ["Original MP3 Artist"]
            
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New MP3 Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS: ["New MP3 Artist"],  # Should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # Not supported by any format
            }
            
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            final_read = get_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original MP3 Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS) == ["Original MP3 Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

    def test_fail_on_unsupported_field_no_changes_flac_vorbis_only(self):
        initial_metadata = {
            "title": "Original FLAC Title",
            "artist": "Original FLAC Artist"
        }
        with TempFileWithMetadata(initial_metadata, "flac") as test_file:
            initial_read = get_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original FLAC Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS) == ["Original FLAC Artist"]
            
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New FLAC Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS: ["New FLAC Artist"],  # Should NOT be written
                UnifiedMetadataKey.REPLAYGAIN: "89 dB"  # Not supported by any format
            }
            
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            final_read = get_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original FLAC Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS) == ["Original FLAC Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.REPLAYGAIN) is None  # Should not exist

    def test_fail_on_unsupported_field_no_changes_wav_riff_only(self):
        initial_metadata = {
            "title": "Original WAV Title",
            "artist": "Original WAV Artist"
        }
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            initial_read = get_unified_metadata(test_file)
            assert initial_read.get(UnifiedMetadataKey.TITLE) == "Original WAV Title"
            assert initial_read.get(UnifiedMetadataKey.ARTISTS) == ["Original WAV Artist"]
            
            test_metadata = {
                UnifiedMetadataKey.TITLE: "New WAV Title",  # Should NOT be written
                UnifiedMetadataKey.ARTISTS: ["New WAV Artist"],  # Should NOT be written
                UnifiedMetadataKey.PUBLISHER: "Test Publisher"  # Not supported by RIFF format
            }
            
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError):
                update_metadata(test_file.path, test_metadata, fail_on_unsupported_field=True)
            
            final_read = get_unified_metadata(test_file)
            assert final_read.get(UnifiedMetadataKey.TITLE) == "Original WAV Title"  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.ARTISTS) == ["Original WAV Artist"]  # Should be unchanged
            assert final_read.get(UnifiedMetadataKey.PUBLISHER) is None  # Should not exist
