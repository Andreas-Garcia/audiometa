import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.test_helpers import TempFileWithMetadata


@pytest.mark.integration
class TestVorbisGenreReading:

    def test_vorbis_single_genre(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_vorbis_multiple_genres_separate_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_semicolon_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock; Alternative; Indie"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_comma_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Jazz, Fusion, Experimental"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Jazz", "Fusion", "Experimental"]

    def test_vorbis_genre_with_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Electronic/Dance/Ambient"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Electronic", "Dance", "Ambient"]

    def test_vorbis_genre_with_double_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock//Alternative//Indie"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock\\Alternative\\Indie"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_double_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock\\\\Alternative\\\\Indie"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_mixed_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock; Alternative, Indie/Experimental"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie", "Experimental"]

    def test_vorbis_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: " Rock ; Alternative ; Indie "
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock;;;Alternative"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative"]

    def test_vorbis_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ""
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == [""]

    def test_vorbis_genre_none_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: None
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_vorbis_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "   "
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["   "]

    def test_vorbis_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock & Roll; R&B; Hip-Hop"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock & Roll", "R&B", "Hip-Hop"]

    def test_vorbis_genre_unicode_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Música; 音楽; موسيقى"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Música", "音楽", "موسيقى"]

    def test_vorbis_genre_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases For Vorbis Format In FLAC Files"
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: long_genre
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == [long_genre]

    def test_vorbis_genre_custom_genre_names(self):
        custom_genres = [
            "Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave",
            "Synthwave", "Retrowave", "Outrun", "Future Funk", "Lo-Fi Hip Hop",
            "Ambient", "Drone", "Noise", "Experimental", "Avant-garde"
        ]
        
        for genre in custom_genres:
            with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
                update_file_metadata(test_file.path, {
                    UnifiedMetadataKey.GENRE_NAME: genre
                }, metadata_format=MetadataFormat.VORBIS)
                
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_vorbis_genre_multiple_custom_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            custom_genres = ["Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave", "Ambient", "Drone"]
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: custom_genres
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == custom_genres

    def test_vorbis_genre_no_genre_codes_support(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "17; 20; 131"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["17", "20", "131"]

    def test_vorbis_genre_text_based_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Rock; Alternative; Indie"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_no_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_vorbis_genre_with_other_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.VORBIS)
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "Alternative", "Indie"]
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_vorbis_genre_edge_case_single_character(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "A"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["A"]

    def test_vorbis_genre_edge_case_numbers_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "12345"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["12345"]

    def test_vorbis_genre_edge_case_special_separators_in_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"]
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"]

    def test_vorbis_genre_utf8_encoding(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: "Música Electrónica; 電子音楽; موسيقى إلكترونية"
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Música Electrónica", "電子音楽", "موسيقى إلكترونية"]

    def test_vorbis_genre_mixed_languages(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: ["Rock", "ロック", "Roc", "Рок"]
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock", "ロック", "Roc", "Рок"]

    def test_vorbis_genre_very_many_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            many_genres = [f"Genre {i}" for i in range(50)]
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: many_genres
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == many_genres

    def test_vorbis_genre_empty_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.GENRE_NAME: []
            }, metadata_format=MetadataFormat.VORBIS)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []
