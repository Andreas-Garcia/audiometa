from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestId3v2_4Mixed:
    def test_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            metadata = {
                UnifiedMetadataKey.TITLE: "Single Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"],
                UnifiedMetadataKey.ALBUM_NAME: "Single Album",
                UnifiedMetadataKey.COMPOSER: ["Composer 1", "Composer 2", "Composer 3"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2_4)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            
            assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Single Title"
            assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Single Album"
            
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist 1" in artists
            assert "Artist 2" in artists
            
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer 1" in composers
            assert "Composer 2" in composers
            assert "Composer 3" in composers

    def test_legacy_data_single_entry_parsed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One;Artist Two;Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2_4)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_modern_format_multiple_entries_no_parsing(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist; with; semicolons", "Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2_4)
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 5
            assert "Artist One" in artists
            assert "Artist" in artists
            assert "with" in artists
            assert "semicolons" in artists
            assert "Artist Three" in artists