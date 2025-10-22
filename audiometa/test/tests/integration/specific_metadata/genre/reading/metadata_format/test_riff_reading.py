import pytest

from audiometa import get_specific_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRiffGenreParsing:

    def test_riff_genre_codes_only_semicolon(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text("17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_codes_only_comma(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text("8, 30, 26")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz", "Fusion", "Ambient"]

    def test_riff_genre_codes_only_slash(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text("52/35/26")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic", "Acid Jazz", "Ambient"]

    def test_riff_genre_names_only_semicolon(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text("Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_names_only_comma(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text("Jazz, Fusion, Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz", "Fusion", "Experimental"]

    def test_riff_genre_names_only_slash(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Electronic/Dance/Ambient")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic", "Dance", "Ambient"]

    def test_riff_genre_mixed_codes_and_names(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_mixed_with_pipe_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "17 | Alternative | 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_single_code(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_single_name(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Rock")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_unknown_code(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "999")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["999"]

    def test_riff_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_riff_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "   ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_riff_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( " Rock ; Alternative ; Indie ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_riff_genre_multiple_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Rock; Alternative, Indie/Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie", "Experimental"]

    def test_riff_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Rock;;;Alternative")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_riff_genre_code_mode_vs_text_mode(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: "Rock"
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_genre_edge_case_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases"
            test_file.set_riff_genre_text( long_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == [long_genre]

    def test_riff_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            special_genre = "Rock & Roll; R&B; Hip-Hop"
            test_file.set_riff_genre_text( special_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock & Roll", "R&B", "Hip-Hop"]

    def test_riff_writes_single_genre_from_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Alternative", "Indie"]
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_writes_genre_code_from_name(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: "Rock"
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_riff_writes_unknown_genre_as_code_255(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: "Unknown Genre"
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is not None

    def test_riff_handles_empty_genre_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            update_metadata(test_file.path, {
                UnifiedMetadataKey.GENRES_NAMES: []
            }, metadata_format=MetadataFormat.RIFF)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_future_riff_multi_genre_parsing_names(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_future_riff_multi_genre_parsing_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_future_riff_multi_genre_parsing_mixed(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_genre_text( "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]
