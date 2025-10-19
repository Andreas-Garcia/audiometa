from audiometa import get_single_format_app_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestRiffMixed:
    def test_mixed_separators_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["Artist 1;Artist 2", "Artist 3", "Artist 4"], in_separate_frames=True)
            verification = test_file.verify_riff_multiple_entries_in_raw_data("IART", expected_count=3)
            
            # Verify the raw data creation - exiftool shows RIFF tags as "Artist" not "IART"
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert verification["actual_count"] == 3, f"Expected 3 separate IART frames, found {verification['actual_count']}"
            assert "[RIFF]" in verification['raw_output']
            assert "Artist" in verification['raw_output']
            assert "Artist 1;Artist 2" in verification['raw_output'] 
            assert "Artist 3" in verification['raw_output']
            assert "Artist 4" in verification['raw_output']
            
            # Get RIFF metadata specifically to read the artists
            riff_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            artists = riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            
            # We created 3 separate RIFF frames, so we should get 3 entries 
            # (separator parsing happens at a higher level, not in RIFF format itself)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists
