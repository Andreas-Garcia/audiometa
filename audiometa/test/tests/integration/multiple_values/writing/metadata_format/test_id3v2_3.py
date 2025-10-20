from pathlib import Path

from audiometa import update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.id3v2.id3v2_metadata_inspector import ID3v2MetadataInspector


class TestMultipleEntriesId3v2_3:
    def test_write_multiple_artists_id3v2_3(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
        
        # Use helper to check the created ID3v2 frame directly
        verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(temp_audio_file, "TPE1")
        assert verification['success']
        assert "TPE1=Artist One;Artist Two;Artist Three" in verification['raw_output']
