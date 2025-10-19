from audiometa import get_specific_metadata, get_single_format_app_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestRiffMultipleEntries:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["One", "Two", "Three"], in_separate_frames=True)
            
            # Verify that artists are actually stored in separate RIFF frames
            verification_result = test_file.verify_riff_multiple_entries_in_raw_data("IART", expected_count=3)
            
            assert verification_result["success"], f"Verification failed: {verification_result.get('error', 'Unknown error')}"
            assert verification_result["actual_count"] == 3, f"Expected 3 separate IART frames, found {verification_result['actual_count']}"
            
            # Get RIFF metadata specifically to read the artists
            riff_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            artists = riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)

            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists