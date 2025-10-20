
from audiometa import get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from test.helpers.id3v2.id3v2_header_verifier import ID3HeaderVerifier


class TestId3v2_4Mixed:
    def test_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_4_multiple_artists(["Artist 1;Artist 2", "Artist 3", "Artist 4"])
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            verification = test_file.verify_id3v2_4_multiple_entries_in_raw_data("TPE1", expected_count=3)
            
            assert "TPE1=Artist 1;Artist 2 / Artist 3 / Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists


    def test_multiple_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_4_multiple_artists(["Artist One", "Artist Two", "Artist Three"], in_separate_frames=False)
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            verification = test_file.verify_id3v2_4_multiple_entries_in_raw_data("TPE1", expected_count=3)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert "TPE1=Artist One / Artist Two / Artist Three" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists


    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            test_file.set_id3v2_4_single_artist("Artist One;Artist Two;Artist Three")
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            verification = test_file.verify_id3v2_4_multiple_entries_in_raw_data("TPE1", expected_count=1)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert "TPE1=Artist One;Artist Two;Artist Three" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists