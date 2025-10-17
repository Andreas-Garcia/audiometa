import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestId3v2GenreReading:

    def test_id3v2_single_genre(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v2_multiple_genres_separate_frames(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_semicolon_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock; Alternative; Indie"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_comma_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Jazz, Fusion, Experimental"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Jazz", "Fusion", "Experimental"]

    def test_id3v2_genre_with_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Electronic/Dance/Ambient"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Electronic", "Dance", "Ambient"]

    def test_id3v2_genre_with_double_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock//Alternative//Indie"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock\\Alternative\\Indie"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_double_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock\\\\Alternative\\\\Indie"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_mixed_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock; Alternative, Indie/Experimental"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie", "Experimental"]

    def test_id3v2_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: " Rock ; Alternative ; Indie "
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock;;;Alternative"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ""
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v2_genre_none_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: None
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v2_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "   "
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v2_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock & Roll; R&B; Hip-Hop"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock & Roll", "R&B", "Hip-Hop"]

    def test_id3v2_genre_unicode_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Música; 音楽; موسيقى"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Música", "音楽", "موسيقى"]

    def test_id3v2_genre_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases For ID3v2 Format"
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: long_genre
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == [long_genre]

    def test_id3v2_genre_custom_genre_names(self):
        custom_genres = [
            "Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave",
            "Synthwave", "Retrowave", "Outrun", "Future Funk", "Lo-Fi Hip Hop"
        ]
        
        for genre in custom_genres:
            with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
                update_file_metadata(test_file.path, {
                    UnifiedMetadataKey.GENRE_NAME: genre
                }, metadata_format=MetadataFormat.ID3V2)
                
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v2_genre_multiple_custom_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            custom_genres = ["Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave"]
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: custom_genres
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == custom_genres

    def test_id3v2_genre_with_genre_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "17; 20; 131"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["17", "20", "131"]

    def test_id3v2_genre_mixed_names_and_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock; 20; Indie"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "20", "Indie"]

    def test_id3v2_genre_no_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v2_genre_with_other_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative"]
            }, metadata_format=MetadataFormat.ID3V2)
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative"]
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_id3v2_genre_id3v2_3_version(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative"]
            }, metadata_format=MetadataFormat.ID3V2_3)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_id3v2_4_version(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative"]
            }, metadata_format=MetadataFormat.ID3V2_4)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_edge_case_single_character(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "A"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["A"]

    def test_id3v2_genre_edge_case_numbers_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "12345"
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["12345"]

    def test_id3v2_genre_edge_case_special_separators_in_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"]
            }, metadata_format=MetadataFormat.ID3V2)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"]
