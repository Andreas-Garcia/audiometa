from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_full_metadata
)
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestRiffMultipleEntries:
    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["One", "Two", "Three"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_format_specific_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["One", "Two", "Three"])
            
            riff_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            artists = riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists

    def test_multiple_artists_full_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["One", "Two", "Three"])
            
            full_metadata = get_full_metadata(test_file.path)
            
            unified_artists = full_metadata['unified_metadata'].get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(unified_artists, list)
            assert len(unified_artists) == 3
            assert "One" in unified_artists
            assert "Two" in unified_artists
            assert "Three" in unified_artists
            
            riff_artists = full_metadata['format_metadata']['riff'].get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(riff_artists, list)
            assert len(riff_artists) == 3
            assert "One" in riff_artists
            assert "Two" in riff_artists
            assert "Three" in riff_artists

    def test_comment_field_returns_first_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_comments(["First comment", "Second comment", "Third comment"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            comments = unified_metadata.get(UnifiedMetadataKey.COMMENT)
            
            assert isinstance(comments, str)
            assert comments == "First comment"

    def test_multiple_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_genres(["Rock", "Alternative", "Indie"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            genres = unified_metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock" in genres
            assert "Alternative" in genres
            assert "Indie" in genres

    def test_multiple_composers(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_composers(["Composer A", "Composer B", "Composer C"])
            
            unified_metadata = get_merged_unified_metadata(test_file.path)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer A" in composers
            assert "Composer B" in composers
            assert "Composer C" in composers