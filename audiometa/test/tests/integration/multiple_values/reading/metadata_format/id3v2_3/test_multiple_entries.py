from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_full_metadata
)
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestId3v23MultipleEntries:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["One", "Two", "Three"], in_separate_frames=False)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_format_specific_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["One", "Two", "Three"], in_separate_frames=False)
            
            id3v2_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            artists = id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_full_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["One", "Two", "Three"], in_separate_frames=False)
            
            full_metadata = get_full_metadata(test_file.path)
            
            unified_artists = full_metadata['unified_metadata'].get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(unified_artists, list)
            assert len(unified_artists) == 3
            assert "One" in unified_artists
            assert "Two" in unified_artists
            assert "Three" in unified_artists
            
            id3v2_artists = full_metadata['format_metadata']['id3v2'].get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(id3v2_artists, list)
            assert len(id3v2_artists) == 3
            assert "One" in id3v2_artists
            assert "Two" in id3v2_artists
            assert "Three" in id3v2_artists

    def test_comment_field_returns_first_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_comments(["First comment", "Second comment", "Third comment"], in_separate_frames=False)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            comments = unified_metadata.get(UnifiedMetadataKey.COMMENT)
            
            assert isinstance(comments, str)
            assert comments == "First comment"

    def test_multiple_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_genres(["Rock", "Alternative", "Indie"], in_separate_frames=False)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Alternative" in genres
            assert "Indie" in genres

    def test_multiple_composers(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_composers(["Composer A", "Composer B", "Composer C"], in_separate_frames=False)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer A" in composers
            assert "Composer B" in composers
            assert "Composer C" in composers

    def test_separate_frames_behavior(self):
        """Test that in_separate_frames=True behaves as expected (keeps last value due to ID3v2 limitations)."""
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["Artist One", "Artist Two", "Artist Three"], in_separate_frames=True)
            
            # Note: Due to ID3v2 specification and tool limitations, in_separate_frames=True
            # cannot actually create multiple frames of the same type. Instead, multiple
            # calls to mid3v2 overwrite previous values, keeping only the last one.
            verification_result = test_file.verify_id3v2_multiple_entries_in_raw_data("TPE1", expected_count=1)
            
            assert verification_result['success'], f"Verification failed: {verification_result.get('error', 'Unknown error')}"
            assert verification_result['actual_count'] == 1, f"Expected 1 frame, got {verification_result['actual_count']}"
            assert not verification_result['has_multiple'], "Should have only one frame (last value kept)"
            assert verification_result['count_matches'], "Count should match expected value of 1"
            
            # Verify that only the last artist is kept
            entries = verification_result['entries']
            assert len(entries) == 1
            single_entry = entries[0]
            assert "Artist Three" in single_entry  # Only the last value should be kept
            assert "Artist One" not in single_entry  # Previous values should be overwritten
            assert "Artist Two" not in single_entry

    def test_single_frame_creates_one_frame(self):
        """Test that in_separate_frames=False creates a single TPE1 frame with multiple values."""
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["Artist One", "Artist Two", "Artist Three"], in_separate_frames=False)
            
            # Verify that only one frame was created using the raw data verification method
            verification_result = test_file.verify_id3v2_multiple_entries_in_raw_data("TPE1", expected_count=1)
            
            assert verification_result['success'], f"Verification failed: {verification_result.get('error', 'Unknown error')}"
            assert verification_result['actual_count'] == 1, f"Expected 1 frame, got {verification_result['actual_count']}"
            assert not verification_result['has_multiple'], "Should have only one frame when in_separate_frames=False"
            assert verification_result['count_matches'], "Count should match expected value of 1"
            
            # Verify the single entry contains all artists
            entries = verification_result['entries']
            assert len(entries) == 1
            single_entry = entries[0]
            assert "Artist One" in single_entry
            assert "Artist Two" in single_entry  
            assert "Artist Three" in single_entry