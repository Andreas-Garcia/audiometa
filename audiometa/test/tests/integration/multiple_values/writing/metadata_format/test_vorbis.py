from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.vorbis.vorbis_metadata_inspector import VorbisMetadataInspector
from audiometa.test.helpers.vorbis.vorbis_metadata_setter import VorbisMetadataSetter


class TestMultipleEntriesVorbis:
    def test_write_multiple_artists(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Write multiple artists using update_file_metadata
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two", "Artist Three"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # verify against multiple entries in vorbis metadata not using the API
            verification = VorbisMetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "ARTIST")

            # For Vorbis we expect separate ARTIST entries, ensure there are three
            assert verification['actual_count'] == 3
            raw_output = verification['raw_output']
            assert "Artist One" in raw_output
            assert "Artist Two" in raw_output
            assert "Artist Three" in raw_output
            
            
            